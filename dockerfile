FROM python:3.12.4
WORKDIR /qbot
COPY . /qbot
CMD ["python", "main.py"]
