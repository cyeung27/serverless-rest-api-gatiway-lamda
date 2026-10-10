# Set a temporary local environment variable for the authorizer test.
# This is demo-only test data, not a production token or credential.
import os

# Import the real authorizer Lambda handler.
from authorizer_function import lambda_handler

# Configure the token the authorizer expects during this local test.
os.environ["API_TOKEN"] = "local-test-token"

# Supply a realistic-looking method ARN because API Gateway sends one to authorizers.
# The authorizer echoes this ARN into the Allow or Deny policy it returns.
method_arn = (
    "arn:aws:execute-api:us-east-1:example-account:example-api-id/"
    "dev/GET/pets"
)

# Test an authorization header containing the expected bearer token.
allowed_event = {
    "authorizationToken": "Bearer local-test-token",
    "methodArn": method_arn
}

# Call the real authorizer and confirm it returns an Allow policy.
allowed_response = lambda_handler(allowed_event, None)
allowed_effect = allowed_response["policyDocument"]["Statement"][0]["Effect"]
assert allowed_effect == "Allow"

# Test an authorization header containing an incorrect token.
denied_event = {
    "authorizationToken": "Bearer incorrect-token",
    "methodArn": method_arn
}

# Call the real authorizer and confirm it returns a Deny policy.
denied_response = lambda_handler(denied_event, None)
denied_effect = denied_response["policyDocument"]["Statement"][0]["Effect"]
assert denied_effect == "Deny"

# Print both outcomes as local test evidence after all assertions pass.
print("Authorizer tests passed:")
print("  Valid token decision:", allowed_effect)
print("  Invalid token decision:", denied_effect)
