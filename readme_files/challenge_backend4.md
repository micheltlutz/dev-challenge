# Back-end Developer Technical Challenge 4 - Pagination Statements

## Objective:

Its main objective is to design and implement the back-end logic to support the front-end interface for bank statement paging. This includes configuring the required API routes, handling data, and ensuring that the authentication process works as expected.


### Pagination:

The route should receive two parameters, `limit` and `offset`, the `limit` parameter will be the number of statements to be returned and the `offset` parameter will be the number of statements to be skipped. 

**GET:** `/statements/{limit}/{offset}`

### Response:

- After successfully processing the input data and check the auth information, the endpoint should return a status code of 200 OK. With JSON Statement list:

```json
[
  {
    "type": "Deposit",
    "amount": "15000.00",
    "description": "Payment from Freela",
    "from_user": "John Doe",
    "authentication": "45d064afbd6cf24613daed52133320b84ece0e2cc751995a4d0b94fca84823dd",
    "id": 1,
    "created_at": "2023-09-21T18:46:45.478966",
    "to_user": "John Doe",
    "bank_name": "Adams LLC"
  },
  {
    "type": "Deposit",
    "amount": "88.81",
    "description": "Trip authority window myself hour.",
    "from_user": "Holly Bailey",
    "authentication": "0ef6dc8284c7908ce7af354b10b6f354ff355a201f8f54e22bd60d928a6670c8",
    "id": 2,
    "created_at": "2020-09-07T00:00:00",
    "to_user": "Caitlin Bennett",
    "bank_name": "Williams-Norris"
  }, ....
]
```

## Validations:

- The Route shoul be authenticated if not user should receive a status code of 401 unauthorized, with the following message:

```json
{
  "detail": "Not authenticated"
}
```

### API Documentation

- As a bonus, provide Swagger documentation for the `/statements/{limit}/{offset}` route, offering insights into its expected input, output, and behavior.

### Unit Testing:

- Integrate unit tests to ensure the reliability of the route under various scenarios. Tests should cover, at a minimum:
  - Successful user login.
  - Validation failures (incorrect email format, invalid date, etc.).
  - Proper password hashing and retrieval.


## Final Considerations:

- Prioritize best practices concerning code structure, error handling, security, and scalability.
- Make sure to handle potential database errors or conflicts, such as duplicate email addresses.

Embarking on challenges like this offers a unique opportunity to showcase your skills. We wish you the best and eagerly await your innovative solution!

