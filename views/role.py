from flask import Blueprint, jsonify, request
from models import Departement, Role, RoleSchema, User, db


#blueprint setup
role = Blueprint('role',__name__)



@role.route('/AddRole', methods = ['POST'])
def AddRole():
    req_Json = request.json
    name = req_Json['name']
    nameDepartement= req_Json['nameDepartement']
    departement = Departement.query.filter_by(name=nameDepartement).first()
    idDepartement = departement.id
    role = Role(name,idDepartement,nameDepartement)
    try:
        db.session.add(role)
        db.session.commit()
    except Exception:
        return "0" #Name already used
        
    return "1" #Add successfully



@role.route('/UpdateRole/<int:_id>', methods = ['PUT'])
def UpdateRole(_id):
    req_Json = request.json
    role = Role.query.get(_id)
    users = User.query.filter_by(role = role.name)
    role.name = req_Json['name']
    role.nameDepartement= req_Json['nameDepartement']
    try:
        for u in users:
            u.role = role.name
        departement = Departement.query.filter_by(name=role.nameDepartement).first()
        role.idDepartement = departement.id
        db.session.commit()
    except Exception:
        return "0" #Name already used
    return '1' #Role updated !!



@role.route('/GetAllRole', methods = ['GET'])
def GetAllRole():
    roles = Role.query.all()
    role_schema = RoleSchema(many=True)
    output = role_schema.dump(roles)
    return jsonify({'Roles' : output})



@role.route('/GetListRoleByDepartement/<string:_DepartementName>', methods = ['GET'])
def GetListRoleByDepartement(_DepartementName):
    roles = Role.query.filter(
        Role.nameDepartement == _DepartementName
    )
    role_schema = RoleSchema(many=True)
    output = role_schema.dump(roles)
    return jsonify({'Roles' : output})



@role.route('/DeleteRole/<int:_id>', methods = ['DELETE'])
def DeleteRole(_id):
    role = Role.query.get(_id)
    users = User.query.filter_by(role = role.name)
    for u in users:
        u.role = "Null"
    db.session.delete(role)        
    db.session.commit()

    return '1' #SubCategory deleted !!