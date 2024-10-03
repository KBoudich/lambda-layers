/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "lambda-layer",
      removal: "remove",
      home: "aws",
      region: "eu-west-1",
    };
  },
  async run() {
    const bucket = new sst.aws.Bucket("Bucket");

    const bucketArn = bucket.arn;

    bucket.subscribe(
      {
        handler: "src/lambda.handler",
        runtime: "python3.11",
        layers: [
          "arn:aws:lambda:eu-west-1:567686919184:layer:opencv-numpy-python3111:1",
        ],
        link: [bucket],
      },
      {
        events: ["s3:ObjectCreated:*"],
      }
    );
    return {
      bucketArn,
    };
  },
});
