FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN adduser --system --group --shell /bin/sh auser \
 && mkdir /home/auser/bin
USER auser
RUN pip install -r requirements.txt