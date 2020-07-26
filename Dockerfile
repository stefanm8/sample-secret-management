FROM python:3.7-alpine

ARG DB_USERNAME=default
ARG DB_PASSWORD=default
ENV DB_USERNAME=$DB_USERNAME
ENV DB_PASSWORD=$DB_PASSWORD

COPY . . 

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]

