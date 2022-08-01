from models import Document, DocumentSchema, db, User, SubCategory, Category
from flask import Blueprint, jsonify, request
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename


#blueprint setup
document = Blueprint('document',__name__)



@document.route('/UploadDocument/<int:_id>', methods = ['POST'])
def UploadDocument(_id):
    if request.method == 'POST':
        user = User.query.get(_id)
        file = request.files['file']
        name = request.form['name']
        file.seek(0, os.SEEK_END)
        Format = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        description = request.form['description']
        nameCreator = user.f_name + user.l_name
        note = request.form['note']
        tag= request.form['tag']
        status= request.form['status']
        size = file.tell()
        creationDate = datetime.today().strftime('%Y-%m-%d')
        lastModification = datetime.today().strftime('%Y-%m-%d')
        nameModificator = user.f_name + user.l_name
        nameSubCategory = request.form['nameSubCategory']
        #get the SubCategory and the Category
        SubCategory1 = SubCategory.query.filter_by(name=nameSubCategory).first()
        Category1 = Category.query.get(SubCategory1.idCategory)
        nameCategory = Category1.name
        #path of the document
        path= 'uploads'+ '/' + Category1.name + '/' + SubCategory1.name + '/' + name + '.' + Format
        doc = Document(name,Format,description,nameCreator,note,tag,status,path,size,creationDate,lastModification,nameModificator,nameSubCategory,nameCategory)
        #upload the document 
        file.save(os.path.join('uploads'+ '/' + Category1.name + '/' + SubCategory1.name + '/'  + name + '.' + Format))
        try:
            db.session.add(doc)
            db.session.commit()
        except Exception:
            return "0" #Name already used

        return "1" #uploaded successfully

@document.route('/UpdateDocument/<int:_idUser>/<int:_idDoc>', methods = ['PUT'])
def UpdateDocument(_idDoc,_idUser):
    if request.method == 'PUT':
        document = Document.query.get(_idDoc)
        user = User.query.get(_idUser)

        document.nameModificator = user.f_name + user.l_name
        document.lastModification = datetime.now().strftime('%Y-%m-%d')
        document.description = request.form['description']
        document.note = request.form['note']
        document.tag= request.form['tag']
        document.status= request.form['status']
        document.nameSubCategory= request.form['nameSubCategory']
        #get the SubCategory and the Category
        SubCategory1 = SubCategory.query.filter_by(name=document.nameSubCategory).first()
        Category1 = Category.query.get(SubCategory1.idCategory)
        # Absolute path of a file
        old_name = document.path
        document.name = request.form['name']
        new_name = "uploads/" + Category1.name + "/"+ SubCategory1.name + "/" + document.name + "." + document.Format
        document.path = new_name
        # Renaming the file
        os.rename(old_name, new_name)

        db.session.commit()
        try:
            db.session.commit()
        except Exception:
            return "0" #Name already used

        return "1" #uploaded successfully



@document.route('/DeleteDocument/<int:_id>', methods = ['DELETE'])
def DeleteDocument(_id):
    document = Document.query.get(_id)
    os.remove(document.path)
    db.session.delete(document)        
    db.session.commit()
    return "deleted"



@document.route('/GetDocumentDetails/<int:_id>', methods= ['GET'])
def GetDocumentDetails(_id):
    document = Document.query.get(_id)
    print(DocumentSchema().dump(document))
    return DocumentSchema().dump(document)



@document.route('/GetAllDocument', methods= ['GET'])
def GetAllDocument():
    documents = Document.query.all()
    document_schema = DocumentSchema(many=True)
    output = document_schema.dump(documents)
    return jsonify({'Documents' : output})



@document.route('/SearchDocumentWithFilters/<string:_Name>/<string:_creator>/<string:_Tags>/<string:_StartDate>/<string:_EndDate>/<string:_SubCategory>/<string:_Category>', methods= ['GET'])
def SearchDocumentByName(_Name,_creator,_Tags,_StartDate,_EndDate,_SubCategory,_Category):
    if _Name == "Null":
        _Name = ""
    if _creator == "Null":
        _creator = ""
    if _Tags == "Null":
        _Tags = ""
    if _StartDate == "Null":
        _StartDate = ""
    if _EndDate == "Null":
        _EndDate = ""
    if _Category == "Null":
        _Category = ""
    if _SubCategory == "Null":
        _SubCategory = ""



    SubCategory1 = SubCategory.query.filter_by(name = _SubCategory).first()
    Category1 = Category.query.filter_by(name = _Category).first()

    documents = Document.query.filter(
    Document.name.contains(_Name),
    Document.creator.contains(_creator),
    Document.tag.contains(_Tags),
    Document.idSubCategory == SubCategory1.id,
    Document.idCategory == Category1.id,
    Document.creationDate >= _StartDate,
    Document.creationDate <= _EndDate
    )
    document_schema = DocumentSchema(many=True)
    output = document_schema.dump(documents)
    return jsonify({'Documents' : output})
