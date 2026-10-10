# Convert the sample Python request body into JSON text, like an HTTP client would.
import json

# Import the real backend Lambda handler.
from lambda_function import lambda_handler

# Simulate POST /pets with a required field intentionally missing.
test_event = {
    "httpMethod": "POST",
    "path": "/pets",
    "body": json.dumps({
        "type": "dog"
    })
}

# Call the backend handler locally.
response = lambda_handler(test_event, None)

# Missing name must be rejected with HTTP 400 Bad Request.
assert response["statusCode"] == 400

# Print the controlled JSON error response as evidence.
print("Response:", response)
