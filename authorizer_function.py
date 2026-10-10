import hmac
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    token = event.get("authorizationToken", "")
    method_arn = event.get("methodArn", "")
    expected_token = os.environ.get("API_TOKEN")
    
    is_authorized = (
        bool(expected_token) 
        and hmac.compare_digest(token, f"Bearer {expected_token}")
    )
    
    effect = "Allow" if is_authorized else "Deny"
    
    logger.info("Authorization Decision: %s ", effect)
    
    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": method_arn
                }
            ]
        }
    }