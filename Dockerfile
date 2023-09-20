FROM python:3.11-slim

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "app.main:app" ]