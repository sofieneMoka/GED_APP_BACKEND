from flask import Blueprint, jsonify, request
from models import Direction, DirectionSchema, db


#blueprint setup
direction = Blueprint('direction',__name__)



@direction.route('/AddDirection', methods = ['POST'])
def AddDirection():
    req_Json = request.json
    name = req_Json['name']
    direction = Direction(name)
    db.session.add(direction)
    db.session.commit()
    return "1" #Add successfully



@direction.route('/UpdateDirection/<int:_id>', methods = ['PUT'])
def UpdateDirection(_id):
    req_Json = request.json
    direction = Direction.query.get(_id)
    direction.name = req_Json['name']
    
    db.session.commit()

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
    db.session.delete(direction)        
    db.session.commit()

    return '1' #direction deleted !!