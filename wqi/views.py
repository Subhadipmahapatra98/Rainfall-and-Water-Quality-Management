from cmath import cos
from distutils.log import error
import email
from click import confirm
from django.shortcuts import redirect, render,HttpResponse
import pickle
import joblib
from matplotlib.style import available, use
import numpy as np
import random
import pandas as pd
import pyowm, datetime
import requests
import os
import time
import datetime
from time import mktime
import math
import time
import datetime
from datetime import date,timedelta
from water.models import User, User_details, Product,NewOrder, Querry
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import date
import time
import datetime
from time import mktime
from datetime import datetime
import smtplib

api_key = "46ebe6e9b97d08784d31e660bcd5d5a0"     #your API Key here as string
owm = pyowm.OWM( api_key ).weather_manager()     # Use API key to get data

def home(request):
	if request.POST:
		fullname = request.POST['fullname']
		email = request.POST['email']
		mobileno = request.POST['mobileno']
		messages = request.POST['messages']
		querry_user = Querry(fullname=fullname,email=email,mobile = mobileno,messages=messages)
		querry_user.save()
		return redirect('/')
	return render(request, 'indexnew.html')
@login_required(login_url='/login')
def main(request):
	if request.POST:
		fullname = request.POST['fullname']
		email = request.POST['email']
		mobileno = request.POST['mobileno']
		messages = request.POST['messages']
		querry_user = Querry(fullname=fullname,email=email,mobile = mobileno,messages=messages)
		querry_user.save()
		return redirect('/main')
	return render(request, 'index.html')
def rainfall(request):
	result = None
	if request.method=='POST':
		city = request.POST['city']		
		complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key
		api_link = requests.get(complete_api_link)
		api_link_=str(api_link)
		if api_link_=="<Response [404]>":
			print("Error is :- ",api_link)
			result="City not found, please try again !!!"
			return render(request,'rainfall.html',{'result':result})
		api_data = api_link.json()
		weather_api = owm.weather_at_place(city)
		weather_data = weather_api.weather 
		rainfall = weather_data.rain
		if rainfall:
			Rainfall=1
		else:
			Rainfall = 0
		if api_data['cod'] == '404' :
			print ( "Invalid City : () , Please check you City name".format (city))
		else :
			Min_Temperature=((api_data ['main'] ['temp_min'])-273.15)
			Max_Temperature=((api_data ['main'] ['temp_max'])-273.15)
			Wind_dir=(api_data['wind']['deg'])
			Wind_speed=( api_data ['wind']['speed'])
			Humidity = (api_data ['main'] ['humidity'])
			pressure=(api_data ['main'] ['pressure'])
			cloud=(api_data ['clouds'] ['all'])
			temp_city = ((api_data['main']['temp'])-273.15)
			Sunset=(api_data['sys']['sunset'])
			Sunrise=(api_data['sys']['sunrise'])
			sunrisetime=(datetime.fromtimestamp(Sunrise).strftime("%I.%M"))
			sunsettime=(datetime.fromtimestamp(Sunset).strftime ("%I:%M"))
		
		data = np.array([[Max_Temperature,Min_Temperature,Rainfall,Humidity,sunrisetime,Wind_dir,Wind_speed,Wind_speed,Wind_speed,Wind_speed,Wind_speed,Wind_speed,Humidity,Humidity,pressure,pressure,cloud,cloud,temp_city,temp_city]])
		print(Max_Temperature)
		# load the model from disk
		loaded_model = joblib.load('cat.pkl')
		output = loaded_model.predict(data)
		print(output)
		print(city)
		if output==0:
			result = "It will not rain tomorrow."
		else:
			result = "It will rain tomorrow."
		print(result)

	return render(request, 'rainfall.html',{'result':result})
	
my_dict={'element':None}
def rfvisualization(request):
	return render(request,'df.html')
def wqi(request):
	if request.method=='POST':
		temperature=request.POST['temperature']
		dissolvedoxy=request.POST['dissolvedoxy']
		ph=request.POST['ph']
		bio=request.POST['bio']
		faecal=request.POST['faecal']
		nitrate=request.POST['nitrate']
		coliform=request.POST['coliform']
		total_col=request.POST['total_col']
		conductivity=request.POST['conductivity']
		if((temperature=="") and (dissolvedoxy=="")and (ph=="")and (bio=="")and (dissolvedoxy=="")and (faecal=="")and (nitrate=="")and (coliform=="")and (total_col=="")and (conductivity=="")):
			wqi="Please provide all the details correctly"
			return render(request,'wqi.html',{'result':wqi})
		model=pickle.load(open('WQI_model.pkl','rb'))
		sc=pickle.load(open('scaler.pkl','rb'))
		arr=np.array([temperature,dissolvedoxy,ph,bio,faecal,nitrate,coliform,total_col,conductivity]).reshape(1,-1)
		arr=sc.transform(arr)
		# print(arr)
		pred=model.predict(arr)
		my_dict['element']=pred[0]
		output_ = int(my_dict['element'])
		if output_ == 0:
			wqi = "Excellent"
		elif output_ == 1:
			wqi = "Very Good"
		elif output_ == 2:
			wqi = "Good"
		elif output_ == 3:
			wqi = "Bad"
		elif output_ == 4:
			wqi = "Not Drinkable"
		else:
			output_ = None
		my_dict['element'] = wqi
		print(my_dict['element'])
	return render(request,'wqi.html',context=my_dict)

