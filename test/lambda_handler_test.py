import base64
from src.lambda_function import lambda_handler

event = {
  "Records": [
    {
      "cf": {
        "config": {
          "distributionId": "EDFDVBD6EXAMPLE"
        },
        "request": {
          "clientIp": "203.0.113.178",
          "method": "GET",
          "uri": "/jihasil-stage/image/003.png",
          "querystring": "width=300",
          "headers": {
            "host": [
              {
                "key": "Host",
                "value": "cloudfront.test.com"
              }
            ],
            "user-agent": [
              {
                "key": "User-Agent",
                "value": "curl/7.68.0"
              }
            ]
          }
        }
      }
    }
  ]
}

response = lambda_handler(event, None)

print(response.get('status'))

test_file_path = "lambda_test_003-width300.png"
body_data = base64.b64decode(response.get("body"))

with open(test_file_path, "wb") as image_file:
    image_file.write(body_data)