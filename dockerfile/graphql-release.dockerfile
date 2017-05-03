FROM python:3.6-alpine
MAINTAINER Thomas Rampelberg <thomasr@vapor.io>

RUN mkdir /logs
# Run the dependencies as a single layer
COPY graphql /graphql_frontend
RUN pip install -r /graphql_frontend/requirements.txt

WORKDIR /graphql_frontend
CMD python runserver.py
