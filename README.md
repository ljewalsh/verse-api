# Verse Api
A basic api for the verse banking app

## Quick Start
- Download or clone repo
- Set local environment variables:
```
export FLASK_ENV=development
export DATABASE_URL=postgres://{username}:{database}@{server}:{port}/{database}
export JWT_SECRET_KEY={your_secret_key}
```
- Run `docker-compose up` 
- The api-server should now be available at http://127.0.0.1:5000

## Running Tests
Once the server is running, run tests in another terminal using:
```
docker-computer exec api pipenv run pytest
```
