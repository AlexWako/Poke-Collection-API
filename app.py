from dotenv import load_dotenv
from main import create_app
from models import db

load_dotenv()
app = create_app()
with app.app_context():
    db.create_all() 
app.run(debug = False)

