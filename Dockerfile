FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
COPY credentials.json .
COPY static static

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
