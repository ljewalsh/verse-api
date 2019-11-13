import os
from src.config import DATABASE_CONNECTION_URI
from src.app import create_app
from src.models import db

app = create_app('verse_api')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.create_all()

if __name__ == '__main__':
  app.run(host='0.0.0.0')
