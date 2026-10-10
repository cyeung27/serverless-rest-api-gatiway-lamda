# Convert the sample Python request body into JSON text, like an HTTP client would.
import json

# Import the real backend Lambda handler rather than testing a copy of its logic.
from lambda_function import lambda_handler

# Simulate a valid API Gateway POST /pets request with the required fields.
test_event = {
    "httpMethod": "POST",
    "path": "/pets",
    "body": json.dumps({
        "name": "Buddy",
        "type": "dog"
    })
}

# Call the backend handler locally. None is enough because this test does not use context.
response = lambda_handler(test_event, None)

# A valid create-style request should return HTTP 201 Created.
assert response["statusCode"] == 201

# Print the response as evidence when the assertion passes.
print("Response:", response)
