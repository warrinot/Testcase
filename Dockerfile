FROM python:3.8.3-alpine


WORKDIR /usr/src/testcase


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev libffi-dev musl-dev make 

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/usr/src/testcase/entrypoint.sh"]