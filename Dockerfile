FROM python:3.11-slim

# Use a imagem oficial do Python 3.11 em sua versão slim
FROM python:3.11-slim

# Defina uma variável de ambiente para garantir que a saída python seja enviada diretamente para o terminal sem buffering
ENV PYTHONUNBUFFERED=1

# Defina o diretório de trabalho dentro do container
WORKDIR /code

# Copie o Pipfile e Pipfile.lock (se estiver usando Pipenv) ou requirements.txt para o diretório de trabalho

COPY ./requirements.txt /code/requirements.txt

# Instale as dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copie o restante do código do projeto para o diretório de trabalho
COPY ./app /code/app

# Expõe a porta em que sua aplicação irá rodar. Por padrão, FastAPI usa a porta 8000.
EXPOSE 8000

# Comando para rodar a aplicação. Ajuste conforme a forma que você roda sua aplicação.
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]