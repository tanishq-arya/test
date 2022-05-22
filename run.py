from app import app
from db import db

db.init_app(app)

# Flask decorator
@app.before_first_request
def create_tables():
  db.create_all() # create all the tables unless they exist already
