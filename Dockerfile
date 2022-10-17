FROM python:3.10.4

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat \
    nano

WORKDIR /opt/flask_api

COPY requirements/common.txt /opt/flask_api

RUN pip install --no-cache-dir -r common.txt

COPY . /opt/flask_api/
COPY .pdbrc.py /home/
COPY database-healthy.sh /tmp/database-healthy.sh

EXPOSE 5000

ENTRYPOINT ["bash", "/tmp/database-healthy.sh"]

CMD python3 main.py