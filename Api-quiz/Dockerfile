FROM python:3.9
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get install -y mariadb-client
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["python3", "main.py"]
