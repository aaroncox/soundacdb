FROM python:3.3.6-slim

RUN apt-get update && \
    apt-get install -y libffi-dev libssl-dev python-dev python3-pip

RUN apt-get install -y git
RUN pip3 install pymongo
RUN pip3 install git+https://github.com/aaroncox/python-muse.git#

COPY . /src

CMD ["python", "/src/sync.py"]
