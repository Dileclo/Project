from app import db,login,app
from flask_login import UserMixin
from dadata import Dadata
from flask import json
import datetime

class DadataINN():
    def __init__(self):
        self.token = "20defa76b6273253c20e0213cb383ddfe51c60aa"
        self.dadata = Dadata(self.token)
    def find_by_inn(self,inn):
        result = self.dadata.find_by_id("party",inn)
        if result:
            data = {'name':result[0]['value'],'kpp':result[0]['data']['kpp'],'ogrn':result[0]['data']['ogrn'],"address":result[0]['data']['address']['value']}
            return data

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
 
    def create(self, user):
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    inn = db.Column(db.String(64), index=True, unique=True)
    ogrn = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(64), index=True)
    SRO = db.Column(db.String(64), index=True)
    licence = db.Column(db.String(64), index=True)
    svvo = db.Column(db.String(64), index=True)
    kpp = db.Column(db.String(64), index=True)
    tipe = db.Column(db.String(64), index=True)
   
class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    zastroyshik = db.Column(db.String(64), index=True)
    lico_os_str = db.Column(db.String(64), index=True)
    lico_os_proekt = db.Column(db.String(64), index=True)
   
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name_org = db.Column(db.String(64), index=True)
    name_work = db.Column(db.String(64), index=True)
    
