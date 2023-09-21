# Instructions for contributors

Checkout code, code and run local

## Enviroment

Python 3.11+

## Create environment

**macOS / Linux**

`source env/bin/activate` 

**Windows**

`env \Scripts\activate.bat`

## Deactivate environment

In root project folder run command `deactivate` in terminal

```bash
pip install -r requirements.txt
```

## Run server

```bash
uvicorn app.main:app --reload
```