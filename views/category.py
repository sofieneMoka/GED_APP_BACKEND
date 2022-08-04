import os
from flask import Blueprint, jsonify, request
from models import Category, CategorySchema, SubCategory, db


#blueprint setup
category = Blueprint('category',__name__)



@category.route('/AddCategory', methods = ['POST'])
def AddCategory():
    req_Json = request.json
    name = req_Json['name']
    category = Category(name)
    try:
        db.session.add(category)
        db.session.commit()
    except Exception:
        return "0" #Name already used
    #Create folder    
    path = os.path.join('uploads/', name)
    os.mkdir(path)
    return "1" #Add successfully



@category.route('/UpdateCategory/<int:_id>', methods = ['PUT'])
def UpdateCategory(_id):
    req_Json = request.json
    category = Category.query.get(_id)
    subcategories = SubCategory.query.filter(
    SubCategory.nameCategory ==category.name
    )
    src_path = 'uploads/'+category.name
    category.name = req_Json['name']
    for i in subcategories:
        i.nameCategory = category.name
    try:
        db.session.commit()
        os.rename(src_path,'uploads/'+category.name)
    except Exception:
        return "0" #Name already used


    return '1' #category updated !!



@category.route('/GetAllCategories', methods = ['GET'])
def GetAllCategories():
    categorys = Category.query.all()
    category_schema = CategorySchema(many=True)
    output = category_schema.dump(categorys)
    return jsonify({'Categories' : output})



@category.route('/SearchCategoryByName/<string:_NameCategory>', methods = ['GET'])
def SearchCategoryByName(_NameCategory):
    if _NameCategory == "Null":
        _NameCategory = ""
    categorys = Category.query.filter(
        Category.name.contains(_NameCategory)
    )
    category_schema = CategorySchema(many=True)
    output = category_schema.dump(categorys)
    return jsonify({'Categories' : output})



@category.route('/DeleteCategory/<int:_id>', methods = ['DELETE'])
def DeleteCategory(_id):
    category = Category.query.get(_id)
    try:
        os.rmdir('uploads/'+category.name)
    except Exception:
        return "0" #Folder is not Empty
    db.session.delete(category)        
    db.session.commit()

    return '1' #category deleted !!