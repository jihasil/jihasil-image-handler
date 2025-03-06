import boto3
from botocore.exceptions import ClientError
import base64
from src.image_resizer import resize_image
from urllib.parse import unquote


def lambda_handler(event, context):
    # Parse Lambda Function URL request
    raw_path = event.get('rawPath', '').rstrip('/')

    # Extract the bucket name and file path
    try:
        bucket_name, image_path = raw_path.lstrip('/').split('/', 1)
        # decode url
        image_path = unquote(image_path)
        print(image_path)
    except ValueError:
        return {
            'statusCode': 400,
            'body': 'Invalid request path. Expected format: /<bucket_name>/<file_path>',
        }

    # Extract width parameter from query string
    width = int(event.get("queryStringParameters", {"width": 0}).get("width"))

    # S3 client
    s3 = boto3.client('s3')

    try:
        # Fetch image from S3
        s3_object = s3.get_object(Bucket=bucket_name, Key=image_path)
        image_data = s3_object['Body'].read()

        # Resize the image
        buffer = resize_image(image_data, width)

        # Return the resized image as the response
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {
            'statusCode': 200,
            'body': encoded_image,
            'isBase64Encoded': True,
            'headers': {
                'Content-Type': s3_object['ContentType']
            }
        }

    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return {
                'statusCode': 404,
                'body': 'The requested image does not exist.'
            }
        else:
            raise e
