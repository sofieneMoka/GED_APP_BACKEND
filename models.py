from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

db = SQLAlchemy()
ma = Marshmallow()

#################################### User Model ##################################
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(200),nullable=False)
    l_name = db.Column(db.String(200),nullable=False)
    role = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200), unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    status=db.Column(db.String(200),default="Active")
    activate_acc = db.Column(db.Integer(),default=0)
    idRole = db.Column(db.Integer, db.ForeignKey('Role.id'))



    def __init__(self, f_name, l_name,role, email, password, activate_acc):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.role = role
        self.password = password
        self.activate_acc = activate_acc
        

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

#################################### Document Model ##################################
class Document(db.Model):
    __tablename__ = 'Document'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),unique=True,nullable=False)
    Format = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(200),nullable=False)
    creator = db.Column(db.String(200))
    note = db.Column(db.String(200),nullable=False)
    tag=db.Column(db.String(200))
    status=db.Column(db.String(200))
    path=db.Column(db.String(200))
    size = db.Column(db.Float(),nullable=False)
    creationDate = db.Column(db.DateTime,nullable=False)
    lastModification = db.Column(db.DateTime,nullable=False)
    modificatorId = db.Column(db.Integer)
    creatorId = db.Column(db.Integer)
    idSubCategory = db.Column(db.Integer, db.ForeignKey('SubCategory.id'))
    idCategory = db.Column(db.Integer)



    def __init__(self, name, Format,description, creator, note, tag, status, path, size, creationDate, lastModification, modificatorId, creatorId, idSubCategory, idCategory):
        self.name = name
        self.Format = Format
        self.description = description
        self.creator = creator
        self.note = note
        self.tag = tag
        self.status = status
        self.path = path
        self.size = size
        self.creationDate = creationDate
        self.lastModification = lastModification
        self.modificatorId = modificatorId
        self.creatorId = creatorId
        self.idSubCategory = idSubCategory
        self.idCategory = idCategory
        

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        load_instance = True

#################################### SubCategory Model ##################################
class SubCategory(db.Model):
    __tablename__ = 'SubCategory'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),unique=True,nullable=False)
    idCategory = db.Column(db.Integer, db.ForeignKey('Category.id'))
    

    def __init__(self, name, idCategory):
        self.name = name
        self.idCategory = idCategory
        

class SubCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubCategory
        load_instance = True

#################################### Category Model ##################################
class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),unique=True,nullable=False)


    def __init__(self, name):
        self.name = name
        

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

#################################### Access Model ##################################
class Access(db.Model):
    __tablename__ = 'Access'
    id = db.Column(db.Integer, primary_key = True)
    idDocument = db.Column(db.Integer, db.ForeignKey('Document.id'))
    idRole = db.Column(db.Integer, db.ForeignKey('Role.id'))
    read = db.Column(db.Integer,nullable=False)
    write = db.Column(db.Integer,nullable=False)
    update = db.Column(db.Integer,nullable=False)


    def __init__(self, name, read, write, update):
        self.name = name
        self.read = read
        self.write = write
        self.update = update
        

class AccessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Access
        load_instance = True


#################################### Role Model ##################################
class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key = True)
    idDepartement = db.Column(db.Integer, db.ForeignKey('Departement.id'))
    name = db.Column(db.String(200),unique=True,nullable=False)



    def __init__(self, name,idDepartement):
        self.name = name
        self.idDepartement = idDepartement
        

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True


#################################### Departement Model ##################################
class Departement(db.Model):
    __tablename__ = 'Departement'
    id = db.Column(db.Integer, primary_key = True)
    idDirection = db.Column(db.Integer, db.ForeignKey('Direction.id'))
    name = db.Column(db.String(200),unique=True,nullable=False)



    def __init__(self, name, idDirection):
        self.name = name
        self.idDirection = idDirection
        

class DepartementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Departement
        load_instance = True


#################################### Direction Model ##################################
class Direction(db.Model):
    __tablename__ = 'Direction'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),unique=True,nullable=False)



    def __init__(self, name):
        self.name = name
        

class DirectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Direction
        load_instance = True