FROM python:3.8.12-slim-buster

ENV DOCKER_RUNMODE "TRUE"

COPY src/ /cert_reminder/src/
COPY main.py /cert_reminder/main.py
COPY settings.json /cert_reminder/settings.json
COPY requirements.txt /cert_reminder/requirements.txt

WORKDIR /cert_reminder

RUN apt-get update && apt-get install --no-install-recommends -q -y cron nano
RUN pip3 install -r requirements.txt

COPY /entrypoint.sh /etc/entrypoint.sh
CMD [ "/bin/sh", "/etc/entrypoint.sh" ]