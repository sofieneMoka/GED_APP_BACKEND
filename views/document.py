from models import Document, DocumentSchema, db, User, SubCategory, Category
from flask import Blueprint, jsonify, request, send_from_directory
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename


#blueprint setup
document = Blueprint('document',__name__)




@document.route('/UploadDocument/<int:_id>', methods = ['POST'])
def UploadDocument(_id):
    if request.method == 'POST':
        file = request.files['file']
        user = User.query.get(_id)
        name = request.form['name']
        Format = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        description = request.form['description']
        nameCreator = user.f_name + user.l_name
        note = request.form['note']
        tag= request.form['tag']
        status= request.form['status']
        size= request.form['size']
        creationDate = datetime.today().strftime('%Y-%m-%d')
        lastModification = datetime.today().strftime('%Y-%m-%d')
        nameModificator = user.f_name + user.l_name
        nameSubCategory = request.form['nameSubCategory']
        nameCategory = request.form['nameCategory']
        #path of the document
        path= 'uploads'+ '/' + nameCategory + '/' + nameSubCategory + '/' + name + '.' + Format
        doc = Document(name,Format,description,nameCreator,note,tag,status,path,size,creationDate,lastModification,nameModificator,nameSubCategory,nameCategory)
        #upload the document 
        file.save(os.path.join('uploads'+ '/' + nameCategory + '/' + nameSubCategory + '/'  + name + '.' + Format))
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
        print(user.f_name)
        document.lastModification = datetime.now().strftime('%Y-%m-%d')
        document.description = request.form['description']
        document.note = request.form['note']
        document.tag= request.form['tag']
        document.status= request.form['status']
        document.nameSubCategory= request.form['nameSubCategory']
        document.nameCategory= request.form['nameCategory']
        # Absolute path of a file
        old_name = document.path
        document.name = request.form['name']
        new_name = "uploads/" + document.nameCategory + "/"+ document.nameSubCategory + "/" + document.name + "." + document.Format
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


@document.route('/getDocument/<int:_idDoc>')
def getDocument(_idDoc):
    document = Document.query.get(_idDoc)
    filename=document.name+'.'+document.Format
    file = send_from_directory("uploads/"+document.nameCategory +'/'+document.nameSubCategory + '/',filename, as_attachment=True)
    return file

@document.route('/SearchDocumentWithFilters/<string:_Name>/<string:_creator>/<string:_Tags>/<string:_StartDate>/<string:_EndDate>/<string:_SubCategory>/<string:_Category>', methods= ['GET'])
def SearchDocumentWithFilters(_Name,_creator,_Tags,_StartDate,_EndDate,_SubCategory,_Category):
    if _Name == "Null":
        _Name = ""
    if _creator == "Null":
        _creator = ""
    if _Tags == "Null":
        _Tags = ""
    if _StartDate == "Null":
        _StartDate = "2001-01-01"
    if _EndDate == "Null":
        _EndDate = "2099-01-01"
    if _Category == "Null":
        _Category = ""
    if _SubCategory == "Null":
        _SubCategory = ""


    documents = Document.query.filter(
    Document.name.contains(_Name),
    Document.nameCreator.contains(_creator),
    Document.tag.contains(_Tags),
    Document.nameSubCategory.contains(_SubCategory),
    Document.nameCategory.contains(_Category),
    Document.creationDate >= _StartDate,
    Document.creationDate <= _EndDate
    )
    document_schema = DocumentSchema(many=True)
    output = document_schema.dump(documents)
    return jsonify({'Documents' : output})




@document.route('/SearchDocumentBySubCategory/<string:_SubCategory>', methods= ['GET'])
def SearchDocumentBySubCategory(_SubCategory):

    documents = Document.query.filter(
    Document.nameSubCategory.contains(_SubCategory)
    )
    document_schema = DocumentSchema(many=True)
    output = document_schema.dump(documents)
    return jsonify({'Documents' : output})






@document.route('/SaveDocument/<int:_idUser>/<int:_idDoc>', methods = ['POST'])
def SaveDocument(_idUser,_idDoc):
    if request.method == 'POST':
        user = User.query.get(_idUser)
        document = Document.query.get(_idDoc)
        file = request.files['file']
        document.lastModification = datetime.now().strftime('%Y-%m-%d')
        document.nameModificator = user.f_name + user.l_name

        #upload the document 
        file.save(os.path.join(document.path))

        db.session.commit()

        return "1" #uploaded successfully