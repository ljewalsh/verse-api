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
docker-compile exec api pipenv run pytest
```

## Authentication
All requests but the user create request require a jwt-token in the header. The jwt-token is available in two responses:

1. On user create (`/api/v1/users/`)
2. On user login (`/api/v1/users/login`)

Header should be formatted as follows:
```
{ 'api-token': 'your_jwt_token' }
```
