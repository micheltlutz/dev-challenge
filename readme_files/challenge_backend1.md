# Back-end Developer Technical Challenge 1

## Objective:
Your task is to design and implement a route named create_contact in your preferred back-end language/framework. This route will handle the reception and processing of contact information sent via a POST request.

## Specifications:

### 1. Endpoint:

- Develop an endpoint named /create_contact.

### 2. Input:

- The route should expect a POST request with a JSON body formatted as:

```json
{
    "nome": "User's Name",
    "email": "email@example.com",
    "message": "Message sent by the user",
    "interest": "Interest indicated by the user"
}
```
userid: email
    password: str
    fullname: str
    birthdate: date
### 3. Output:

- After successfully processing the input data, the endpoint should return a status code of `200 OK`.
- Additionally, it should provide a JSON response in the following format:

```json
{
    "msg": "Thank [contact.name], for getting in touch and sharing your interests. We look forward to hearing from you soon."
}
```

### Additional Points (Bonus):

- As a distinguishing feature, integrate a Swagger documentation for the create_contact route, outlining its expected input, output, and behavior. This would not only demonstrate your proficiency with modern API documentation standards but would also offer a clear interface for front-end developers and other consumers of your API.


## Final Considerations:

- Ensure your solution adheres to best practices in terms of code structure, error handling, and security.
- Thoroughly test the route to guarantee its reliability under different scenarios.
- Be sure to write a good README guiding how to run your project, dependencies and what you think is necessary to install and run the project.

We wish you the best with this challenge and eagerly await your solution!