FROM python:3

RUN mkdir /api
ADD api /api
WORKDIR api
RUN pip3 install pipenv
RUN pipenv --three
RUN pipenv install

ENV FLASK_ENV development
ENV DATABASE_URL postgres://verse_developer:iamaversedeveloper@localhost:5432/verse
ENV JWT_SECRET_KEY hhgaghhgsdhdhdd

CMD ["pipenv", "run", "python", "run.py"]
