FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 80
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2", "--timeout-keep-alive", "90"]
