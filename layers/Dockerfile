FROM public.ecr.aws/lambda/python:3.11

RUN yum install zip find -y
# Copy python requirements to the docker container and install packages in Lambda-compatible path
COPY requirements.txt .

# Install Python packages
RUN mkdir /packages
# compy the requirements file to the container
COPY requirements.txt /packages/
# Create the correct directory structure for Lambda layers
RUN mkdir -p /packages/opencv-python-3.11/python/lib/python3.11/site-packages

# Install the packages in the Lambda layer compatible directory
RUN python3.11 -m pip install --no-cache-dir -r /packages/requirements.txt -t /packages/opencv-python-3.11/python/lib/python3.11/site-packages

WORKDIR /packages/opencv-python-3.11/python/lib/python3.11/site-packages
# Clean up unnecessary files
RUN rm -rf *.dist-info
RUN find . -name "tests" -type d | xargs -I{} rm -rf {}
RUN find . -name "docs" -type d | xargs -I{} rm -rf {}
RUN find . -name "__pycache__" -type d | xargs -I{} rm -rf {}
RUN rm -rf boto*
# Create a zip file for the Lambda Layer deployment
WORKDIR /packages/opencv-python-3.11/
RUN zip -r9 /packages/cv2-python311.zip .



# Cleanup after zipping
WORKDIR /packages/
RUN rm -rf /packages/opencv-python-3.11/


