FROM python:3

WORKDIR /usr/src/app

COPY app.py requirements.txt start.sh ./
COPY templates ./templates
COPY certs ./certs 

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x start.sh

CMD ["/bin/bash", "start.sh"]
