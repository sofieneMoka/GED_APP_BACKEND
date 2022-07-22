from flask import Blueprint, jsonify, request
from models import Departement, DepartementSchema, db


#blueprint setup
departement = Blueprint('departement',__name__)



@departement.route('/AddDepartement', methods = ['POST'])
def AddDepartement():
    req_Json = request.json
    name = req_Json['name']
    idDirection = req_Json['idDirection']
    departement = Departement(name,idDirection)
    db.session.add(departement)
    db.session.commit()
    return "1" #Add successfully



@departement.route('/UpdateDepartement/<int:_id>', methods = ['PUT'])
def UpdateDepartement(_id):
    req_Json = request.json
    departement = Departement.query.get(_id)
    departement.name = req_Json['name']
    departement.idDirection = req_Json['idDirection']
    
    db.session.commit()

    return '1' #departement updated !!



@departement.route('/GetAllDepartement', methods = ['GET'])
def GetAllDepartement():
    departements = Departement.query.all()
    departement_schema = DepartementSchema(many=True)
    output = departement_schema.dump(departements)
    return jsonify({'Departements' : output})



@departement.route('/GetListDepartementByDirection/<int:_id>', methods = ['GET'])
def GetListDepartementByDirection(_id):
    departements = Departement.query.filter(
        Departement.idDirection == _id
    )
    departement_schema = DepartementSchema(many=True)
    output = departement_schema.dump(departements)
    return jsonify({'Departements' : output})



@departement.route('/DeleteDepartement/<int:_id>', methods = ['DELETE'])
def DeleteDepartement(_id):
    departement = Departement.query.get(_id)
    db.session.delete(departement)        
    db.session.commit()

    return '1' #departement deleted !!