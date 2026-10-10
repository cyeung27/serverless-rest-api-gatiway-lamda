# Convert Python dictionaries/lists to and from JSON text for API requests and responses.
import json

# Send safe operational information to CloudWatch Logs after deployment.
import logging

# Create one reusable logger for this module.
logger = logging.getLogger()

# Record informational messages and more severe messages.
logger.setLevel(logging.INFO)

# Sample in-memory data for this learning project.
# This list is not persistent storage: a real API would use a database such as DynamoDB.
PETS = [
    {"id": 1, "name": "Buddy", "type": "dog"},
    {"id": 2, "name": "Whiskers", "type": "cat"},
    {"id": 3, "name": "Luna", "type": "rabbit"}
]


# AWS Lambda calls this function for each API Gateway request.
# event contains request data; context contains Lambda runtime metadata.
def lambda_handler(event, context):
    # Read the HTTP operation safely. Use UNKNOWN if the event does not include one.
    http_method = event.get("httpMethod", "UNKNOWN")

    # Read the requested API route safely. Use / if the event does not include one.
    path = event.get("path", "/")

    # Log only safe routing data. Do not log tokens, headers, or the full request body.
    logger.info("Received request: method=%s path=%s", http_method, path)

    # Return the sample pet list when the caller requests GET /pets.
    if path == "/pets" and http_method == "GET":
        return {
            # HTTP 200 means the request completed successfully.
            "statusCode": 200,
            # Tell the client that the response body contains JSON.
            "headers": {"Content-Type": "application/json"},
            # Convert the Python dictionary and PETS list into JSON response text.
            "body": json.dumps({"pets": PETS})
        }

    # Handle a create-style request only when the caller sends POST /pets.
    if path == "/pets" and http_method == "POST":
        try:
            # API Gateway sends request bodies as text, so parse the JSON text into a dictionary.
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError:
            # Reject malformed JSON without exposing a Python traceback or raw request body.
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "Invalid JSON",
                    "statusCode": 400
                })
            }

        # Read the required client fields after JSON parsing succeeds.
        name = body.get("name")
        pet_type = body.get("type")

        # Reject incomplete input before it reaches the creation logic.
        if not name or not pet_type:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "Missing required fields",
                    "statusCode": 400
                })
            }

        # Build a demo pet object. This ID/list update is temporary and not database-backed.
        new_pet = {
            "id": len(PETS) + 1,
            "name": name,
            "type": pet_type
        }

        # Demonstrate an in-memory update for local learning only.
        # Do not rely on this for persistent production data in Lambda.
        PETS.append(new_pet)

        return {
            # HTTP 201 means a resource was created in this demonstration flow.
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            # Return the created demo object as JSON text.
            "body": json.dumps(new_pet)
        }

    # Return a controlled JSON error for every unsupported route or method.
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "error": "Not Found",
            "statusCode": 404
        })
    }
