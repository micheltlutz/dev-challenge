# dev-challenge

## For development mode

**macOS / Linux**

`source env/bin/activate` 

**Windows**

`env \Scripts\activate.bat`

### Desactivate environment

In root project folder run command `deactivate` in terminal

## Create Image

```bash
docker build -t "dev-challenge" .
```

### Check if image was created

```bash
docker images
```
## Run container

```bash
docker run -d -p 8000:8000 dev-challenge:latest
```

Development challenge

## If you want to run the project in a container

```bash
docker-compose up -d --build
```

## Install

```bash
pip install -r requirements.txt
```

## Run server

```bash
uvicorn app.main:app --reload
```