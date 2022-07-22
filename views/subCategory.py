from flask import Blueprint, jsonify, request
from models import SubCategory, SubCategorySchema, db


#blueprint setup
subCategory = Blueprint('subCategory',__name__)



@subCategory.route('/AddSubCategory', methods = ['POST'])
def AddSubCategory():
    req_Json = request.json
    name = req_Json['name']
    idCategory = req_Json['idCategory']
    subCategory = SubCategory(name,idCategory)
    db.session.add(subCategory)
    db.session.commit()
    return "1" #Add successfully



@subCategory.route('/UpdateSubCategory/<int:_id>', methods = ['PUT'])
def UpdateSubCategory(_id):
    req_Json = request.json
    subCategory = SubCategory.query.get(_id)
    subCategory.name = req_Json['name']
    subCategory.idCategory = req_Json['idCategory']
    
    db.session.commit()

    return '1' #SubCategory updated !!



@subCategory.route('/GetAllSubCategory', methods = ['GET'])
def GetAllSubCategory():
    subCategorys = SubCategory.query.all()
    subCategory_schema = SubCategorySchema(many=True)
    output = subCategory_schema.dump(subCategorys)
    return jsonify({'SubCategorys' : output})



@subCategory.route('/GetListSubCategoryByCategory/<int:_id>', methods = ['GET'])
def GetListSubCategoryByCategory(_id):
    subCategorys = SubCategory.query.filter(
        SubCategory.idCategory == _id
    )
    subCategory_schema = SubCategorySchema(many=True)
    output = subCategory_schema.dump(subCategorys)
    return jsonify({'SubCategorys' : output})



@subCategory.route('/DeleteSubCategory/<int:_id>', methods = ['DELETE'])
def DeleteSubCategory(_id):
    subCategory = SubCategory.query.get(_id)
    db.session.delete(subCategory)        
    db.session.commit()

    return '1' #SubCategory deleted !!