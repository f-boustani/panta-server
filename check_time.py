import threading
from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import Context
from datetime import *
import time
import json
import unicodedata
from django.utils import timezone
from django.db.models import Q
from MyApp.models import *
from gcm import *



def check_deadline():

	t_current=datetime.utcnow()+timedelta(minutes=210)
	t_current=(t_current - datetime(1970,1,1)).total_seconds()

	for task in Task.objects.all():

		if task.delta <= t_current and task.status=='0':

			print "task deadline is over!must send notif"

			# start sending notif to user
			msg1=Projects.objects.get(id_iexact=task.projectID).projectName
			msg2=Login.objects.get(username__iexact=task.username).name 
			manager=Projects.objects.get(projectID__iexact=task.projectID).managerUser

			task=task.as_json()
			del task["task_info"]
			del task["deadline"]
			del task["username"]
			del task["status"]

			task["managerUser"]=manager


			data1={'message':msg1,'msg_type':'5','task_info':task}
			data2={'message':msg2,'msg_type':'6','task_info':task}
			
			for obj in Gcm_users.objects.filter(username__iexact=task.username):
				user_reg_id=obj.reg_id
				
				#add api key
				gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")

				try:
				    canonical_id = gcm.plaintext_request(registration_id=user_reg_id, data=data1)
				    print canonical_id

				    if canonical_id:	
				    	print 'reg_id change,must replace'
				        
				        for entry in Gcm_users.objects.filter(registration_id=user_reg_id):
				        	entry.reg_id = canonical_id
				        	entry.save()

				except GCMNotRegisteredException:
				    print 'notregistered,Remove from db'
				    for entry in Gcm_users.objects.filter(registration_id=user_reg_id):
				       entry.delete()
				       
				except GCMUnavailableException:
				    print 'gcm unavailable,resend'



			for obj in Gcm_users.objects.filter(username__iexact=manager):
	
				manager_reg_id=obj.reg_id
				
				#add api key
				gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
				try:
				    canonical_id = gcm.plaintext_request(registration_id=manager_reg_id, data=data2)
				    print canonical_id

				    if canonical_id:	
				    	print 'reg_id change,must replace'
				        
				        for entry in Gcm_users.objects.filter(registration_id=manager_reg_id):
				        	entry.reg_id = canonical_id
				        	entry.save()

				except GCMNotRegisteredException:
				    print 'notregistered,Remove from db'
				    for entry in Gcm_users.objects.filter(registration_id=manager_reg_id):
				       entry.delete()
				       
				except GCMUnavailableException:
				    print 'gcm unavailable,resend'



	t = threading.Timer(70.0, check_deadline)
	t.start()  
	
#********************************************************************
def check_end_project():

	d_current=date.utcnow()+timedelta(minutes=210)
	d_current=(d_current - datetime(1970,1,1)).days
	for pro in Projects.objects.all():

		if pro.pDelta <= d_current:

			print "project deadline is over! must send notif for pro"
			msg=pro.projectName
			data={'message':msg,'msg_type':'4'}

			for f in Profile.objects.filter(projectID__iexact=pro.id):
				for rec in Gcm_users.objects.filter(username__iexact=f.username):
					user_regID=rec.reg_id
				
					#add api key
					gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
					try:
				    canonical_id = gcm.plaintext_request(registration_id=user_regID, data=data)
				    print canonical_id

				    if canonical_id:	
				    	print 'reg_id change,must replace'
				        
				        for entry in Gcm_users.objects.filter(registration_id=user_regID):
				        	entry.reg_id = canonical_id
				        	entry.save()

				except GCMNotRegisteredException:
				    print 'notregistered,Remove from db'
				    for entry in Gcm_users.objects.filter(registration_id=user_regID):
				       entry.delete()
				       
				except GCMUnavailableException:
				    print 'gcm unavailable,resend'


	p = threading.Timer(86400.0, check_end_project)
	p.start()  
	

check_deadline()
check_end_project()

