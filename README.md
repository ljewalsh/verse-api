# Verse Api
A basic api for the verse banking app

## Quick Start
- Download or clone repo
- Set environment variables:
```
ENV FLASK_ENV development
ENV DATABASE_URL postgres://{username}:{database}@{server}:{port}/{database}
ENV JWT_SECRET_KEY {your_secret_key}
```
- Run `docker-compose up` 
- The api-server should now be available at http://127.0.0.1:5000
