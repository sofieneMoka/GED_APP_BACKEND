import os
from flask import Blueprint, jsonify, request
from models import Category, Document, SubCategory, SubCategorySchema, db


#blueprint setup
subCategory = Blueprint('subCategory',__name__)



@subCategory.route('/AddSubCategory', methods = ['POST'])
def AddSubCategory():
    req_Json = request.json
    name = req_Json['name']
    nameCategory= req_Json['nameCategory']
    category = Category.query.filter_by(name=nameCategory).first()
    idCategory = category.id
    subCategory = SubCategory(name,idCategory,nameCategory)
    try:
        db.session.add(subCategory)
        db.session.commit()
    except Exception:
        return "0" #Name already used
    #Create folder    
    path = os.path.join('uploads/'+nameCategory, name)
    os.mkdir(path)
    return "1" #Add successfully



@subCategory.route('/UpdateSubCategory/<int:_id>', methods = ['PUT'])
def UpdateSubCategory(_id):
    req_Json = request.json
    subCategory = SubCategory.query.get(_id)
    src_path = 'uploads/'+subCategory.nameCategory + '/' + subCategory.name

    documents = Document.query.filter(
    Document.nameSubCategory ==subCategory.name
    )

    subCategory.name = req_Json['name']
    subCategory.nameCategory= req_Json['nameCategory']

    for i in documents:
        i.nameSubCategory = subCategory.name

    try:
        category = Category.query.filter_by(name=subCategory.nameCategory).first()
        subCategory.idCategory = category.id
        db.session.commit()
        os.rename(src_path,'uploads/'+subCategory.nameCategory + '/' + subCategory.name)
    except Exception:
        return "0" #Name already used

    return '1' #SubCategory updated !!



@subCategory.route('/GetAllSubCategory', methods = ['GET'])
def GetAllSubCategory():
    subCategorys = SubCategory.query.all()
    subCategory_schema = SubCategorySchema(many=True)
    output = subCategory_schema.dump(subCategorys)
    return jsonify({'SubCategories' : output})



@subCategory.route('/GetListSubCategoryByCategory/<string:_nameCategory>', methods = ['GET'])
def GetListSubCategoryByCategory(_nameCategory):
    subCategorys = SubCategory.query.filter(
        SubCategory.nameCategory == _nameCategory
    )
    subCategory_schema = SubCategorySchema(many=True)
    output = subCategory_schema.dump(subCategorys)
    return jsonify({'SubCategorys' : output})



@subCategory.route('/DeleteSubCategory/<int:_id>', methods = ['DELETE'])
def DeleteSubCategory(_id):
    subCategory = SubCategory.query.get(_id)
    try:
        os.rmdir('uploads/'+subCategory.nameCategory+'/'+subCategory.name)
    except Exception:
        return "0" #Folder is not Empty
    db.session.delete(subCategory)        
    db.session.commit()

    return '1' #SubCategory deleted !!