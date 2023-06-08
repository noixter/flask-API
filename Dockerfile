FROM python:3.9

WORKDIR /opt/flask_api

COPY requirements.txt /opt/flask_api

RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/flask_api/

EXPOSE 5000

CMD ["python3", "main.py"]
