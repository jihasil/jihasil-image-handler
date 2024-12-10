import boto3
from botocore.exceptions import ClientError
import base64
from src.image_resizer import resize_image


def lambda_handler(event, context):
    # Parse Lambda Function URL request
    raw_path = event.get('rawPath', '').rstrip('/')
    raw_query_string = event.get('rawQueryString', '')

    # Extract the bucket name and file path
    try:
        bucket_name, image_path = raw_path.lstrip('/').split('/', 1)
    except ValueError:
        return {
            'statusCode': 400,
            'body': 'Invalid request path. Expected format: /<bucket_name>/<file_path>',
        }

    # Extract width parameter from query string
    width = None
    if raw_query_string:
        params = {k: v for k, v in (pair.split('=') for pair in raw_query_string.split('&'))}
        width = int(params.get('width', 0)) if 'width' in params else None

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
                'statusCode': 200,
                'body': encoded_image,
                'isBase64Encoded': True,
                'headers': {
                    'Content-Type': s3_object['ContentType']
                }
            }

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