class AOCR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_object = db.Column(db.String(64), index=True)
    object = db.Column(db.String(64), index=True)
    zastroyshik = db.Column(db.String(64), index=True)
    lico_os_str = db.Column(db.String(64), index=True)
    lico_os_proekt = db.Column(db.String(64), index=True)
    name_work = db.Column(db.String(64), index=True)
    lico_vip_rab = db.Column(db.String(64), index=True)
    num_act = db.Column(db.String(64), index=True)
    start_date = db.Column(db.String(64), index=True)
    end_date = db.Column(db.String(64), index=True)
    pred_teh_zak = db.Column(db.String(64), index=True)
    pred_str = db.Column(db.String(64), index=True)
    pred_str_control = db.Column(db.String(64), index=True)
    pred_proekt = db.Column(db.String(64), index=True)
    pred_vip_rab = db.Column(db.String(64), index=True)
    inie = db.Column(db.String(64), index=True)
    work = db.Column(db.String(64), index=True)
    project = db.Column(db.String(64), index=True)
    materials = db.Column(db.String(64), index=True)
    isp_scheme = db.Column(db.String(64), index=True)
    reglament = db.Column(db.String(64), index=True)
    next_work = db.Column(db.String(64), index=True)
    prilozhenie = db.Column(db.String(64), index=True)
    
    def addAOCR(self,request):
        materials,prilozh = self.get_materials_for_aocr(request)
        prilozhenie = prilozh+" "+request['isp_scheme']
        zastroyshik,lico_os_str,lico_os_proekt,name_object,name_obj = self.get_full_info_about_objects(request)
        lico_vip_rab = self.get_info_by_inn(request['lico_vip_work'])
        num_act = request['num_act']
        start_date = datetime.datetime.strptime(request['start_date'],"%Y-%m-%d")
        end_date = datetime.datetime.strptime(request['end_date'],"%Y-%m-%d")
        pred_teh_zak = self.get_info_by_name(request.getlist('pred_teh_zak[]'))

        pred_str = self.get_info_by_name(request.getlist("pred_str[]"))
        pred_str_control = self.get_info_by_name(request.getlist("pred_str_control[]"))
        pred_proekt = self.get_info_by_name(request.getlist("pred_proekt[]"))
        pred_vip_rab = self.get_info_by_name(request.getlist("pred_vip_rab[]"))
        inie = self.get_info_by_name(request.getlist("inie[]"))
        work = request['work']
        project = request['project']
        reglaments = request['reglaments']
        next_work = request['next_work']
        isp_scheme = request['isp_scheme']
        name_work = request['name_work']
        aocr = AOCR(name_object= name_object,
                            object=name_obj,
                        zastroyshik=zastroyshik,
                        lico_os_str=lico_os_str,
                        lico_os_proekt=lico_os_proekt,
                        name_work=name_work,
                        lico_vip_rab=lico_vip_rab,
                        num_act=num_act,
                        start_date=start_date,
                        end_date=end_date,
                        pred_teh_zak=pred_teh_zak,
                        pred_str=pred_str,
                        pred_str_control=pred_str_control,
                        pred_proekt=pred_proekt,
                        pred_vip_rab=pred_vip_rab,
                        inie=inie,
                        work=work,
                        project=project,
                        materials=materials,
                        isp_scheme=isp_scheme,
                        reglament=reglaments,
                        next_work=next_work,
                        prilozhenie=prilozhenie)
        db.session.add(aocr)
        db.session.commit()
        return True

    def find_all_AOCR(self,name_object,name_work):
        aocrs = AOCR.query.filter_by(name_object=name_object,name_work=name_work).all()
        r = []
        for i in aocrs:
            r.append({'name': "<a href='/aocr/objects/"+name_object+"/"+name_work+"/"+i['num_act']+"'>"+i.num_act+"</a>","work":i.work,'start_date':i.start_date,'end_date':i.end_date,'next_work':i.next_work})
        return r

    def get_materials_for_aocr(self,request):
        mat = request.getlist('materials[]')
        materialx = []
        materials = []
        for i in mat:
            x = json.loads(i)
            materialx.append({'name':x['name'],"doc":x['doc']})
        for i in materialx:
            material = Materials.query.filter_by(name=i['name'],document=i['doc']).first()  # Retrieve the first matching object from the query
            if material:
                materials.append(material)
        stroke = " ; ".join('{} {} № {}'.format(i.name, i.tipe, i.document) for i in materials)
        prilozh = ", ".join('{} № {}'.format(i.tipe,i.document) for i in materials)
        return stroke,prilozh

    def get_full_info_about_objects(self,request):
        objects = Objects.query.filter_by(name=request['name_object']).first()
        print(request['name_object'])
        zastroyshik = self.get_info_by_inn(objects.zastroyshik)
        lico_os_str = self.get_info_by_inn(objects.lico_os_str)
        lico_os_proekt = self.get_info_by_inn(objects.lico_os_proekt)
        name_obj = objects.name
        name_object = objects.name+" по адресу: "+ objects.address
        return zastroyshik,lico_os_str,lico_os_proekt,name_object,name_obj
        
    def get_info_by_inn(self,inn):
        org = Organization.query.filter_by(inn=inn).first()
        stroke = ""
        for key,value in org.__dict__.items():

            if key != "_sa_instance_state":
                if key == 'inn' and value:
                    stroke +='ИНН '
                elif key == 'ogrn' and value:
                    stroke +='ОГРН '
                elif key == 'svvo' and value:
                    stroke +='св-во о гос. регистрации '
                elif key == "SRO" and value:
                    stroke += "СРО "
                elif key == "licence" and value:
                    stroke+= "рег. номер в реестре членов"
                elif key == "kpp":
                    continue
                elif key == 'tipe':
                    continue
                elif key == 'id':
                    continue
                if value:
                    stroke +=f'{value}; '
        print(stroke)
        return stroke

    def get_info_by_name(self,req):
        if req:
            name = json.loads(req[0])
            db = Person.query.filter_by(fio=name['name'],person_dolzhnost=name['dolzhnost']).first()
            return db.person_dolzhnost + db.person_org + db.fio + db.prikaz + db.person_licence
        else:
            return ""

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(64), index=True)
    person_dolzhnost = db.Column(db.String(64), index=True)
    person_org = db.Column(db.String(64), index=True)
    prikaz = db.Column(db.String(64), index=True)
    person_licence = db.Column(db.String(64), index=True)
    
class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    tipe = db.Column(db.String(64), index=True)
    document = db.Column(db.String(64), index=True)
    start_date = db.Column(db.String(64), index=True)
    end_date = db.Column(db.String(64), index=True)
       
with app.app_context():
    db.create_all()


@login.user_loader
def load_user(id):
    print("login")
    return User.query.get(int(id))
