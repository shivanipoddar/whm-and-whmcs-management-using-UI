from django.shortcuts import render
from random import *
import string
import json
import pycpanel
import whmcspy


usr = 'none'
identifier = 'identifier'
secret = 'secret'
whmcs = whmcspy.WHMCS('http://www.yourdomain.com/support/includes/api.php', identifier, secret)


def login(request):
    if request.method == 'POST':
        em = request.POST.get('em')
        ps = request.POST.get('ps')
        global usr
        try:
            whmcs.ValidateLogin(email=em, password2=ps)
            usr = whmcs.GetClientsDetails(email=em)['fullname']
            return render(request, 'user.html', {'user': usr})
        except:
            return render(request, 'wrong.html')
    else:
        if usr == 'none':
            return render(request, 'login.html')
        else:
            return render(request, 'logout.html')


def adddom(request):
    if request.method == 'POST':
            nm = request.POST.get('nm')
            em = request.POST.get('ce')
            msg = request.POST.get('msg')
            pn = request.POST.get('pn')
            un = nm.split(".")[0]
            li = []
            characters = string.ascii_letters + string.punctuation + string.digits
            ps = "".join(choice(characters) for x in range(randint(8, 16)))
            server = pycpanel.conn(hostname='hostname.com', password='password', )
            if pn != 'none':
                param = {
                    'username': un,
                    'domain': nm,
                    'contactemail': "contact@mail.in",
                    'password': ps,
                    'pkgname': pn
                }
                r = (server.api('createacct', param))
                rs = json.dumps(r, indent=4)
                try:
                    rst = rs.rsplit("New Account Info")[1]
                    re = rst.rsplit("Language: en")[0]
                    for i in range(1, 15):
                        resu = re.rsplit("\\n|")[i]
                        li.append(resu)
                    res = li
                except:
                    res = rs
                if str(em) != 'None':
                    characters = string.ascii_letters + string.punctuation + string.digits
                    ps = "".join(choice(characters) for x in range(randint(8, 16)))
                    params = {
                        'email': em,
                        'password': ps,
                        'domain': nm,
                        'quota': 500,
                    }
                    ed = server.cpanel_api('Email', 'addpop', un, params=params)
                else:
                    ed = None
                td = whmcs.OpenTicket(deptid='2', subject='new account created', message=msg, name=un, email=nm)
                return render(request, 'detail.html', {"result": res, "td": td, "ed":ed})
            else:
                return render(request, 'login.html')
    else:
        if usr == 'none':
            return render(request, 'wrong.html')
        else:
            return render(request, 'adddomain.html')


def email(request):
    if request.method == 'POST':
            dnm = request.POST.get('nm')
            enm = request.POST.get('ce')
            unm = request.POST.get('unm')
            characters = string.ascii_letters + string.punctuation + string.digits
            ps = "".join(choice(characters) for x in range(randint(8, 16)))
            server = pycpanel.conn(hostname='hostname.com', password='password', )
            params = {
                'email' : enm,
                'password' : ps,
                'domain' : dnm,
                'quota' : 500,
            }
            res = server.cpanel_api('Email', 'addpop', unm, params=params)
            return render(request, 'detail.html', {'result': res})
    else:
        if usr == 'none':
            return render(request, 'wrong.html')
        else:
            return render(request, 'addemail.html')


def user(request):
    if usr == 'none':
        return render(request, 'wrong.html')
    else:
        return render(request, 'user.html', {'user': usr})


def log(request):
    global usr
    usr = 'none'
    return render(request, 'log.html')


def accountlist(request):
    if request.method == 'POST':
        nm = request.POST.get('nm')
        ps = request.POST.get('ps')
        try:
            server = pycpanel.conn(hostname=nm, password=ps, )
            li = []
            dom = server.api('listaccts')['acct']
            for i in range(190):
                det = dom[i]['domain']
                li.append(det)
            res = li
            return render(request, 'accountlist.html', {'dom': res})
        except:
            return render(request, 'wrong.html', )
    else:
        return render(request, 'server.html')

def ticket(request):
    if request.method == 'POST':
            nm = request.POST.get('nm')
            em = request.POST.get('em')
            sb = request.POST.get('sb')
            ms = request.POST.get('ms')
            res = whmcs.OpenTicket( deptid='1', subject=sb, message=ms, name=nm, email=em)
            return render(request, 'detail.html', {'result': res})
    else:
        if usr == 'none':
            return render(request, 'wrong.html')
        else:
            return render(request, 'openticket.html')


def addclient(request):
    if request.method == 'POST':
            nm = request.POST.get('nm')
            ln = request.POST.get('ln')
            em = request.POST.get('em')
            ad = request.POST.get('ad')
            ct = request.POST.get('ct')
            st = request.POST.get('st')
            pc = request.POST.get('pc')
            pn = request.POST.get('pn')
            characters = string.ascii_letters + string.punctuation + string.digits
            ps = "".join(choice(characters) for x in range(randint(8, 16)))
            addcl = whmcs.add_client(
                   firstname=nm,
                   lastname=ln,
                   email=em,
                   address1=ad,
                   city=ct,
                   state=st,
                   postcode=pc,
                   country="IN",
                   phonenumber=pn,
                   password2=ps)
            return render(request, 'detail.html', {'result': addcl} )
    else:
        if usr == 'none':
            return render(request, 'wrong.html')
        else:
            return render(request, 'addclient.html' )
