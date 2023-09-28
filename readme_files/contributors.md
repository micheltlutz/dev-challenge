# Instructions for contributors

Checkout code, code and run local

## Enviroment

Python 3.11+

## Create environment

**macOS / Linux**

`source venv/bin/activate` 

**Windows**

- `.\venv\Scripts\activate.bat`

- `.\venv\Scripts\activate.ps1`

## Deactivate environment

In root project folder run command `deactivate` in terminal

```bash
pip install -r requirements.txt
```

## Run server

```bash
uvicorn app.main:app --reload
```