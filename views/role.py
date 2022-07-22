from flask import Blueprint, jsonify, request
from models import Role, RoleSchema, db


#blueprint setup
role = Blueprint('role',__name__)



@role.route('/AddRole', methods = ['POST'])
def AddRole():
    req_Json = request.json
    name = req_Json['name']
    idDepartement = req_Json['idDepartement']
    role = Role(name,idDepartement)
    db.session.add(role)
    db.session.commit()
    return "1" #Add successfully



@role.route('/UpdateRole/<int:_id>', methods = ['PUT'])
def UpdateRole(_id):
    req_Json = request.json
    role = Role.query.get(_id)
    role.name = req_Json['name']
    role.idDepartement = req_Json['idDepartement']
    
    db.session.commit()

    return '1' #Role updated !!



@role.route('/GetAllRole', methods = ['GET'])
def GetAllRole():
    roles = Role.query.all()
    role_schema = RoleSchema(many=True)
    output = role_schema.dump(roles)
    return jsonify({'Roles' : output})



@role.route('/GetListRoleByDepartement/<int:_id>', methods = ['GET'])
def GetListRoleByDepartement(_id):
    roles = Role.query.filter(
        Role.idDepartement == _id
    )
    role_schema = RoleSchema(many=True)
    output = role_schema.dump(roles)
    return jsonify({'Roles' : output})



@role.route('/DeleteRole/<int:_id>', methods = ['DELETE'])
def DeleteRole(_id):
    role = Role.query.get(_id)
    db.session.delete(role)        
    db.session.commit()

    return '1' #SubCategory deleted !!