def wqivisualization(request):
	return render(request,'waterIndex.html')


def login_call(request):
	if request.POST:
		unam = request.POST['uname']
		pas = request.POST['pas']
		currentUser=authenticate(username=unam,password=pas)
		if currentUser:
			print(currentUser)
			login(request,currentUser)
			if currentUser.is_superuser ==True:
				return redirect('/superadmin')
			else:
				return redirect('/main')
		else:
			message = "incorrect password or username"
			return render(request, 'login.html',{"message":message})
	return render(request,'login.html')



def reg(request):

	if request.POST:
		fullname = request.POST['name']
		uname = request.POST['uname']
		email = request.POST['email']
		mob = request.POST['mobno']
		address=request.POST['address']
		password = request.POST['password']
		c_password = request.POST['cpass']
		if password == c_password:
			data= User(username=uname,password=make_password(password),first_name=fullname,email=email)
			data.save()
			additional= User_details(user=data,address=address,mobile=mob)
			additional.save()
			return redirect('/login')
		else:
			message = "Both passwords are not same..."
			return render(request, 'Registration.html',{'message':message})

	return render(request,'Registration.html')

@login_required(login_url='/login')
def logout_call(request):
	logout(request)
	return redirect('/')

@login_required(login_url='/login')
def userbuy(request):
	card = Product.objects.all()
	return render(request,'userbuy.html',{'product': card})
@login_required(login_url='/login')
def order(request,id):

	if request.POST:
		name = request.POST['fullname']
		email = request.POST['email']
		pnum = request.POST['pnum']
		pin = request.POST['pin']
		state = request.POST['state']
		city = request.POST['city']
		houseno = request.POST['houseno']
		landmark = request.POST['landmark']
		qty = request.POST['qty']
		qty = int(qty)
		water = Product.objects.get(id=id)
		cost = int(water.cost)
		totalcost = qty * cost
		print(totalcost)
		import time
		import datetime
		from datetime import date,timedelta
		if int(qty)>int(water.available):
			return redirect('/order/{}'.format(id))
		dt=datetime.datetime.today()
		exp_Date = dt+datetime.timedelta(days=5)
		exp_Date = str(exp_Date.date())
		uObj=User_details.objects.get(user__username=request.user)
		neworder = NewOrder(user=uObj,water=water,quantity=qty,fullname=name,email=email, pnum=pnum,pin=pin,state=state,city=city,houseno=houseno,landmark=landmark, totalcost=totalcost, confirmation='Pending',status="Order placed",expected_date=exp_Date)
		neworder.save()
		Product.objects.filter(id=id).update(available=int(water.available) - int(qty))

		#SMTP
		sender_email = "mahapatrasubhadip0@gmail.com"
		rec_email = email
		password = "bqzclinvalxmxdar"
		SUBJECT = "Your New Order Details | WQI"
		TEXT ="Hi {}, \nWe have received you order. Please wait for some time, admin will verify your product and approve it. \nThanks and Regards, \nWQI".format(name)
		message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login(sender_email,password)
		print("password")
		server.sendmail(sender_email,rec_email,message)

		return redirect('/payment')
	return render(request,'addaddress.html',{'pdid':id})

@login_required(login_url='/login')
def payment(request):
	uObj=User_details.objects.get(user__username=request.user)
	orderdetails = NewOrder.objects.filter(user=uObj)
	totalcost = 0
	for i in orderdetails:
		totalcost = i.totalcost
	print(totalcost)
	if request.POST:
		return render(request,'orderdone.html',{'user':uObj,'totalcost':totalcost})
	return render(request,"payment.html",{'user':uObj,'totalcost':totalcost})

@login_required(login_url='/login')
def orderdetails(request):
	uObj=User_details.objects.get(user__username=request.user)
	order_details = NewOrder.objects.filter(user = uObj)
	print(order_details)
	return render(request, 'orderdetails.html',{'order_details':order_details})

@login_required(login_url='/login')
def contact(request):
	if request.POST:
		fullname = request.POST['fullname']
		email = request.POST['email']
		mobileno = request.POST['mobileno']
		messages = request.POST['messages']
		querry_user = Querry(fullname=fullname,email=email,mobile = mobileno,messages=messages)
		querry_user.save()
		return redirect('/main')

	return render(request,'contact.html')

