# getting base image
FROM python:latest

RUN pip install -r Gin-and-Tensor/requirements.txt

CMD ["echo", "hello from docker file"]
