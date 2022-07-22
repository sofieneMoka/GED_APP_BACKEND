from flask import Blueprint, jsonify, request
from models import Departement, Direction, DirectionSchema, db


#blueprint setup
direction = Blueprint('direction',__name__)



@direction.route('/AddDirection', methods = ['POST'])
def AddDirection():
    req_Json = request.json
    name = req_Json['name']
    direction = Direction(name)
    try:
        db.session.add(direction)
        db.session.commit()
    except Exception:
        return "0" #Name already used
        
    return "1" #Add successfully



@direction.route('/UpdateDirection/<int:_id>', methods = ['PUT'])
def UpdateDirection(_id):
    req_Json = request.json
    direction = Direction.query.get(_id)
    departements = Departement.query.filter(
    Departement.nameDirection==direction.name
    )
    direction.name = req_Json['name']
    try:
        for i in departements:
            i.nameDirection = direction.name
        db.session.commit()
    except Exception:
        return "0" #Name already used

    return '1' #direction updated !!



@direction.route('/GetAllDirection', methods = ['GET'])
def GetAllDirection():
    directions = Direction.query.all()
    direction_schema = DirectionSchema(many=True)
    output = direction_schema.dump(directions)
    return jsonify({'Directions' : output})




@direction.route('/DeleteDirection/<int:_id>', methods = ['DELETE'])
def DeleteDirection(_id):
    direction = Direction.query.get(_id)
    departements = Departement.query.filter(
    Departement.nameDirection==direction.name
    )
    x=0
    for i in departements : 
        x = x+1
    if x==0:
        db.session.delete(direction)        
        db.session.commit()
        return '1' #direction deleted !!
    else :
        return '0' #direction containes roles