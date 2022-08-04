from flask import Blueprint, jsonify, request
from models import Departement, DepartementSchema, Direction, Role, db


#blueprint setup
departement = Blueprint('departement',__name__)



@departement.route('/AddDepartement', methods = ['POST'])
def AddDepartement():
    req_Json = request.json
    name = req_Json['name']
    nameDirection= req_Json['nameDirection']
    direction = Direction.query.filter_by(name=nameDirection).first()
    idDirection = direction.id
    departement = Departement(name,idDirection,nameDirection)
    try:
        db.session.add(departement)
        db.session.commit()
    except Exception:
        return "0" #Name already used
        
    return "1" #Add successfully



@departement.route('/UpdateDepartement/<int:_id>', methods = ['PUT'])
def UpdateDepartement(_id):
    req_Json = request.json
    departement = Departement.query.get(_id)
    roles = Role.query.filter(
    Role.nameDepartement==departement.name
    )
    departement.name = req_Json['name']
    departement.nameDirection = req_Json['nameDirection']
    direction = Direction.query.filter_by(name=departement.nameDirection).first()
    departement.idDirection = direction.id
    try:
        for i in roles:
            i.nameDepartement = departement.name
            i.idDepartement = departement.id
        db.session.commit()
    except Exception:
        return "0" #Name already used
    return '1' #departement updated !!



@departement.route('/GetAllDepartement', methods = ['GET'])
def GetAllDepartement():
    departements = Departement.query.all()
    departement_schema = DepartementSchema(many=True)
    output = departement_schema.dump(departements)
    return jsonify({'Departements' : output})



@departement.route('/GetListDepartementByDirection/<string:_DirectionName>', methods = ['GET'])
def GetListDepartementByDirection(_DirectionName):
    departements = Departement.query.filter(
        Departement.nameDirection == _DirectionName
    )
    departement_schema = DepartementSchema(many=True)
    output = departement_schema.dump(departements)
    return jsonify({'Departements' : output})



@departement.route('/DeleteDepartement/<int:_id>', methods = ['DELETE'])
def DeleteDepartement(_id):
    departement = Departement.query.get(_id)
    roles = Role.query.filter(
    Role.nameDepartement==departement.name
    )
    x=0
    for i in roles : 
        x = x+1
    if x==0:
        db.session.delete(departement)        
        db.session.commit()
        return '1' #departement deleted !!
    else :
        return '0' #departement containes roles