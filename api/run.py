import os

from src.app import create_app

app = create_app('verse_api')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
