import sqlite3,json
class data_handle:
    def __init__(self):
        self.conn=sqlite3.connect('temp.db')
        self.cursor=self.conn.cursor()
    def __del__(self):
        self.cursor.close()
        self.conn.close()
    def get_token(self,name):
        try:
            self.cursor.execute("select token from token where username = '%s'"%name)
            token=self.cursor.fetchone()
            if token !=None:
                return token[0]
            return 0
        except Exception,e:
            return 0
    def check_token(self,username,token):
        try:
            self.cursor.execute("select token from token where token = '%s' and username = '%s'"%(token,username))
            m=self.cursor.fetchone()
            if m!=None:
                return True
            return False
        except Exception,e:
            return False
    def new_token(self,name,token):
        try:
            self.cursor.execute("insert into token ('usernaem','token') values ('%s','%s')"%(name,token))
            self.conn.commit()
            return True
        except Exception,e:
            return False
    def set_token(self,name,token):
        try:
            self.cursor.execute("update token set token = '%s' where username = '%s'"%(token,name))
            self.conn.commit()
            return True
        except Exception,e:
            return False
    def get_pwd(self,name):
        try:
            m=self.cursor.execute("select password from user where username ='%s'"%name)
            pwd=self.cursor.fetchone()
            if pwd !=None:
                return pwd[0]
            return 0
        except Exception,e:
            return 0
    def new_user(self,name,pwd,phone):
        try:
            self.cursor.execute("insert into user ('username','password','phone') values ('%s','%s','%s')"%(name,pwd,phone))
            self.conn.commit()
            return True
        except Exception,e:
            return False
    def list_task(self,username):
        self.cursor.execute("select * from task where username = '%s'"%username)
        result=self.cursor.fetchall()
        d=[]
        for i in xrange(len(result)):
            per_data={}
            per_data['no']=i+1
            per_data['id']=result[i][0]
            per_data['task']=result[i][2]
            per_data['send_list']=result[i][3]
            per_data['date']=result[i][4]
            per_data['status']=result[i][-1]
            d.append(per_data)
        data={}
        data['data']=d
        if len(result)==0:
            data['errCode']=0
        else:
            data['errCode']=1
        return data
    def searchtask_api(self,date,type):
        self.cursor.execute("select task,send_list from task where set_date<='%s' and send_way='%s'"%(date,type))
        result=self.cursor.fetchall()
        data={}
        if len(result)==0:
            data['errCode']=-1
        else:
            d=[]
            for i in result:
                perdata={}
                perdata['task']=i[0]
                perdata['target']=i[1]
                d.append(perdata)
            data['errCode']=0
            data['data']=d
        return data
    def list_contacts(self,username,contact_type,group_name):
        if contact_type!='all':
            if group_name!='*all*':
                self.cursor.execute("select contact from contacts where username='%s' and type='%s' and group_name='%s'"%(username,contact_type,group_name))
                result=self.cursor.fetchall()
                d=[]
                for i in xrange(len(result)):
                    per_data={}
                    per_data['contact']=result[i][0]
                    d.append(per_data)
                data={}
                data['data']=d
                if len(result)==0:
                    data['errCode']=0
                else:
                    data['errCode']=1
                return data
            else:
                self.cursor.execute("select contact from contacts where username='%s' and type='%s'"%(username,contact_type))
                result=self.cursor.fetchall()
                d=[]
                for i in xrange(len(result)):
                    per_data={}
                    per_data['contact']=result[i][0]
                    d.append(per_data)
                data={}
                data['data']=d
                if len(result)==0:
                    data['errCode']=0
                else:
                    data['errCode']=1
                return data
        else:
            if group_name!='*all*':
                self.cursor.execute("select contact from contacts where username='%s' and group_name='%s'"%(username,group_name))
                result=self.cursor.fetchall()
                d=[]
                for i in xrange(len(result)):
                    per_data={}
                    per_data['contact']=result[i][0]
                    d.append(per_data)
                data={}
                data['data']=d
                if len(result)==0:
                    data['errCode']=0
                else:
                    data['errCode']=1
                return data
            else:
                self.cursor.execute("select contact from contacts where username='%s'"%(username))
                result=self.cursor.fetchall()
                d=[]
                for i in xrange(len(result)):
                    per_data={}
                    per_data['contact']=result[i][0]
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
    print d.list_contacts('1234','all','*all*')