FROM python:3.13-slim-bookworm

WORKDIR /app

EXPOSE 8000

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
