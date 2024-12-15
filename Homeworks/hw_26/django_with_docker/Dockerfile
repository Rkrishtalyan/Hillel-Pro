FROM python:3.10-slim

WORKDIR /django_app

COPY requirements.txt /django_app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /django_app/

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]