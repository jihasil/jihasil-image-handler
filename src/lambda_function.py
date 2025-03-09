import boto3
from botocore.exceptions import ClientError
import base64
from src.image_resizer import resize_image
from urllib.parse import unquote


# S3 client
s3 = boto3.client('s3')

def parse_request(event):
    # Parse Lambda Function URL request
    raw_path = event.get('rawPath', '').rstrip('/')

    # Extract the bucket name and file path
    bucket_name, image_key = raw_path.lstrip('/').split('/', 1)
    # decode url
    image_key = unquote(image_key)
    print(image_key)

    return bucket_name, image_key


def get_cached_image_key(image_path, width):
    file_name = image_path.rsplit('.', 1)[0]

    if width > 0:
        file_suffix = f"_{width}"
    else:
        file_suffix = ""

    return f"{file_name}{file_suffix}.webp"


def lambda_handler(event, context):
    try:
        bucket_name, image_key = parse_request(event)
    except ValueError:
        return {
            'statusCode': 400,
            'body': 'Invalid request path. Expected format: /<bucket_name>/<file_path>',
        }

    # Extract width parameter from query string
    width = int(event.get("queryStringParameters", {"width": 0}).get("width"))

    cached_image_key = get_cached_image_key(image_key, width)

    try:
        cached_s3_object = s3.get_object(Bucket=bucket_name, Key=cached_image_key)
        print(f"{cached_image_key} cache hit")
        cached_image_data = cached_s3_object['Body'].read()

        # Return the resized image as the response
        encoded_image = base64.b64encode(cached_image_data).decode('utf-8')

        return {
            'statusCode': 200,
            'body': encoded_image,
            'isBase64Encoded': True,
            'headers': {
                'Content-Type': cached_s3_object['ContentType']
            }
        }
    except ClientError as e:
        print(f"{cached_image_key} cache miss")

        try:
            # Fetch image from S3
            s3_object = s3.get_object(Bucket=bucket_name, Key=image_key)
            image_data = s3_object['Body'].read()
        except ClientError as e:
            return {
                'statusCode': 404,
                'body': 'The requested image does not exist.'
            }

        try:
            # Resize the image
            buffer = resize_image(image_data, width)

            # Return the resized image as the response
            encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

            s3.put_object(Bucket=bucket_name, Key=cached_image_key, Body=buffer, ContentType="image/webp")

            return {
                'statusCode': 200,
                'body': encoded_image,
                'isBase64Encoded': True,
                'headers': {
                    'Content-Type': "image/webp"
                }
            }
        except Exception as e:
            print(str(e))

            encoded_image = base64.b64encode(image_data).decode('utf-8')

            return {
                "statusCode": 200,
                "body": encoded_image,
                'isBase64Encoded': True,
            }
