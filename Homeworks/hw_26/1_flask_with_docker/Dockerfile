FROM python:3.10-slim

WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app/ .

CMD ["python", "flask_app.py"]