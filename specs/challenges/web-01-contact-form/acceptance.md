# Acceptance criteria — Contact form

Challenge: `web-01-contact-form`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### WEB01-AC1 — Form renders all fields

Given the contact page is open
When it has loaded
Then `contact-name`, `contact-email`, `contact-interest`, `contact-message` and `contact-submit` are all visible

### WEB01-AC2 — Empty submission is blocked client-side

Given every field is empty
When `contact-submit` is activated
Then no request is sent and a validation message appears

### WEB01-AC3 — Invalid e-mail is flagged

Given `contact-email` contains `not-an-email` and the rest are filled
When `contact-submit` is activated
Then a validation message identifies the e-mail field

### WEB01-AC4 — Valid submission calls the API

Given every field is filled correctly
When `contact-submit` is activated
Then a POST to /contact/ is issued with name, email, interest and message

### WEB01-AC5 — Success state is shown

Given the API responds 200
When the response is handled
Then `contact-success` is visible and contains the returned message

### WEB01-AC6 — Failure state is shown

Given the API responds 422 or the request fails
When the response is handled
Then `contact-error` is visible and the entered data is not lost

### WEB01-AC7 — Double submission is prevented

Given a submission is in flight
When `contact-submit` is activated again
Then only one request is sent
