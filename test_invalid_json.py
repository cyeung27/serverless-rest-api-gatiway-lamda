# Import the real backend Lambda handler.
from lambda_function import lambda_handler

# Simulate POST /pets with a body that cannot be parsed as JSON.
test_event = {
    "httpMethod": "POST",
    "path": "/pets",
    "body": "this is not valid JSON"
}

# Call the backend handler locally.
response = lambda_handler(test_event, None)

# Malformed JSON must be rejected with HTTP 400 instead of an unhandled server error.
assert response["statusCode"] == 400

# Print the controlled JSON error response as evidence.
print("Invalid JSON test passed:", response)
