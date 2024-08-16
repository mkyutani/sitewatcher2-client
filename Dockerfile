#
# Install:
#
#   docker build . --tag sw2:latest
#
# Command sample:
#
#   # Test the connection to the server
#   docker run --env SW2_SERVER=https://sw2server:port --rm sw2
#
#   # (sw2 server on docker host network)
#   docker run --net=host --rm sw2
#
#   # List directories
#   docker run --env SW2_SERVER=https://sw2server:port --rm sw2 d list
#
FROM python:3.12-slim-bookworm
WORKDIR /app
COPY . /app
RUN pip install .

ENV SW2_SERVER=$SW2_SERVER
ENTRYPOINT ["sw2"]
CMD ["ping"]