from django.shortcuts import render
from django.db.models import Avg,Max,Min,Sum,Count
from vishalapp.models import Login
from vishalapp.models import Registration
from vishalapp.models import Guestdetails
from vishalapp.models import PGdetails
from vishalapp.models import paycard
from vishalapp.models import custpayment
from vishalapp.models import custfeedback
from vishalapp.models import expensee
from vishalapp.models import bookingdetails
from .models import expensee
from django.contrib.auth import get_user_model
from calendar import calendar
import datetime
import smtplib
import random
from django.core.files.storage import FileSystemStorage
from vishal.settings import BASE_DIR
import os

# Create your views here.

def index(request):
    return render(request,'index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('t1', '')
        password = request.POST.get('t2', '')
        request.session['username']=username
        #if username=="admin" and password=="admin":
        checklogin = Login.objects.filter(Emailid=username).values()
        for a in checklogin:
            utype = a['type']
            upass= a['Password']
            if(upass == password):

                if(utype == "admin"):

                    return render(request,'admin_home.html',context={'msg':'welcome to admin'})
                if(utype == "guest"):
                    return render(request, 'guest_home.html', context={'msg': 'welcome to user'})
            else:
                return render(request,'login.html',context={'msg':'LOGIN FAILED'})

    return render(request,'login.html')

def forgotpassword(request):
    if request.method=="POST":
        uname = request.POST.get('t1', '')
        user = Login.objects.filter(Emailid=uname).count()
        if user >= 1:
            userlog = Login.objects.filter(Emailid=uname).values()
            for u in userlog:
                upass= u['Password']
                content = upass
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('vishalenterprisers11@gmail.com', 'Vishal@11')
                mail.sendmail('vishalenterprisers11@gmail.com', uname , content)
                mail.close()
                return render(request,'login.html', {'msg': 'Your password has been sent to your E-mail'})
        else:
            return render(request,'forgotpassword.html', {'msg': 'Enter a valid username'})
    return render(request,'forgotpassword.html')


def userregistration(request):
    if request.method=="POST":
        Fname=request.POST.get('t1','')
        Lname = request.POST.get('t2', '')
        emailid = request.POST.get('t3', '')
        password = request.POST.get('t4', '')
        confirmpass= request.POST.get('t5', '')
        State = request.POST.get('t6', '')
        city = request.POST.get('t7', '')

        user=Registration.objects.filter(emailid=emailid).count()
        if user >= 1:
            return render(request,'registration.html',{'msg':'user is already exist'})
        else:
            Registration.objects.create(Fname=Fname,Lname=Lname,emailid=emailid,Password=password,Confirmpass=confirmpass,State=State,city=city)
            Login.objects.create(Emailid=emailid,Password=password,type='guest')
            content = "Thank You for Registering!"
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('vishalenterprisers11@gmail.com', 'Vishal@11')
            mail.sendmail('vishalenterprisers11@gmail.com', emailid, content)
            mail.close()
            return render(request,'index.html',{'msg':'Registration successfull'})

    return render(request,'registration.html')    
        
   

def pgdetails(request):
    if request.method == "POST":
        name=request.POST.get('t1','')
        address= request.POST.get('t2', '')
        location= request.POST.get('t3', '')
        categories = request.POST.get('t4','')
        Contactdetails= request.POST.get('t5', '')
        roomno=request.POST.get('rmno','')
        occupants=request.POST.get('occupants','')
        Image1 = request.FILES['file1']
        fs = FileSystemStorage()
        filename = fs.save(Image1.name, Image1)
        uploaded_file_url = fs.url(filename)
        pat = os.path.join(BASE_DIR, '/media/' + filename)
        Image2 = request.FILES['file2']
        fs = FileSystemStorage()
        filename = fs.save(Image2.name, Image2)
        uploaded_file_url = fs.url(filename)
        pat = os.path.join(BASE_DIR, '/media/' + filename)
        PGdetails.objects.create(pgname=name,pgaddress=address,pglocation=location,categories=categories,contactdetails=Contactdetails,image1=Image1,image2=Image2,room_no=roomno,occupants=occupants)

    return render(request, 'pgdetails.html')

def pgview(request):
    user_dict=PGdetails.objects.all()
    #user_dict={'users':user_list}
    return render(request,'PGview.html',{'user_dict':user_dict})

def delete_details(request):
    if request.method == 'POST':
        userdata= PGdetails.objects.all()
        id=request.POST.get('id')
        useritem= PGdetails.objects.get(id=id)

        useritem.delete()
        user_item = PGdetails.objects.all()
    return render(request,'PGview.html',context={'user_dict':user_item})


def update_details(request):
    if request.method == 'POST':
        userdata=PGdetails.objects.all()
        id=request.POST.get('id')
        useritem=PGdetails.objects.filter(id=id).values()
        #print(useritem)
        return render(request,'PGedit.html',{'useritem':useritem})

def PG_db(request):
    if request.method == 'POST':
        userdata=PGdetails.objects.all()
        id=request.POST.get('id')
        useritem=PGdetails.objects.filter(id=id).values()
        pgname = request.POST.get('t1', '')
        pgaddress = request.POST.get('t2', '')
        pglocation = request.POST.get('t3', '')
        cat = request.POST.get('t4','')
        contactdetails = request.POST.get('t5', '')
        PGdetails.objects.filter(id=id).update(pgname=pgname,pgaddress=pgaddress,pglocation=pglocation,categories=cat,contactdetails=contactdetails)
        user_item=PGdetails.objects.all()
    return render(request,'PGview.html',context={'user_dict': user_item})

def guest_details(request):
    num=random.randint(1,200)
    gid =Guestdetails.objects.all().aggregate(Max('Custid'))['Custid__max']
    cid = int(gid)+1
    bid=Guestdetails.objects.all().aggregate(Max('Bookid'))['Bookid__max']
    bid = int(bid)+1

    if request.method == "POST":
        date=request.POST.get('t1','')
        pgid = request.POST.get('t2', '')
        custid= request.POST.get('t3', '')
        bookid= request.POST.get('t4', '')
        studentname = request.POST.get('t5', '')
        mobileno = request.POST.get('t6', '')
        Permanentaddress= request.POST.get('t7', '')
        roomno = request.POST.get('t8', '')
        city = request.POST.get('t10', '')
        studenttype = request.POST.get('t11', '')
        depositamount = request.POST.get('t12', '')
        Guestdetails.objects.create(Mobilenumber=mobileno,Date=date,PGid=pgid,Custid=custid,Bookid=bookid,Studentname=studentname,Permanentaddress=Permanentaddress,Roomno=roomno,City=city,studenttype=studenttype,Depositamount=depositamount)

    return render(request,'guest_details.html',{'gid':cid,'bid':bid})

def guestview(request):
    user_dict=Guestdetails.objects.all()
    #user_dict={'users':user_list}
    return render(request,'guestview.html',{'user_dict':user_dict})

def guest_remove(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        useritem=Guestdetails.objects.get(id=id)
        useritem.delete()
        user_item = Guestdetails.objects.all()
    return render(request,'guestview.html',context={'user_dict': user_item})

def guest_update(request):
    if request.method == 'POST':
        userdata=Guestdetails.objects.all()
        id=request.POST.get('id')
        useritem=Guestdetails.objects.filter(id=id).values()
        #print(useritem)
        return render(request,'guestedit.html',{'useritem':useritem})

def guest_db(request):
    if request.method == 'POST':
        userdata=Guestdetails.objects.all()
        id=request.POST.get('id')
        useritem=Guestdetails.objects.filter(id=id).values()
        date = request.POST.get('t1')
        pgid = request.POST.get('t2')
        custid = request.POST.get('t3')
        bookid = request.POST.get('t4')
        studentname = request.POST.get('t5')
        mobileno = request.POST.get('t6')
        Permanentaddress = request.POST.get('t7')
        roomno = request.POST.get('t8', '')
        city = request.POST.get('t9', '')
        studenttype = request.POST.get('t10', '')
        depositamount = request.POST.get('t11', '')
        Guestdetails.objects.filter(id=id).update(Date=date,PGid=pgid,Custid=custid,Bookid=bookid,Studentname=studentname,Mobilenumber=mobileno,Permanentaddress=Permanentaddress,Roomno=roomno,City=city,studenttype=studenttype,Depositamount=depositamount)
        user_item=Guestdetails.objects.all()
    return render(request,'guestview.html',context={'user_dict': user_item})

def changepassword(request):
    user_dict={'msg':'one record inserted successfully'}
    if request.method == "POST":
        uname = request.POST.get('t1','')
        currentpass = request.POST.get('t2','')
        newpass = request.POST.get('t3','')
        confirmpass = request.POST.get('t4','')

        ucheck = Login.objects.filter(Emailid=uname).values()
        for a in ucheck:
            u=a['Emailid']
            p=a['Password']
            if u == uname and currentpass == p:
                if newpass == confirmpass:
                    Login.objects.filter(Emailid=uname).update(Password=newpass)
                    return render(request,'login.html', context={'msg':'password successfully changed'})
                else:
                    return render(request,'changepassword.html', context={'msg':'both the password must match'})
            else:
                return render(request,'changepassword.html',context={'msg':'inavlid username or password'})
    return render(request,'changepassword.html')

def paycard_db(request):
    if request.method == 'POST':
        userdata=paycard.objects.all()
        id=request.POST.get('id')
        useritem=paycard.objects.filter(id=id).values()
        Custid = request.POST.get('select', '')
        Month = request.POST.get('select2', '')
        Date = request.POST.get('datefield', '')
        Recivedamount = request.POST.get('textfield2', '')
        Balanceamount = request.POST.get('textfield3', '')

        paycard.objects.filter(id=id).update(Custid=Custid,Month=Month,Date=Date,Recivedamount=Recivedamount,Balanceamount=Balanceamount)
        user_item=paycard.objects.all()
    return render(request,'paycardview.html',context={'user_dict': user_item})

def paycardview(request):
    user_dict=paycard.objects.all()
    userdata=bookingdetails.objects.all()
    print(userdata)
    for i in userdata:
        print(i.guestid)
    #user_dict={'users':user_list}
    return render(request,'paycardview.html',{'user_dict':user_dict,'userdata':userdata})

def paycardedit(request):
    user_dict=paycard.objects.all()
    #user_dict={'users':user_list}
    return render(request,'paycardedit.html',{'user_dict':user_dict})

def paycard_remove(request):
    if request.method == 'POST':
        userdata=paycard.objects.all()
        id=request.POST.get('id')
        useritem=paycard.objects.get(id=id)

        useritem.delete()
        user_item = paycard.objects.all()
    return render(request,'paycardview.html',context={'user_dict':user_item})

def update_items(request):
    if request.method == 'POST':
        userdata=paycard.objects.all()
        id=request.POST.get('id')
        useritem=paycard.objects.filter(id=id).values()
        #print(useritem)
        return render(request,'paycardedit.html',{'useritem':useritem})

def payment_card(request):
    now=datetime.datetime.now()
    m=now.month
    guestdata=bookingdetails.objects.all()
    if request.method == "POST":
        Custid=request.POST.get('select')
        print(Custid)
        Month = request.POST.get('mm')
        Date = request.POST.get('datefield','')
        Recivedamount = request.POST.get('textfield','')
        Balanceamount = request.POST.get('textfield2','')

        paycard.objects.create(Custid=Custid,Month=Month,Date=Date,Recivedamount=Recivedamount,Balanceamount=Balanceamount)

    return render(request,'payment_card.html',{'m':m,'guestdata':guestdata})

def guest_home(request):
    return render(request,'guest_home.html')

def admin_home(request):
    return render(request,'admin_home.html')

def book_pg(request):
    if request.method == 'POST':
        cat= request.POST.get('t6','')
        print(cat)
        user_dict = PGdetails.objects.filter(categories=cat).values()
        for item in user_dict:
            print(item)
        print(user_dict)
        #bookdata=list(bookingdetails.objects.filter(roomno='2')|filter(roomno='3').aggregate(Count('roomno')).values())[0]
        #b=bookdata[0]
        return render(request,'book_pg2.html',{'user_dict' : user_dict})

    return render(request,'book_pg.html')

def book_status(request):
    username=request.session['username']
    if request.method=="POST":
        guestid=request.POST.get('t1','')

        guestdata=bookingdetails.objects.filter(guestid=guestid).values()
        for g in guestdata:
            bookstatus=g['book_status']
            amount=int(g['totcost'])
            gid=g['guestid']
            roomno=g['roomno']
            return render(request,'book_status2.html',{'bstatus':bookstatus,'amount':amount,'gid':gid,'roomno':roomno})

    return render(request,'book_status.html',{'u':username})

def payment(request):
    username=request.session['username']
    if request.method=="POST":
        tot=request.POST.get('amt')
        amt=int(tot)
        gid=request.POST.get('gid')
        roomno=request.POST.get('roomno')
        now=datetime.datetime.now()
        date=now.strftime("%Y-%m-%d")

        custpayment.objects.create(custid=username,guestid=gid,payamount=amt,paydate=date,roomno=roomno)
        return render(request,'payment2.html',{'amount':amt})

def bill_generate(request):
    username=request.session['username']
    cname=""
    if request.method=="POST":
        #userdict=custpayment.objects.all()
        userdict=bookingdetails.objects.order_by('-id')[:1]
        custname=Registration.objects.filter(emailid=username).values()
        for uname in custname:
            cname=uname['Fname']
        return render(request,'bill_generate.html',{'userdict':userdict,'cname':cname})


def paymentcardguest(request):
    user_dict = paycard.objects.all()
    return render(request,'paymentcardguest.html',{'user_dict':user_dict})

def paycard_search(request):
    if request.method=="POST":

        search=request.POST.get('search')
        paycard_search=paycard.objects.filter(Custid=search).values()
        guestdata=Guestdetails.objects.all()
        return render(request,'payment_card.html',{'paycard_search':paycard_search,'guestdata':guestdata})


def booking_form(request):
    num = random.randint(1, 200)
    username=request.session['username']
    #gid= list(Guestdetails.objects.aggregate(Max('PGid')).values())[0]
    #gid= Guestdetails.objects.aggregate(Max('PGid')).values()
    #ggid=gid[0]

    if request.method == 'POST':
        rmno=request.POST.get('rmno')
        now=datetime.datetime.now()
        ddate=now.strftime("%Y-%m-%d")
        return render(request,'booking_form.html',{'rmno':rmno,'ddate':ddate,'gid':username,'num':num})
    return render(request,'booking_form.html')  


def booking_form_next(request):
    if request.method=="POST":
        guestid = request.POST.get('t1', '')
        bookdate = request.POST.get('t3', '')
        roomtype = request.POST.get('t4', '')
        totcost = request.POST.get('t5')
        advpay = request.POST.get('t6', '')
        bal = request.POST.get('t7', '')
        roomno = request.POST.get('t8', '')
        now=datetime.datetime.now()
        amonth=now.month
        ayear=now.year
        check = bookingdetails.objects.filter(roomno=roomno).count()
        if check >= 1:
            return render(request,'book_pg.html',{'msg':'Already booked please check other room'})
        else:
            bookingdetails.objects.create(guestid=guestid, advancepayment=advpay, bookeddate=bookdate, balance=bal,roomno=roomno,roomtype=roomtype, totcost=totcost,book_status='booked',amonth=amonth,ayear=ayear)
            return render(request,'payment2.html',{'amount':advpay})




def guestsearch(request):
    gname=""
    roomno=""
    if request.method == 'POST':
        id= request.POST.get('search')
        print(id)
        gdata=bookingdetails.objects.filter(guestid=id).values()
        for guest in gdata:
            gname=guest['guestid']
            roomno=guest['roomno']
            guest_data=paycard.objects.filter(Custid=id).values()
            return render(request,'paycardview.html',{'guest_data':guest_data,'roomno':roomno,'gname':gname})
    return render(request,'paycardview.html')


def expense_db(request):
    if request.method == 'POST':
        userdata=expensee.objects.all()
        expensetype = request.POST.get('t1', '')
        expensename = request.POST.get('t2', '')
        expensedate = request.POST.get('datefield', '')
        month = request.POST.get('t4', '')
        amount = request.POST.get('t5', '')

        expense.objects.filter(id=id).update(expense_type=expensetype,expense_name=expensename,edate=expensedate,month_of_exp=month,amount=amount)
        user_item=expensee.objects.all()
    return render(request,'expenseview.html',context={'user_dict': user_item})

def expense_delete(request):
    if request.method == 'POST':
        userdata=expensee.objects.all()
        id=request.POST.get('id')
        useritem=expensee.objects.get(id=id)
        useritem.delete()
        user_item = expensee.objects.all()
    return render(request,'expenseview.html',context={'user_dict':user_item})

def expense_update(request):
    if request.method == 'POST':
        userdata=expensee.objects.all()
        id=request.POST.get('id')
        useritem=expensee.objects.filter(id=id).values()
        #print(useritem)
        return render(request,'expenseedit.html',{'useritem':useritem})

def expense(request):
    if request.method == "POST":

        expensetype = request.POST.get('t1', '')
        expensename = request.POST.get('t2', '')
        expensedate = request.POST.get('t3')

        amount = request.POST.get('t5', '')
        now=datetime.datetime.now()
        ayear=now.year
        month=now.month


        Expense = expensee.objects.create(expense_type=expensetype,expense_name=expensename,edate=expensedate,month_of_exp=month,amount=amount,ayear=ayear)
        Expense.save()
    return render(request,'expense.html')

def expenseview(request):
    user_dict = expensee.objects.all()
    # user_dict={'users':user_list}
    return render(request,'expenseview.html', {'user_dict': user_dict})

def expenseedit(request):
    user_dict = expensee.objects.all()
    #user_dict={'users':user_list}
    return render(request,'expenseedit.html',{'user_dict':user_dict})

def feedback(request):
    username=request.session['username']
    gid=""
    udata=custpayment.objects.filter(custid=username).values()
    for uu in udata:
        gid=uu['guestid']
        print(gid)
    if request.method=="POST":
        guestid=request.POST.get('t1','')
        pgid=request.POST.get('t2','')
        ratings=request.POST.get('t3','')
        comments=request.POST.get('t4','')
        custfeedback.objects.create(PGid=pgid,custid=guestid,ratings=ratings,comments=comments)
        return render(request,'guest_home.html')
    return render(request,'feedback.html',{'usern':username})

def monthly_report(request):

    if request.method=="POST":

        tot=0
        total=0
        bal=0
        grandtotal=0
        m=request.POST.get('t1','')
        expensedata=expensee.objects.filter(month_of_exp=m).values()
        for nn in expensedata:
            tot=tot+int(nn['amount'])
        monthlydata=paycard.objects.filter(Month=m).values()
        for mm in monthlydata:
            total=total+int(mm['Recivedamount'])
            bal=bal+int(mm['Balanceamount'])
            grandtotal=total-tot
            return render(request,'monthly_report.html',{'monthlydata':monthlydata,'total':total,'bal':bal,'tot':tot,'grandtotal':grandtotal})

    return render(request,'monthly_report.html')


def yearly_report(request):

    if request.method=="POST":

        tot=0
        total=0
        bal=0
        grandtotal=0
        m=request.POST.get('t1','')
        expensedata=expensee.objects.filter(ayear=m).values()
        for nn in expensedata:
            tot=tot+int(nn['amount'])
        yearlydata=paycard.objects.filter(ayear=m).values()
        for mm in yearlydata:
            total=total+int(mm['Recivedamount'])
            bal=bal+int(mm['Balanceamount'])
            grandtotal=total-tot
            return render(request,'yearly_report.html',{'yearlydata':yearlydata,'total':total,'bal':bal,'tot':tot,'grandtotal':grandtotal})

    return render(request,'yearly_report.html')

def reviews(request):
    user_dict=custfeedback.objects.all()
    return render(request,'reviews.html',{'user_dict':user_dict})



