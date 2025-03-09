import base64
from src.lambda_function import lambda_handler

event = {
  "version": "2.0",
  "routeKey": "$default",
  "rawPath": "/jihasil-stage/post-media/Ts_WFvbvdj2YwMWs7uSrm/스크린캐스트%202024-12-09%2000-00-38.webm",
  "rawQueryString": "width=640",
  "headers": {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "host": "test-cloudfront.net",
    "user-agent": "Mozilla/5.0 (compatible; ExampleClient/1.0)",
    "via": "2.0 xxxxx.cloudfront.net (CloudFront)",
    "x-amz-cf-id": "abc123def456ghi789",
    "x-forwarded-for": "203.0.113.0",
    "x-forwarded-port": "443",
    "x-forwarded-proto": "https"
  },
  "queryStringParameters": {
    "width": "700"
  },
  "requestContext": {
    "accountId": "anonymous",
    "apiId": "abcdefghij",
    "domainName": "test-cloudfront.net",
    "domainPrefix": "test-cloudfront",
    "http": {
      "method": "GET",
      "path": "/jihasil-stage/image/001.png/",
      "protocol": "HTTP/1.1",
      "sourceIp": "203.0.113.0",
      "userAgent": "Mozilla/5.0 (compatible; ExampleClient/1.0)"
    },
    "requestId": "abcdefghijklmnopqrst",
    "routeKey": "$default",
    "stage": "$default",
    "time": "10/Dec/2024:12:00:00 +0000",
    "timeEpoch": 1702219200000
  },
  "isBase64Encoded": False
}

import time

tik = time.time()
response = lambda_handler(event, None)
tok = time.time()

print(response.get('statusCode'))
print("elapsed %f" % (tok - tik))

test_file_path = "test_no_resize.webp"
body_data = base64.b64decode(response.get("body"))

with open(test_file_path, "wb") as image_file:
    image_file.write(body_data)