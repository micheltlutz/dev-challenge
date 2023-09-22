# Front-end Developer Technical Challenge 1

## Objective:
Implement a graphical user interface that allows users to submit contact information through a form. The interface should be developed in your preferred language/framework and will be used to communicate with a REST API.

## Specifications:

### 1. Contact Form:
- The interface should include a form with the following fields:
    - Name (text field)
    - Email (text field with email format validation)
    - Message (multiline text field)
    - Interest (text field)
  The form should have a submit button to send the information.

### 2. API Communication:

- Upon form submission, make a POST request to the API at the following endpoint: /contact/.
- The request body should adhere to the following JSON format:

```json
{
    "nome": "User's Name",
    "email": "email@example.com",
    "message": "Message sent by the user",
    "interest": "Interest indicated by the user"
}
```

- Handle any potential errors that might occur during communication with the API and provide suitable user feedback.

### 3. API Documentation

- Comprehensive API documentation can be found at: http://localhost/docs#/contact. Use it to familiarize yourself with the request details and possible API responses.

### 4. Show response to user

- After sending the data to the API, show the user the response received from the API.

## Final Considerations:

- We value creativity, so feel free to design an intuitive and appealing interface.
- Your code implementation should be clean, well-organized, and adhere to best development practices.
- Be sure to write a good README guiding how to run your project, dependencies and what you think is necessary to install and run the project.

We wish you the best with the challenge! We're looking forward to seeing your solution!
