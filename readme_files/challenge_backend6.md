# Back-end Developer Technical Challenge 6 - Profile edit

## Objective:

Its main objective is to design and implement a logical back-end to support a front-end interface that presents user registration data and allows editing and saving of this data. Easily add and configure API routes, manipulate data, and ensure the authentication process works as expected.

You are expected to create this backend in your preferred language/framework.


## Specifications:

**PUT**: `/users/{user_id}`

### Edit User Profile:

- The route should expect a PUT request with a JSON body formatted as:

```json
{
  "password": "string",
  "fullname": "string",
  "birthdate": "2024-01-02"
}
```

## Validations:

- The Route shoul be authenticated if not user should receive a status code of 401 unauthorized, with the following message:

```json
{
  "detail": "Not authenticated"
}
```

### API Documentation

- As a bonus, provide Swagger documentation for the `/users/{user_id}` route, offering insights into its expected input, output, and behavior.

### Unit Testing:

- Integrate unit tests to ensure the reliability of the route under various scenarios. Tests should cover, at a minimum:
  - Successful user login.
  - Validation failures (incorrect email format, invalid date, etc.).
  - Proper password hashing and retrieval.


## Final Considerations:

- Prioritize best practices concerning code structure, error handling, security, and scalability.
- Make sure to handle potential database errors or conflicts, such as duplicate email addresses.

Embarking on challenges like this offers a unique opportunity to showcase your skills. We wish you the best and eagerly await your innovative solution!

