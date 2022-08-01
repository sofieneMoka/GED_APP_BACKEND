from models import Document, User, UserSchema, db
from flask import Blueprint, jsonify, request
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_refresh_token, get_jwt_identity, jwt_required, create_access_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from random import randint
from flask_mail import Mail,Message

#blueprint setup
user = Blueprint('user',__name__)

otp=randint(000000,999999)

bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()


@user.route('/Registration', methods = ['POST'])
def UserRegistration():
    if request.method == 'POST':
        req_Json = request.json
        f_name = req_Json['f_name']
        l_name = req_Json['l_name']
        role = req_Json['role']
        email = req_Json['email']
        activate_acc = 0
        if User.query.filter_by(email=email).first():
            return "0" #email already exist
        if req_Json['password'] != req_Json['Conf_password'] :
            return "1" #password != confirm_password
        else:
            password=bcrypt.generate_password_hash(req_Json['password'])

            user = User(f_name, l_name, role, email, password, activate_acc)
            access_token = create_access_token(identity = email,additional_claims=UserSchema().dump(user),expires_delta=timedelta(days=1))
            refresh_token = create_refresh_token(identity = email,additional_claims=UserSchema().dump(user),expires_delta=timedelta(days=1))
            response = jsonify(message="user added, pleas activate your email, token", access_token=access_token)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            db.session.add(user)
            db.session.commit()
            return access_token



@user.route('/AllUsers', methods = ['GET'])
def FindAllUser():
    if request.method == 'GET':
        users = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        return jsonify({'Users' : output})




@user.route('/SearchUserWithFilter/<string:_FirstName>/<string:_LastName>/<string:_Role>/<string:_Status>/<string:_Activate_acc>', methods= ['GET'])
def SearchUserWithFilter(_FirstName,_LastName,_Role,_Status,_Activate_acc):
    if _FirstName == "Null":
        _FirstName = ""
    if _LastName == "Null":
        _LastName = ""
    if _Role == "Null":
        _Role = ""
    if _Status == "Null":
        _Status = ""
    if _Activate_acc == "Null":
        _Activate_acc = ""

    users = User.query.filter(
    User.f_name.contains(_FirstName),
    User.l_name.contains(_LastName),
    User.role.contains(_Role),
    User.status.contains(_Status),
    User.activate_acc.contains(_Activate_acc)
    )
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    return jsonify({'Users' : output})




@user.route('/Update/<int:_id>', methods = ['PUT'])
def Update(_id):
    if request.method == 'PUT':
        req_Json = request.json
        user = User.query.get(_id)
        
        documents1 = Document.query.filter(
        Document.nameModificator == user.f_name + user.l_name
        )

        documents = Document.query.filter(
        Document.nameCreator == user.f_name + user.l_name
        )
        user.f_name = req_Json['f_name']
        user.l_name = req_Json['l_name']
        user.role = req_Json['role']
        user.status = req_Json['status']

        for i in documents1:
            i.nameModificator = user.f_name + user.l_name

        for i in documents:
            i.nameCreator = user.f_name + user.l_name

        db.session.commit()

        return '1' #user updated !!



@user.route('/Delete/<int:_id>', methods = ['DELETE'])
def Delete(_id):
    if request.method == 'DELETE':
        user = User.query.get(_id)
        db.session.delete(user)        
        db.session.commit()

        return '1' #user deleted !!





@user.route('/Login', methods = ['POST'])
def Login():
    if request.method == 'POST':
        req_Json = request.json
        email = req_Json['email']
        password = req_Json['password']
        if email == "admin@admin" and password == "admin":
            return "2" #admin access
        user = User.query.filter_by(email=email).first()
        if user == None:
            return "0" #user n existe pas
        else:
            if bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity = email,additional_claims=UserSchema().dump(user),expires_delta= timedelta(days=1))
                refresh_token = create_refresh_token(identity = email,additional_claims=UserSchema().dump(user),expires_delta=timedelta(days=1))
                response = jsonify(message="Login Succeeded! account already activated", access_token=access_token)
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                print(access_token)
                return access_token
            else:
                return "1" #mdp incorrecte



@user.route('/validate/<string:_email>',methods=['POST'])
def validate(_email):
    req_Json = request.json
    user_otp = req_Json['otp']
    user = User.query.filter_by(email=_email).first()
    try:
        if otp==int(user_otp):
            user.activate_acc = 1
            db.session.commit()
            access_token = create_access_token(identity = _email,additional_claims=UserSchema().dump(user),expires_delta=timedelta(days=1))
            return access_token
        else:
            return "0" #code invalide
    except:
        return "0"

@user.route('/SendCode/<string:_email>',methods=['POST'])
def SendCode(_email):
        user = User.query.filter_by(email=_email).first()
        if user == None:
            return "0" #user n existe pas
        else:
            msg=Message(subject='CODE CONFIRMATION',sender='sofienemokaddem98@gmail.com',recipients=[_email])
            msg.body=str(otp)
            mail.send(msg)
            return "1"


@user.route('/VerifyCode',methods=['POST'])
def VerifyCode():
    req_Json = request.json
    user_otp = req_Json['otp']
    try:
        if otp==int(user_otp):
            return "1" #code valid
        else:
            return "0" #code invalid
    except:
        return "0"

@user.route('/ResetPassword/<string:_email>', methods = ['PUT'])
def ResetPassword(_email):
    if request.method == 'PUT':
        req_Json = request.json
        user = User.query.filter_by(email=_email).first()
        print(_email)
        if req_Json['password'] != req_Json['Conf_password'] :
            return "0" #il faut confirmer avec le même password
        else:
            password=bcrypt.generate_password_hash(req_Json['password'])
            user.password = password
            db.session.commit()
            return '1' #password modifié avec succés



@user.route("/Logout")
@jwt_required()
def dasboard():
    current_user = get_jwt_identity()
    return jsonify(message="Welcome! to the Data Science Learner", user = current_user)


@user.route("/UserExist/<string:_email>")
def UserExist(_email):
    user = User.query.filter_by(email=_email).first()
    if user == None:
        return "0" #user n'existe pas
    else:
        return "1" #user existe