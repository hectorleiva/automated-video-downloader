FROM python:3.8.5-buster

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN pip install -t vendored/ -r requirements.txt

CMD ["python", "main.py"]
