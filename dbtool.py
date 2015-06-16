# -*- coding: utf-8 -*-
import json
from orm import *
from class_models import *
class data_handle:
    def __init__(self):
        # self.conn=sqlite3.connect('temp.db')
        # self.cursor=self.conn.cursor()
        self.db=db_handle()
        self.session=self.db.session
    def __del__(self):
        # self.cursor.close()
        # self.conn.close()
        del self.session
    def get_token(self,name):
        try:
            t=self.session.query(token).filter(token.username==name).one()
            print t.token
            if t !=None:
                return t.token
            return 0
        except Exception,e:
            return 0
    def check_token(self,username,t):
        try:
            m=self.session.query(token).filter(token.username==username and token.token==t).one()
            if m!=None:
                return True
            return False
        except Exception,e:
            return False
    def new_token(self,name,t):
        try:
            new_token=token(username=name,token=t)
            self.session.add(new_token)
            self.session.commit()
            return True
        except Exception,e:
            return False
    def new_group(self,name,g_name):
        try:
            r=self.session.query(contacts_group).filter(contacts_group.group_name==g_name,contacts_group.username==name).count()
            if r!=0:
                return False
            new_g=contacts_group(id=None,username=name,group_name=g_name)
            self.session.add(new_g)
            self.session.commit()
            return True
        except Exception,e:
            return False
    def new_contact(self,username,g_name,c_name,c_no,type):
        try:
            r=self.session.query(contacts).filter(contacts.username==username,contacts.group_name==g_name,contacts.contact==c_no).count()
            if r!=0:
                return False
            new_c=contacts(id=None,username=username,group_name=g_name,contact_name=c_name,contact=c_no,type=type)
            self.session.add(new_c)
            self.session.commit()
            return True
        except Exception,e:
            return False
    def new_task(self,username,t,send_list,set_date,send_way):
        try:
            new_task=task(id=None,username=username,task=t,send_list=send_list,set_date=set_date,send_way=send_way,status="未发送".decode("utf-8"))
            self.session.add(new_task)
            self.session.commit()
            return True
        except Exception,e:
            return False
    def del_task(self,username,id):
        try:
            self.session.query(task).filter(task.id==id,task.username==username).delete()
            self.session.commit()
            return True
        except Exception,e:
            return False
    def set_token(self,name,t):
        try:
            self.session.query(token).filter(token.username==name).update({token:t})
            return True
        except Exception,e:
            return False
    def get_pwd(self,name):
        try:
            pwd=self.session.query(user).filter(user.username==name).one()
            if pwd !=None:
                return pwd.password
            return 0
        except Exception,e:
            print e
            return 0
    def new_user(self,name,pwd,phone=None):
        try:
            u=user(username=name,password=pwd,phone=phone)
            self.session.add(u)
            self.session.commit()
            return True
        except Exception,e:
            return False
    def getContact_group(self,username):
        data={}
        try:
            d=[]
            result=self.session.query(contacts_group).filter(contacts_group.username==username).all()
            if result!=None:
                if len(result)==0:
                    data['errCode']=0
                    return data
                for i in result:
                    per_data={}
                    per_data['id']=i.id
                    per_data['group_name']=i.group_name
                    d.append(per_data)
                data['data']=d
                data['errCode']=1
                return data
        except Exception,e:
            print e
            data['errCode']=-1
    def list_task(self,username):
        result=self.session.query(task).filter(task.username==username).all()
        d=[]
        for i in xrange(len(result)):
            per_data={}
            per_data['no']=i+1
            per_data['id']=result[i].id
            per_data['task']=result[i].task
            per_data['send_list']=result[i].send_list
            per_data['date']=result[i].set_date
            per_data['status']=result[i].status
            d.append(per_data)
        data={}
        data['data']=d
        if len(result)==0:
            data['errCode']=0
        else:
            data['errCode']=1
        return data
    def searchtask_api(self,date,type):
        sql=self.session.query(task).filter(task.set_date<="2015-6-20",task.send_way=='phone',task.status=='未发送'.decode('utf-8'))
        print sql
        result=sql.all()
        data={}
        if len(result)==0:
            data['errCode']=-1
        else:
            d=[]
            for i in result:
                perdata={}
                perdata['task']=i.task
                perdata['target']=i.send_list
                d.append(perdata)
            data['errCode']=0
            data['data']=d
        return data
    def list_contacts(self,username,group_name):
        if group_name!='*all*':
            result=self.session.query(contacts).filter(contacts.username==username,contacts.group_name==group_name).all()
            d=[]
            for i in xrange(len(result)):
                per_data={}
                per_data['id']=result[i].id
                per_data['contact_name']=result[i].contact_name
                per_data['type']=result[i].type
                per_data['contact']=result[i].contact
                d.append(per_data)
            data={}
            data['data']=d
            if len(result)==0:
                data['errCode']=0
            else:
                data['errCode']=1
            return data
        else:
            result=self.session.query(contacts).filter(contacts.username==username).all()
            d=[]
            for i in xrange(len(result)):
                per_data={}
                per_data['id']=result[i].id
                per_data['contact_name']=result[i].contact_name
                per_data['type']=result[i].type
                per_data['contact']=result[i].contact
                d.append(per_data)
            data={}
            data['data']=d
            if len(result)==0:
                data['errCode']=0
            else:
                data['errCode']=1
            return data

if __name__=='__main__':
    d=data_handle()
    print d.list_contacts('1234','*all*')