FROM python:3.7.3-slim

RUN apt-get update && \
    apt-get install -y libffi-dev libssl-dev python-dev python3-pip

RUN apt-get install -y git
RUN pip3 install git+https://github.com/aaroncox/python-muse.git
RUN pip3 install pymongo apscheduler

COPY . /src

CMD ["python", "/src/witnesses.py"]
