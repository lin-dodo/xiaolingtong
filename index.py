from flask import Flask
from flask import request
from flask import render_template, redirect, url_for, make_response, flash, abort,session
from flask import g
import json
import copy,sys
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
            #name =request.cookies.get('name','')
            if token == '':
                token = request.form.get('token', '')
            if token == '':
                return render_template("test.html", text="sorry, please login first.", url=url_for('login', url=request.url) )
            elif not g.dH.check_token(token):
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
        if token !='':
            if g.dH.check_token(token):
                return render_template("index.html")
        return render_template('login.html')


@app.route('/contacts/')
@login_require(2)
def contacts():
    return render_template('contacts.html')
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

if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)
