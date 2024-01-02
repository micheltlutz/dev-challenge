# Back-end Developer Technical Challenge 5 - Balance (Amout Value)

## Objective:

Its main objective is to design and implement back-end logic to support the front-end interface presenting the bank balance(amount) following the specific business rules below. This includes configuring API routes, manipulating data, and ensuring the authentication process works as expected. Easily add and configure API routes, manipulate data, and ensure the authentication process works as expected.


## Business rules from statements values:

> You should consider the following rules for the values of the statements to build amount:

- Rule for **Deposit**: If the user deposits from_user == to_user, the amount is added to the balance.
- Rule for **Deposit**: If the user deposits from_user != to_user, the amount is added to the balance.
- Rule for **Withdrawal**: If the user withdraws from their own account, the amount is subtracted from the balance.
- Rule for **Transfer**: If the user transfers to their own account (to_user == from_user), the amount is added to the balance.
- Rule for **Transfer**: If the user transfers to another account (to_user != from_user), the amount is subtracted from the balance.


**GET:** `/balance/`

## Response:

```json
{
  "amount": 13512.590000000002
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

- As a bonus, provide Swagger documentation for the `balance` route, offering insights into its expected input, output, and behavior.

### Unit Testing:

- Integrate unit tests to ensure the reliability of the route under various scenarios. Tests should cover, at a minimum:
  - Successful user login.
  - Validation failures (incorrect email format, invalid date, etc.).
  - Proper password hashing and retrieval.


## Final Considerations:

- Prioritize best practices concerning code structure, error handling, security, and scalability.
- Make sure to handle potential database errors or conflicts, such as duplicate email addresses.

Embarking on challenges like this offers a unique opportunity to showcase your skills. We wish you the best and eagerly await your innovative solution!

