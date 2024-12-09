import boto3
from botocore.exceptions import ClientError
import base64
from src.image_resizer import resize_image


def lambda_handler(event, context):
    # Parse CloudFront request
    request = event['Records'][0]['cf']['request']
    uri = request['uri']
    querystring = request.get('querystring', '')

    # Extract the bucket name and file path
    bucket_name, image_path = uri.lstrip('/').split('/', 1)

    # Extract width parameter from query string
    width = None
    if querystring:
        params = {k: v for k, v in (pair.split('=') for pair in querystring.split('&'))}
        width = int(params.get('width', 0))

    # S3 client
    s3 = boto3.client('s3')

    try:
        # Fetch image from S3
        s3_object = s3.get_object(Bucket=bucket_name, Key=image_path)
        image_data = s3_object['Body'].read()

        if not width:
            # Return the original image if width is not specified
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return {
                'status': '200',
                'statusDescription': 'OK',
                'body': encoded_image,
                'headers': {
                    'content-type': [{'key': 'Content-Type', 'value': s3_object['ContentType']}]
                },
                'bodyEncoding': 'base64',
            }

        buffer = resize_image(image_data, width)

        # Cache the resized image in S3 (optional step)
        resized_key = f"resized/{image_path}?width={width}"
        s3.put_object(Bucket=bucket_name, Key=resized_key, Body=buffer, ContentType=s3_object['ContentType'])

        # Return the resized image as the response
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {
            'status': '200',
            'statusDescription': 'OK',
            'body': encoded_image,
            'headers': {
                'content-type': [{'key': 'Content-Type', 'value': s3_object['ContentType']}]
            },
            'bodyEncoding': 'base64',
        }

    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return {
                'status': '404',
                'statusDescription': 'Not Found',
                'body': 'The requested image does not exist.',
            }
        else:
            raise e
