from django.db import models

# Create your models here.
class Registration(models.Model):
    Fname =models.CharField(max_length=200)
    Lname=models.CharField(max_length=200)
    emailid=models.EmailField(max_length=200)
    Password=models.CharField(max_length=200)
    Confirmpass=models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

class Login(models.Model):
    Emailid=models.EmailField(max_length=200)
    Password=models.CharField(max_length=200)
    type=models.CharField(max_length=50)


class PGdetails(models.Model):
    pgid=models.CharField(max_length=50)
    pgname=models.CharField(max_length=200)
    pgaddress=models.CharField(max_length=200)
    pglocation=models.CharField(max_length=200)
    categories=models.CharField(null=True,blank=True,max_length=200)
    contactdetails=models.CharField(max_length=200)
    image1 = models.FileField(upload_to='documents/')
    image2 = models.FileField(upload_to='documents/')
    room_no=models.IntegerField(blank=True,null=True)
    occupants=models.IntegerField(blank=True,null=True)
    

class Guestdetails(models.Model):
    Date= models.DateField()
    PGid=models.CharField(null=True,blank=True,max_length=200)
    Custid=models.IntegerField(null=True,blank=True)
    Bookid=models.CharField(null=True,blank=True,max_length=200)
    Studentname=models.CharField(null=True,blank=True,max_length=200)
    Mobilenumber=models.CharField(null=True,blank=True,max_length=11)
    Permanentaddress=models.CharField(null=True,blank=True,max_length=200)
    State=models.CharField(null=True,blank=True,max_length=200)
    City=models.CharField(null=True,blank=True,max_length=200)
    Roomno=models.CharField(null=True,blank=True,max_length=200)
    studenttype=models.CharField(null=True,blank=True,max_length=200)
    Depositamount=models.IntegerField(null=True,blank=True)

class paycard(models.Model):
    Custid = models.CharField(null=True,blank=True,max_length=200)
    Month = models.IntegerField(null=True,blank=True)
    Date = models.DateField(null=True,blank=True)
    Recivedamount = models.IntegerField(null=True,blank=True)
    Balanceamount = models.IntegerField(null=True,blank=True)
    ayear=models.IntegerField(null=True,blank=True)

class custfeedback(models.Model):
    PGid=models.CharField(null=True,blank=True,max_length=200)
    custid=models.CharField(null=True,blank=True,max_length=200)
    ratings=models.CharField(null=True,blank=True,max_length=200)
    comments=models.CharField(null=True,blank=True,max_length=200)

class custpayment(models.Model):
    custid=models.CharField(null=True,blank=True,max_length=200)
    guestid=models.IntegerField(null=True,blank=True)
    roomno=models.IntegerField(null=True,blank=True)
    payamount=models.IntegerField(blank=True,null=True)
    paydate=models.CharField(null=True,blank=True,max_length=100)


class bookingdetails(models.Model):
    guestid =models.CharField(max_length=200)
    pgid=models.CharField(max_length=200)
    bookeddate=models.CharField(max_length=100)
    roomtype=models.CharField(max_length=200)
    totcost=models.IntegerField(blank=True,null=True)
    advancepayment=models.CharField(max_length=200)
    balance = models.CharField(max_length=200)
    roomno=models.CharField(max_length=100)
    book_status=models.CharField(max_length=50,null=True,blank=True)
    amonth = models.IntegerField(blank=True, null=True)
    ayear = models.IntegerField(blank=True, null=True)


class expensee(models.Model):
    expense_type = models.CharField(max_length=100)
    expense_name = models.CharField(max_length=100)
    month_of_exp = models.IntegerField(null=True,blank=True)
    edate = models.DateField(null=True,blank=True)
    amount = models.IntegerField()
    ayear = models.IntegerField(null=True, blank=True)





