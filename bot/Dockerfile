FROM python:3.13
RUN pip install poetry

COPY . /app
WORKDIR /app

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "app.py"]