@login_required(login_url='/login')
def superadmin(request):
	orders_data = NewOrder.objects.all()
	
	total = 0
	for i in orders_data:
		total = total + 1

	pending_orders = 0
	orders_data = NewOrder.objects.filter(confirmation='Pending')
	for i in orders_data:
		pending_orders = pending_orders + 1
	
	delivered_orders = 0
	orders_data = NewOrder.objects.filter(confirmation='Delivered')
	for i in orders_data:
		delivered_orders = delivered_orders + 1

	available = 0
	water = Product.objects.all()
	for i in water:
		available = int(i.available) + available
	
	deleted_orders = 0
	orders_data = NewOrder.objects.filter(confirmation='Deleted')
	for i in orders_data:
		deleted_orders = deleted_orders + 1
	
	
	return render(request,'adminhome.html',{'total':total,'pending_orders':pending_orders,'deleted_orders':deleted_orders,'delivered_orders':delivered_orders,'available':available})

@login_required(login_url='/login')
def adminneworder(request):
	neworder = NewOrder.objects.filter(confirmation='Pending')
	return render(request,'adminneworder.html',{'neworder':neworder})

@login_required(login_url='/login')
def adminconfirmed(request):
	confirmed = NewOrder.objects.filter(confirmation='Confirmed')
	return render(request,'adminconfirmed.html',{'confirmed':confirmed})

@login_required(login_url='/login')
def admindeleted(request):
	deleted = NewOrder.objects.filter(confirmation='Deleted')
	return render(request,'admindeleted.html',{'deleted':deleted})
@login_required(login_url='/login')
def admindelivered(request):
	delivered = NewOrder.objects.filter(confirmation='Delivered')
	return render(request,'admindelivered.html',{'delivered':delivered})

@login_required(login_url='/login')
def admindelete(request,id):
	current_order = NewOrder.objects.filter(id=id).update(confirmation='Deleted')
	current_order = NewOrder.objects.filter(id=id).update(status='Order not placed')
	user_order = NewOrder.objects.get(id=id)
	print(user_order)
	#SMTP
	sender_email = "mahapatrasubhadip0@gmail.com"
	rec_email = user_order.email
	password = "bqzclinvalxmxdar"
	SUBJECT = "Your Current Order Update | WQI"
	TEXT ="Hi {}, \nDue to some technical reason, your order (id= {}) can't be accepted. Please see you order detils on website. \nThanks and Regards, \nWQI".format(user_order.fullname,id)
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(sender_email,password)
	print("password")
	server.sendmail(sender_email,rec_email,message)
	return redirect('/admindeleted')

#Delivering the product page
@login_required(login_url='/login')
def delivering(request):
	confirmed = NewOrder.objects.filter(confirmation='Confirmed')
	return render(request,'deliveringproduct.html',{'confirmed':confirmed})
#Delivering the product
@login_required(login_url='/login')
def admindelivering(request,id):
	current_order = NewOrder.objects.filter(id=id).update(confirmation='Delivered')
	current_order = NewOrder.objects.filter(id=id).update(status='Delivered')
	user_order = NewOrder.objects.get(id=id)
	#SMTP
	sender_email = "mahapatrasubhadip0@gmail.com"
	rec_email = user_order.email
	password = "bqzclinvalxmxdar"
	SUBJECT = "Your Current Order Update | WQI"
	TEXT ="Hi {}, \nCongratulations!\nyour order (id= {}) has been delivered by WQI team at {}. Please see you order detils on website. \nThanks and Regards, \nWQI".format(user_order.fullname,id,user_order.city)
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(sender_email,password)
	print("password")
	server.sendmail(sender_email,rec_email,message)
	return redirect('/admindelivered')

@login_required(login_url='/login')
def adminapproved(request,id):
	current_order = NewOrder.objects.filter(id=id).update(confirmation='Confirmed')
	user_order = NewOrder.objects.get(id=id)
	#SMTP
	sender_email = "mahapatrasubhadip0@gmail.com"
	rec_email = user_order.email
	password = "bqzclinvalxmxdar"
	SUBJECT = "Your Current Order Update | WQI"
	TEXT ="Hi {}, \nGreetings from WQI!\nyour order (id= {}) has been accepted. Please see you order detils on website. \nThanks and Regards, \nWQI".format(user_order.fullname,id)
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(sender_email,password)
	print("password")
	server.sendmail(sender_email,rec_email,message)
	return redirect('/adminneworder')

def adminnewproduct(request):
	if request.method=='POST':
		Quality = request.POST['Quality']
		qty = request.POST['qty']
		qty = int(qty)
		address = request.POST['address']
		cost = request.POST['cost']
		cost = int(cost)
		prod = Product(quality = Quality, available = qty, address = address, cost=cost)
		prod.save()
		return redirect('/adminnewproduct')
	products = Product.objects.all()
	return render(request, 'adminnewproduct.html',{'products':products})