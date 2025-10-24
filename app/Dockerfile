FROM python:3.12-slim

# container working directory, application root
WORKDIR /code

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port",  "80"]