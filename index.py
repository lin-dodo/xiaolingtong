from flask import Flask
from flask import request
from flask import render_template, redirect, url_for, make_response, flash, abort,session
from flask import g
import json
import copy,sys,urllib,datetime
import random,dbtool
cookies_remain_time=24*60*60
def strrandom(len):
    ret=''
    while len:
        ret += random.choice('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ')
        len -= 1
    return ret

app = Flask(__name__)
app.secret_key = 'b$tXU_cv@lJzYzKXJVcs$tSaBBFiqyGIJVxrXjehCOpl#QQZpAimb~$RMncab$zJ'

def login_require_1(permit=2):
    def _checkLogin(func):
        def checkLogin(*args,**kwds):
            token=request.cookies.get('token','')
            session['see']=token
            func(*args,**kwds)
        #checkLogin.__name__ = func.__name__
        return checkLogin
    return _checkLogin
def login_require(permit = 2):
    def _checkLogin(func):
        def checkLogin(*args, **kwds):
            token = request.cookies.get('token', '')
            username =request.cookies.get('username','')
            if token == '':
                token = request.form.get('token', '')
            if token == '' or username=='':
                return render_template("test.html", text="sorry, please login first.", url=url_for('login', url=request.url) )
            elif not g.dH.check_token(username,token):
                #print url_for('see', url=request.url)
                return render_template("test.html", text="sorry, the user has logout or login in other place.", url=url_for('login', url=request.url) )
            return func(*args, **kwds)
            # username = g.dH.getUsernameByToken( token )
            # if g.dH.getUserPermit( username ) <= permit:
            #     return func(*args, **kwds)
            # else:
            #     return "no permit."

        checkLogin.__name__ = func.__name__
        return checkLogin

    return _checkLogin

@app.before_request
def before_request():
    g.dH = dbtool.data_handle()

@app.route('/')
@login_require(2)
def index():
    return render_template("index.html")

    #return 'Hello World!'

@app.route("/register/",methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        username=request.args.get('username','')
        if username=='':
            return render_template("register.html")
        else:
            return str(g.dH.get_pwd(username))
    else:
        user=request.form.get('name','')
        pwd=request.form.get('pwd','')
        token=strrandom(32)
        if g.dH.new_user(user,pwd) and g.dH.new_token(user,token):
            #return "0"
            re=make_response("0")
            re.set_cookie('username',user,cookies_remain_time)
            re.set_cookie('token',token,cookies_remain_time)
            return re
        else:
            return "-1"
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        user=request.form.get('username','')
        pwd=request.form.get('pwd','')
        retData={}
        #print pwd
        pass_real=g.dH.get_pwd(user)
        token=''
        if pass_real==0:
            retData['errCode']=0
        else:
            #print pwd,pass_real
            if pwd==pass_real:
                retData['errCode']=-1
                token=strrandom(32)
                retData['token']=token
            else:
                retData['errCode']=1
        g.dH.set_token(user,token)
        re=make_response( json.dumps(retData))
        re.set_cookie('username',user,cookies_remain_time)
        re.set_cookie('token',token,cookies_remain_time)
        return re
    else:
        token = request.cookies.get('token', '')
        username= request.cookies.get('username','')
        if token !='':
            if g.dH.check_token(username,token):
                return render_template("index.html")
        return render_template('login.html')

@app.route('/list/')
@login_require()
def search():
    Data={}
    type=request.args.get('type','')
    username=request.cookies.get('username','')
    if type=='' and username =='':
        Data['errCode']=-1
    else:
        if type=='task':
            Data=g.dH.list_task(username)
        if type=='contasts':
            contact_type=request.args.get('contast_type','')
            group_name=request.args.get('group_name','')
            Data=g.dH.list_contacts(username,contact_type,group_name)
        if type=='group':
            Data=g.dH.getContact_group(username)

    return json.dumps(Data)
@app.route('/contacts/')
@login_require(2)
def contacts():
    return render_template('contacts.html')
@app.route('/searchcontacts/')
@login_require(2)
def searchcontacts():
    username=request.cookies.get('username','')
    group_name=urllib.unquote(request.args.get('group_name',''))
    print group_name
    Data=g.dH.list_contacts(username,group_name)
    return json.dumps(Data)

@app.route('/document/')
@login_require(2)
def document():
    return render_template('document.html')
@app.route('/user/')
@login_require(2)
def user():
    return render_template('user.html')
@app.route('/about/')
@login_require(2)
def about():
    return render_template('about.html')
@app.route('/searchtask/')
def searchtask():
    type=request.args.get('type','')
    if type=='phone':
        now=datetime.datetime.now()
        t=now.strftime("%Y-%m-%d %H:%M:%S")
        Data=g.dH.searchtask_api(t,type)
        return json.dumps(Data)
@app.route("/new/",methods=['GET', 'POST'])
@login_require(2)
def newItem():
    if request.method =='GET':
        username=request.cookies.get('username','')
        type=request.args.get('type','')
        if type=='group':
            g_name=request.args.get('g_name','')
            if type=='':
                return "-1"
            else:
                if g.dH.new_group(username,urllib.unquote(g_name)):
                    return "0"
                else:
                    return "-1"
        if type=='contact':
            g_name=urllib.unquote(request.args.get('g_name',''))
            c_name=urllib.unquote(request.args.get('c_name',''))
            c_no=request.args.get('c_no','')
            c_type=request.args.get('c_type','')
            if g_name=='' or c_name=='' or c_no=='':
                return "-1"
            else:
                if g.dH.new_contact(username,g_name,c_name,c_no,c_type):
                    return "0"
                else:
                    return "-1"
    else:
        username=request.cookies.get('username','')
        task=request.form.get('task','')
        send_list=request.form.get('send_list','')
        set_date=request.form.get('date','')
        set_way=request.form.get('type','')
        if task!='' or send_list!='' or set_date!='' or set_way!='':
            if g.dH.new_task(username,task,send_list,set_date,set_way):
                return "0"
            else:
                return "-1"
        else:
            return "-1"
@app.route("/delete/")
@login_require(2)
def delete():
    username=request.cookies.get('username','')
    type=request.args.get('type','')
    if type=='task':
        id=request.args.get('id','')
        if id!='':
            if g.dH.del_task(username,id):
                print "del"
                return "0"
            else:
                print "failed"
                return "-1"
        else:
            return "-1"


if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)
