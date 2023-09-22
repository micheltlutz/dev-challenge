# Back-end Developer Technical Challenge 2

## Objective:
Your primary mission is to design and implement a backend route named create_user for user registration. This route will handle the reception and processing of user data sent via a POST request. The solution should be crafted using your preferred back-end language/framework.

## Specifications:

### 1. Endpoint:
- Develop an endpoint named /create_user.

### 2. Input:
- The route should expect a POST request with a JSON body formatted as:

```json
{
    "userid": "user@example.com",
    "password": "string",
    "fullname": "string",
    "birthdate": "2023-09-22"
}
```

### 3. Database Integration:

- Implement database integration using SQLite.
- Successfully processed user data should be stored persistently in the SQLite database.

### 4. Field Validations & Security:

- Ensure that the `userid` field is validated for a correct email format.
- Ensure that the `birthdate` field strictly adheres to the date format as specified in the JSON model above.
- Passwords must be stored securely. 
  - Use password hashing techniques before storing the password in the database. 
  - We suggest using `bcrypt` for password hashing.

### 5. Output:

- After successfully processing the input data and storing the user information, the endpoint should return a status code of 201 Created.
- The response should contain a confirmation message, for example:

```json
{
    "msg": "User created successfully"
}
```

### 6. API Documentation

- As a bonus, provide Swagger documentation for the `create_user` route, offering insights into its expected input, output, and behavior.

### 7. Unit Testing:

- Integrate unit tests to ensure the reliability of the route under various scenarios. Tests should cover, at a minimum:
  - Successful user registration.
  - Validation failures (incorrect email format, invalid date, etc.).
  - Proper password hashing and retrieval.

## Final Considerations:

- Prioritize best practices concerning code structure, error handling, security, and scalability.
- Make sure to handle potential database errors or conflicts, such as duplicate email addresses.

Embarking on challenges like this allows you to demonstrate both your technical knowledge and your problem-solving abilities. We eagerly await your innovative solution and wish you the best of luck!