FROM python:3.11-slim

# Send Python output straight to the terminal, unbuffered.
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# setuptools comes from the base image and lags behind its own advisories, so
# upgrade it here rather than shipping whatever the tag happens to carry.
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app
COPY ./scripts /code/scripts
COPY ./dev-challenge.db /code/dev-challenge.db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
