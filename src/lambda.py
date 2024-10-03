import boto3
import numpy as np
import cv2
import fitz

s3_client = boto3.client('s3')


def download_s3_object(bucket_name, key):
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    data = s3_object['Body'].read()
    content_type = s3_object['ContentType']

    return data, content_type


def upload_image_to_convertions_s3(buffer, pdf_file_name, bucket_name):

    key = f"{pdf_file_name}.png"
    s3_client.put_object(Body=buffer, ContentType='image/png',
                         Bucket=bucket_name, Key=key,)
    print(f"image uploaded to S3 with key: {key}.png")


def convert_pdf_to_single_image(pdf_bytes, bucket_name, pdf_file_name):
    try:
        doc = fitz.open("pdf", pdf_bytes)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        noOfPages = doc.page_count
        images = []
        for pageNo in range(noOfPages):
            page = doc.load_page(pageNo)
            pix = page.get_pixmap(matrix=mat)
            im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.h, pix.w, pix.n)
            im = np.ascontiguousarray(im[..., [2, 1, 0]])
            images.append(im)
        combined_image = np.vstack(images)
        retval, buffer = cv2.imencode('.png', combined_image)
        if retval:
            upload_image_to_convertions_s3(
                buffer.tobytes(), pdf_file_name, bucket_name)
            return True
        else:
            print("Failed to encode image.")
            return False
    except Exception as e:
        print("Error:", e)
        return None


def handler(event, context):

    try:

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f'Bucket Name: {bucket}')
        print(f'File Name: {key}')

        document_bytes, content_type = download_s3_object(bucket, key)

        if content_type == 'application/pdf':
            print("convert pdf to image")
            convert_pdf_to_single_image(
                document_bytes, bucket_name=bucket, pdf_file_name=key)
        else:
            print("file type not supported")
    except Exception as e:
        print(f"Error occured while extracting text: {e}")

        raise e
