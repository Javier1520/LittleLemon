FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY . /code/
RUN pip install pipenv \
    && pipenv install --system --deploy

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]