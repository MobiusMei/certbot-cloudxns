FROM quay.io/letsencrypt/letsencrypt

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip

RUN pip install --no-cache-dir restclient https://github.com/CloudXNS/CloudXNS-API-SDK-Python/archive/master.zip

ADD auth.py /usr/bin/auth.py
ADD cleanup.py /usr/bin/cleanup.py
