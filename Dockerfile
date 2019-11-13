FROM python:3

RUN mkdir /api
ADD api /api
WORKDIR api
RUN pip3 install pipenv
RUN pipenv --three
RUN pipenv install
EXPOSE 5000
