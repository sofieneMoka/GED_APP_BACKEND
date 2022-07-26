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
    nameCreator = db.Column(db.String(200))
    note = db.Column(db.String(200),nullable=False)
    tag=db.Column(db.String(200))
    status=db.Column(db.String(200))
    path=db.Column(db.String(200))
    size = db.Column(db.Float(),nullable=False)
    creationDate = db.Column(db.DateTime,nullable=False)
    lastModification = db.Column(db.DateTime,nullable=False)
    nameModificator = db.Column(db.String(200))
    nameSubCategory = db.Column(db.String(200))
    nameCategory = db.Column(db.String(200))



    def __init__(self, name, Format,description, nameCreator, note, tag, status, path, size, creationDate, lastModification, modificatorId, nameSubCategory, nameCategory):
        self.name = name
        self.Format = Format
        self.description = description
        self.nameCreator = nameCreator
        self.note = note
        self.tag = tag
        self.status = status
        self.path = path
        self.size = size
        self.creationDate = creationDate
        self.lastModification = lastModification
        self.modificatorId = modificatorId
        self.nameSubCategory = nameSubCategory
        self.nameCategory = nameCategory
        

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
    nameCategory = db.Column(db.String(200),nullable=False)
    

    def __init__(self, name, idCategory, nameCategory):
        self.name = name
        self.idCategory = idCategory
        self.nameCategory = nameCategory
        

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
    nameDepartement = db.Column(db.String(200),nullable=False)



    def __init__(self, name,idDepartement, nameDepartement):
        self.name = name
        self.idDepartement = idDepartement
        self.nameDepartement = nameDepartement
        

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
    nameDirection = db.Column(db.String(200),nullable=False)



    def __init__(self, name, idDirection, nameDirection):
        self.name = name
        self.nameDirection = nameDirection
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