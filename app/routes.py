from flask import jsonify, render_template,request,redirect,url_for
from app import app,db
from app.models import User,Organization,DadataINN,Objects,Work,AOCR,Person,Materials
from flask_login import current_user,login_user,login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

dada = DadataINN()
ao = AOCR()
# Auth
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ["POST","GET"])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('index'))
    if request.method == 'POST':
        print(request.form['email'],request.form['password'])
        user = db.session.query(User).filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password,request.form['password']):
            login_user(user,remember=True)
            return redirect(url_for('index'))
    return render_template('auth/login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
    
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
                return "Вы уже зарегистрированны"
        else:
            user = User(username = request.form['name'],
                    password = generate_password_hash(request.form['password']),
                    email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("auth/register.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# END AUTH

# Organization

@login_required
@app.route('/dbase')
def dbase():
    return render_template('dbase/dbase.html')

@app.route("/organization")
@login_required
def organization():
    res = Organization.query.all()
    r = []
    print(res)
    for i in res:
        r.append({'name': "<a href='/organization/"+i.inn+"'>"+i.name+"</a>",'inn': i.inn})
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(r)
    return render_template("dbase/organization.html",res = res)

@app.post("/by_inn")
def by_inn():
    if request.method == "POST":
        inn = request.form['inn']
        res = dada.find_by_inn(inn=inn)
        return res
    return ""

@app.post("/add_organization")
def add_organization():
    o = request.form
    if Organization.query.filter_by(inn=o['inn']).first():
        return "Организация уже существует"
    org = Organization(name=o['name'],inn=o['inn'],ogrn=o['ogrn'],address=o['address'],SRO=o['SRO'],licence=o['licence'],svvo=o['svvoreg'],kpp=o['kpp'],tipe=o['type'])
    db.session.add(org)
    db.session.commit()
    return "Успешно добавлено"

@app.route("/organization/<inn>")
@login_required
def organization_view(inn):
    res = Organization.query.filter_by(inn=inn).first()
    return render_template("dbase/organization_view.html",res = res)

@app.post("/delete_organization")
@login_required
def delete_organization():
    Organization.query.filter_by(inn=request.form['inn']).delete()
    db.session.commit()
    return "Успешно удалено"

@app.post("/change_organization")
@login_required
def change_organization():
    if request.method == "POST":
        o = request.form
        org = Organization.query.filter_by(inn=o['inn']).update(dict(name=o['name'],ogrn=o['ogrn'],inn=o['inn'],address=o['address'],SRO=o['SRO'],licence=o['licence'],svvo=o['svvoreg'],kpp=o['kpp'],tipe=o['type']))
        db.session.commit()
        return "Успешно изменено"     

# End organization

# Objects

@app.route('/objects')
@login_required
def objects():
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = Organization.query.all()
        r = []
        с = 0
        print(r)
        for i in res:
            с+=1
            r.append({"id":с,'text':i.name,"inn":i.inn})
            
        return r
            
    return render_template('dbase/objects.html')  
@app.post("/add_object")
@login_required
def add_object():
    o = request.form
    try:
        od = Objects(name=o['name'],address=o['address'],zastroyshik=o['zastroyshik'],lico_os_str=o['lico_os_str'],lico_os_proekt=o['lico_os_proekt'])
        print(od)
        db.session.add(od)
        db.session.commit()
        return "Успешно добавлено"
    except:
        return "Не удалось добавить"

@app.route("/objects/<object>",methods=["GET", "POST"])
@login_required
def objects_view(object):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        r = []
        res = Work.query.filter_by(name_org=object).all()
        for i in res:
            r.append({'name': "<a href='/objects/"+i.name_org+"/"+i.name_work+"'>"+i.name_work+"</a>"})
        return jsonify(r)
    res = Objects.query.filter_by(name=object).first()

    return render_template('aocr/object_view.html',res=res)  

@app.post("/addWork")
@login_required
def addWork():
    if request.method == "POST":
        o = request.form
        try:
            w = Work(name_work=o['name_work'],name_org=o['name_org'])
            db.session.add(w)
            db.session.commit()
            return "Успешно добавленно"
        except:
            return "Не удалось добавить"
        
@app.route("/objects/<object>/<work>",methods=["GET", "POST"])
@login_required
def objects_work_view(object,work):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        r = ao.find_all_AOCR(name_object=object,name_work=work)
        return r
    res = Objects.query.filter_by(name=object).first()

    return render_template('aocr/object_work_view.html',res=res,work=work)
 

#Persons
@app.route("/persons",methods=["POST","GET"])
@login_required
def persons():
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = Person.query.all()
        r = []
        с = 0
        for i in res:
            с+=1
            r.append({"id":с,'text':i.fio,'person_dolzhnost':i.person_dolzhnost})
        return r
            
    return render_template('dbase/objects.html')

@app.route("/add_person",methods=['POST'])
@login_required
def add_person():
    if request.method == 'POST':
        o = request.form
        try: 
            person = Person(fio = o['fio'],person_dolzhnost = o['person_dolzhnost'],person_org = o['person_org'],prikaz = o['prikaz'], person_licence = o['person_licence'])
            db.session.add(person)
            db.session.commit()
            return "Успешно добавлено"
        except:
            return "Не удалось добавить"


# End Persons 

# Materials
@app.route("/materials",methods=["POST","GET"])
@login_required
def materials():
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = Materials.query.all()
        r = []
        с = 0
        for i in res:
            с+=1
            r.append({"id":с,'text':i.name,"doc":i.document})
        return r
            
    return render_template('dbase/objects.html')

@app.route("/add_materials",methods=['POST'])
@login_required
def add_materials():
    if request.method == 'POST':
        o = request.form
        try: 
            mat = Materials(name= o['name_mat'],tipe=o['type_mat'],document=o['doc_mat'],start_date=o['start_mat'],end_date=o['end_mat'])
            db.session.add(mat)
            db.session.commit()
            return "Успешно добавлено"
        except:
            return "Не удалось добавить"


# End Materials


# AOCR

@app.route('/aocr')
@login_required
def aocr():
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = Objects.query.all()
        r = []
        for i in res:
            r.append({'name': "<a href='/objects/"+i.name+"'>"+i.name +"</a>"})
        return jsonify(r)

    return render_template('aocr/aocr.html')

        
@app.post("/add_aocr")
@login_required
def add_aocr():
    if ao.addAOCR(request.form):
        return "Успешно добавлено"
    else:
        return "Не удалось добавить"