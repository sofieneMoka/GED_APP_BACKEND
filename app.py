from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from models import db
from views.user import user,bcrypt,jwt,mail
from views.document import document
from views.category import category
from views.subCategory import subCategory
from views.role import role
from views.departement import departement
from views.direction import direction

app = Flask(__name__)

app.config.from_pyfile("app.cfg")

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
mail.init_app(app)
migrate = Migrate(app,db)

app.register_blueprint(user)
app.register_blueprint(document)
app.register_blueprint(category)
app.register_blueprint(subCategory)
app.register_blueprint(role)
app.register_blueprint(departement)
app.register_blueprint(direction)


#ENABLE CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# if __name__ == "__main__" : 
#     app.run(debug=True)
