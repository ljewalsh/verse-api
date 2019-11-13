# Verse Api
A basic banking api built with postgres, Flask, and Flask-SQLAlchemy

Api docs can be found here: https://documenter.getpostman.com/view/7103969/SW7UaqEm?version=latestl

## Quick Start
- Download or clone repo
- Add environment variables to .env file at root of project (POSTGRES_HOST must be set to db):
```
POSTGRES_USER=test
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=example
JWT_SECRET_KEY=example
```
- Run `docker-compose build` 
- Run `docker-compose up -d`
- The api-server should now be available at http://127.0.0.1:5000

## Running Tests
- Setup a local testing db called `verse-testing` with the user `verse_developer` and password `iamaversedeveloper`
- Install pipenv (https://pypi.org/project/pipenv/)
- From with api directory, run `pipenv install`
- Run `pipenv shell` to enter virtual environment
- Run `JWT_SECRET_KEY=testing pytest` to test code

## Authentication
All requests (except user create and login requests) require a jwt-token in the header. The jwt-token is available in two responses:

1. On user create (`/api/v1/users/`)
2. On user login (`/api/v1/users/login`)

Header should be formatted as follows:
```
{ 'api-token': 'your_jwt_token' }
```
