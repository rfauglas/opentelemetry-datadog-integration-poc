FROM python:3.9-buster

# Inject github credentials in order to install private github package
# ARG GITHUB_USER
# ARG GITHUB_TOKEN
# ARG ENVCONSUL_VERSION=0.13.2
RUN ln -snf /bin/bash /bin/sh

# Set python exec to python 3.9, else cron will call python2.7
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 1

RUN \
    apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install --assume-yes apt-utils \
    && apt-get --yes install \

        python3-cffi \
        python3-lxml \
        vim 

RUN \
    pip install --upgrade pip \
    && pip install -U setuptools==66.0.0 \
    && pip install -U pytest
COPY requirements.txt requirements.txt     
RUN pip3 install -r requirements.txt

CMD ["bash"]
