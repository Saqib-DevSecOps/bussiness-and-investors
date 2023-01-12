FROM python:3.10.2-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
WORKDIR app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]