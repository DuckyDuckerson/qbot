FROM python:3.12.4
WORKDIR /app
COPY . /app
CMD ["python", "main.py"]
