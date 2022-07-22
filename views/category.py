from flask import Blueprint, jsonify, request
from models import Category, CategorySchema, db


#blueprint setup
category = Blueprint('category',__name__)



@category.route('/AddCategory', methods = ['POST'])
def AddCategory():
    req_Json = request.json
    name = req_Json['name']
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return "1" #Add successfully



@category.route('/UpdateCategory/<int:_id>', methods = ['PUT'])
def UpdateCategory(_id):
    req_Json = request.json
    category = Category.query.get(_id)
    category.name = req_Json['name']
    
    db.session.commit()

    return '1' #category updated !!



@category.route('/GetAllCategories', methods = ['GET'])
def GetAllCategories():
    categorys = Category.query.all()
    category_schema = CategorySchema(many=True)
    output = category_schema.dump(categorys)
    return jsonify({'Categories' : output})



@category.route('/DeleteCategory/<int:_id>', methods = ['DELETE'])
def DeleteCategory(_id):
    category = Category.query.get(_id)
    db.session.delete(category)        
    db.session.commit()

    return '1' #category deleted !!