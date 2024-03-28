from pymongo import MongoClient
from flask import flash,json
import datetime
client = MongoClient()
client = MongoClient("mongodb://localhost:27017")
db = client.data_base
db_users = db.users
db_organization = db.organization
db_objects = db.objects
db_works = db.works_for_object
db_aocr = db.aocr
db_persons = db.persons
db_materials = db.materials

class Users():
    def addUser(self, name, email, password):
        user = db_users.find_one({"email":email})
        if user:
            print("Такой пользователь уже зарегистрирован")
            return
        db_users.insert_one({"name":name, "email":email, "password":password})
    
    def find_by_email(self, email):
        user = db_users.find_one({"email":email})
        return user

class Organization():
    
    def addOrganization(self,name,ogrn,inn,address,SRO,licence,svvo,kpp,type):
        org = db_organization.find_one({"inn":inn})
        if org:
            return False
        else:
            db_organization.insert_one({"name":name,"inn":inn,"ogrn":ogrn, "address":address,"SRO":SRO, "licence":licence, "svvo":svvo,'kpp':kpp, "type":type})
            return True

    def find_all_organizations(self):
        organ = []
        for i in db_organization.find({}):
            organ.append(i)
        return  organ
    
    def find_organization_by_inn(self,inn):
        return db_organization.find_one({"inn":inn})
    
    def deleteOrganization_by_inn(self,inn):
        return db_organization.delete_one({"inn":inn}) 
    
    def change_organization(self,name,ogrn,inn,address,SRO,licence,svvo,kpp,type):
        if db_organization.replace_one({"inn":inn},{"name":name,"ogrn":ogrn,"inn":inn, "address":address,"SRO":SRO, "licence":licence, "svvo":svvo,'kpp':kpp, "type":type}):
            return True
        return False
    
class Objects():
    def add_objects(self,name,address,zastroyshik,lico_os_str,lico_os_proekt):
        obj = db_objects.find_one({"name":name})
        if obj:
            return False
        else:
            db_objects.insert_one({'name':name, 'address':address, 'zastroyshik':zastroyshik, 'lico_os_str':lico_os_str, 'lico_os_proekt':lico_os_proekt})
            return True
    
    def find_all_objects(self):
        r = []
        for i in db_objects.find({}):
            r.append(i)
        return r
    def find_object_by_name(self,name):
        return db_objects.find_one({"name":name})
    
class Works():
    def add_work(self,work,name):
        if db_works.insert_one({'name_org':name,'name_work':work}):
            return True
        else:
            return False
    
    def find_work_by_name_org(self,name):
        res = []
        r = db_works.find({'name_org':name})
        for i in r:
            res.append(i)
        return res
        
class AOCR():
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
        if db_aocr.insert_one({'name_object':name_object,
                               "object":name_obj,
                            "zastroyshik":zastroyshik,
                            "lico_os_str":lico_os_str,
                            "lico_os_proekt":lico_os_proekt,
                            'name_work':name_work,
                            'lico_vip_rab':lico_vip_rab,
                            'num_act':num_act,
                            'start_date':start_date,
                            'end_date':end_date,
                            'pred_teh_zak':pred_teh_zak,
                            'pred_str':pred_str,
                            'pred_str_control':pred_str_control,
                            'pred_proekt':pred_proekt,
                            'pred_vip_rab':pred_vip_rab,
                            'inie':inie,
                            'work':work,
                            'project':project,
                            'materials':materials,
                            'isp_scheme':isp_scheme,
                            'reglaments':reglaments,
                            'next_work':next_work,
                            'prilozhenie':prilozhenie}):
            return True
        else:
            return False

    def find_all_AOCR(self,name_object,name_work):
        aocrs = db_aocr.find({'object':name_object,'name_work':name_work})
        print(aocrs)
        r = []
        for i in aocrs:
            # data.append({'num_act':i['num_act'],'work':i['work'],'start_date':i['start_date'],'end_date':i['end_date'],'next_work':i['next_work']})
            r.append({'name': "<a href='/aocr/objects/"+name_object+"/"+name_work+"/"+i['num_act']+"'>"+i['num_act']+"</a>","work":i['work'],'start_date':i['start_date'],'end_date':i['end_date'],'next_work':i['next_work']})
        return r

    def get_materials_for_aocr(self,request):
        mat = request.getlist('materials[]')
        materialx = []
        materials = []
        for i in mat:
            x = json.loads(i)
            materialx.append({'name':x['name'],"doc":x['doc']})
        for i in materialx:
            materials.append(db_materials.find_one({'name':i['name'],"document":i['doc']}))
        stroke = " ; ".join('{} {} № {}'.format(i['name'],i['type'],i['document']) for i in materials)
        prilozh = ", ".join('{} № {}'.format(i['type'],i['document']) for i in materials)
        return stroke,prilozh

    def get_full_info_about_objects(self,request):
        object = db_objects.find_one({'name':request['name_object']})
        zastroyshik = self.get_info_by_inn(object['zastroyshik'])
        lico_os_str = self.get_info_by_inn(object['lico_os_str'])
        lico_os_proekt = self.get_info_by_inn(object['lico_os_proekt'])
        name_obj = object['name']
        name_object = object['name']+" по адресу: "+ object['address']
        return zastroyshik,lico_os_str,lico_os_proekt,name_object,name_obj
        
    def get_info_by_inn(self,inn):
        org = db_organization.find_one({'inn':inn})
        stroke = ""
        for key,value in org.items():

            if key != "_id":
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
                elif key == 'type':
                    continue
                if value:
                    stroke +=f'{value}; '
        return stroke

    def get_info_by_name(self,req):
        if req:
            name = json.loads(req[0])
            db = db_persons.find_one({'fio':name['name'],'person_dolzhnost':name['dolzhnost']})
            return db
        else:
            return ""

class Persons():
    def find_all_persons(self):
        res = db_persons.find({})
        r = []
        for i in res:
            r.append(i)
        return r
    
    def add_person(self,fio,person_dolzhnost,person_org,prikaz,person_licence):
        if db_persons.insert_one({"fio":fio,"person_dolzhnost":person_dolzhnost,"person_org":person_org,"prikaz":prikaz,"person_licence":person_licence}):
            return True
        else:
            return False
        
class Materials():
    def add_material(self,name,type,document,start_date,end_date):
        if db_materials.insert_one({"name":name,"type":type,"document":document,"start_date":start_date,"end_date":end_date}):
            return True
        else:
            return False
    
    def find_all_materials(self):
        res = db_materials.find({})
        r = []
        for i in res:
            r.append(i)
        return r