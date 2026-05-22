# gachafakebackend
Simulating a fake gacha backend using AWS services. 
# Fake Gacha Backend Security Project

## Overview

This project is a simulated mobile game backend designed to demonstrate practical backend security and cloud security concepts using AWS.

The goal is not to build a real game, but to design and defend a realistic API-driven backend that resembles systems commonly targeted by attackers.

This project focuses on:
- Authentication and authorization
- API security
- JWT validation
- Secure backend architecture
- Abuse prevention
- AWS-native security controls

---

## Project Goals

The backend simulates systems commonly found in gacha/mobile games, including:

- User authentication and session management
- Player profile handling
- Inventory and currency systems
- Daily rewards and gacha actions
- Monitoring and abuse detection

Security goals include:
- Preventing unauthorized API access
- Understanding IDOR vulnerabilities
- Preventing token replay attacks
- Defending against API abuse and automation
- Correct authentication vs authorization handling

---

# Current Architecture

```text
Client Application
        ↓
Amazon Cognito
        ↓
API Gateway (JWT Authorizer)
        ↓
AWS Lambda
        ↓
Backend Logic
```

---

# Technologies Used

- AWS Cognito
- AWS Lambda
- AWS API Gateway
- JWT Authentication
- Python
- OAuth 2.0

---

# Progress Log

---

## 1. Authentication Setup with Amazon Cognito

Configured Amazon Cognito as the identity provider for the backend.

### Configuration
- Email-based sign in
- Self-registration enabled
- Required email attribute
- Temporary localhost return URL for testing

---

## 2. OAuth Flow Research

Studied the differences between:
- Authorization Code Grant
- Implicit Grant

### Authorization Code Grant
Uses a temporary authorization code exchanged server-side for tokens. This prevents exposing tokens directly to the browser.

### Implicit Grant
Returns tokens directly through the browser URL. This is weaker because tokens may leak through browser history, logs, or extensions.

For temporary testing, Implicit Grant was enabled.

---

## 3. AWS Lambda Backend

Created a Lambda function called:

```python
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "You reached the backend"
    }
```

This confirms that API requests successfully reach the backend service.

---

## 4. API Gateway Integration

Configured an HTTP API Gateway and connected it to the Lambda function.

### Route
```text
GET /profile
```

When a client sends a GET request to `/profile`, API Gateway forwards the request to Lambda.


---

## 5. JWT Authorization

Added JWT authorization to protect the API endpoint.

### JWT Validation Checks
API Gateway now verifies:
- JWT signature validity
- Token expiration
- Issuer validation
- Audience/client ID validation

### Identity Source
```text
$request.header.Authorization
```

Only valid Cognito-issued tokens can access protected endpoints.


---

# Security Concepts Demonstrated

- OAuth 2.0
- JWT authentication
- Token validation
- Secure API architecture
- Authentication vs authorization
- API Gateway authorization flow
- Cloud-native security controls

---

# Future Improvements

Planned future additions include:
- DynamoDB player database
- Inventory system
- Gacha pull mechanics
- CloudWatch logging
- Rate limiting
- WAF integration
- Abuse detection automation
- Refresh token handling
- Role-based access control

---

# Learning Outcome

This project demonstrates practical understanding of:
- Real-world backend attack surfaces
- Secure cloud application design
- API protection strategies
- AWS serverless architecture
- Identity and access management

The focus is on building systems securely rather than only implementing functionality.
