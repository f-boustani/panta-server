from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import Context
from datetime import datetime,timedelta,date
import time
import json
import unicodedata
from django.utils import timezone
from django.db.models import Q
from MyApp.models import *
from gcm import *

def register(request):
	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'register- post mode'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		name=unicodedata.normalize('NFKD', request.POST['name']).encode('utf-8','ignore');

		if(Login.objects.filter(username__iexact=username).exists()):
			results ={}
			results["successful"]="false"
			results["error"]="exists"
			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response	

		#salt = bcrypt.gensalt()
		#hash = bcrypt.hashpw(password, salt)
		newUser=Login(username=username,password=password,name=name)
		newUser.save()
		results ={}
		results["successful"]="true"
		results["user_info"]= Login.objects.get(username__iexact=username).as_json()	


		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
	
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-register"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	elif request.method == "GET":
		print "GET MODE-register"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	else:
		return HttpResponseBadRequest()

def login(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()
     
	if request.method == "POST":
		print 'POST-login'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		#salt = bcrypt.gensalt()
		#hashpw(password, salt)
		
		if(Login.objects.filter(username__iexact=username).exists()):
			passwd=Login.objects.get(username__iexact=username).password.encode('utf-8','ignore');
			if(passwd==password):
				results ={}
				results["successful"]="true"
				results["user_info"]=Login.objects.get(username__iexact=username).as_json()	


				print json.dumps(results)
				response = HttpResponse(json.dumps(results), content_type="application/json")
				response['Access-Control-Allow-Origin'] = "*"
				response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
				response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
				return response
		results ={}	
		results["successful"]="false"
		results["error"]="incorrect"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response				

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-login"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	elif request.method == "GET":
		print "GET MODE-login"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	else:
		return HttpResponseBadRequest()


def view_profile(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-profile'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		print 'username: ', username
		results ={}
		results["successful"]="true"
		lst=[]

		for pro in Profile.objects.filter(username__iexact=username):
	
			project=Projects.objects.get(id__iexact=pro.projectID)
			project.pDeadline=str(project.pDeadline)
			
			task=[]
			for t in Task.objects.filter(Q(projectID__iexact=pro.projectID) & Q(username__iexact=username)):
				t.deadline=str(t.deadline)
				tmp1=t.as_json()
				del tmp1["task_info"]
				del tmp1["status"]
				del tmp1["projectID"]
				del tmp1["username"]
				task.append(tmp1)

			temp=project.as_json()
			del temp["progress"]
			del temp["project_info"]
			
			
			
			
			temp["tasks"]=task
			lst.append(temp)
			
			
		results["projects"]=lst
		results["username"]=username
		#print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-login"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	elif request.method == "GET":
		print "GET MODE-login"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	else:
		return HttpResponseBadRequest()

'''    

def projectInfo(request):

	print "-------------------------------------------"
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-projectInfo'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));

		results ={}
		results["successful"]="true"
		project_info=Projects.objects.get(id__iexact=projectID)
		project_info.pDeadline=str(project_info.pDeadline)
		results["projectInfo"]=project_info.as_json()

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-projectInfo"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode-projectInfo"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


'''

def project_users(request):

	print "-------------------------------------------"
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-project_users'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));

		results ={}
		results["successful"]="true"
		lst=[]
		for pro in Profile.objects.filter(projectID__iexact=projectID):

			a=Login.objects.get(username__iexact=pro.username).as_json()
			del a["password"]
			lst.append(a)
		
		results["project_users"]=lst
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-project_user"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode-project_user"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()

'''

def project_tasks(request):

	print "-------------------------------------------"
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-project_tasks'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));

		results ={}
		results["successful"]="true"
		lst=[]
		for task in Task.objects.filter(projectID__iexact=projectID):
			task.deadline = str(task.deadline)
			lst.append(task.as_json())
		
		results["project_tasks"]=lst
			
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- project_tasks"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - project_tasks"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()

'''

def project_all(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-project all'
		
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));

		print 'projectID: ',projectID
		results ={}
		results["successful"]="true"

		#data for project info
		project_info=Projects.objects.get(id__iexact=projectID)
		project_info.pDeadline=str(project_info.pDeadline)
		results["projectInfo"]=project_info.as_json()

		#data for project's users
		lst=[]
		for pro in Profile.objects.filter(projectID__iexact=projectID):
			a=Login.objects.get(username__iexact=pro.username).as_json()
			del a["password"]
			lst.append(a)
			
		results["project_users"]=lst
		

		#data for project's tasks
		lst2=[]
		for task in Task.objects.filter(projectID__iexact=projectID):
			task.deadline = str(task.deadline)
			lst2.append(task.as_json())
		
		results["project_tasks"]=lst2
			
			
		#print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode - peoject all"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - project all"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


def taskInfo(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-taskInfo'
		taskID=int(unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore'));
		
		results ={}
		proID=Task.objects.get(id__exact=taskID).projectID
		lst=[]
		for pro in Profile.objects.filter(projectID__iexact=proID):
			a=Login.objects.get(username__iexact=pro.username).as_json()
			del a["password"]
			lst.append(a)
			
		results["project_users"]=lst
		
		results["successful"]="true"
		task_info=Task.objects.get(id__iexact=taskID)
		username=task_info.username
		name=Login.objects.get(username__iexact=username).name
		task_info.deadline=str(task_info.deadline)
		t=task_info.as_json()
		t["name"]=name
		
		results["taskInfo"]=t
			
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode - taskInfo"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - taskInfo"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()



def addMember(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-addMember'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		for obj in Profile.objects.filter(username__iexact=username):
			if(obj.projectID==projectID):

				print "username is already added"
				results ={}
				results["successful"]="false"
				results["error"]="1"
				print json.dumps(results)
				response = HttpResponse(json.dumps(results), content_type="application/json")
				response['Access-Control-Allow-Origin'] = "*"
				response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
				response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
				return response


		if(Login.objects.filter(username__iexact=username).exists()):

			results ={}
			results["successful"]="true"
			newUser=Profile(username=username,projectID=projectID)
			newUser.save()

			print "must send notif"
			pro_name=Projects.objects.get(id__exact=projectID).projectName
			message='you are added to project '+ pro_name

			#save notif to notification table
			new_notif=Notification(username=username,msg=message)
			new_notif.save()

			for obj in Gcm_users.objects.filter(username__iexact=username):
	
				user_reg_id=obj.reg_id

				#msg_type=2 ---> add member
				data={'message':message,'msg_type':'2'}
				

				#add api key
				gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
				reg_id = user_reg_id

				gcm.plaintext_request(registration_id=reg_id, data=data)
				print 'notif sent'

				
			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

		else:

			print "username doesnt exist"
			results ={}
			results["successful"]="false"
			results["error"]="2"
			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response
			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- addMemeber"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - addMember"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()



def addProject(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-addProject'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		projectName=unicodedata.normalize('NFKD', request.POST['projectName']).encode('utf-8','ignore');
		project_info=unicodedata.normalize('NFKD', request.POST['project_info']).encode('utf-8','ignore');
		link=unicodedata.normalize('NFKD', request.POST['link']).encode('utf-8','ignore');		
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');		
		pDeadline= date(int(year),int(month),int(day))
		pDelta=(pDeadline - date(1970,1,1)).days



		managerName=Login.objects.get(username__iexact=username).name
		
		results ={}
		results["successful"]="true"

		newProject=Projects(projectName=projectName,pDelta=pDelta, managerUser=username, managerName=managerName, project_info=project_info,progress=0, pDeadline=pDeadline,link=link)
		newProject.save()
		lst=Projects.objects.all().order_by("-id")
		print lst
		projectID=lst[0].id

		newProfile=Profile(username=username , projectID= projectID)
		newProfile.save()
			
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- addProject"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - addProject"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


	

def addTask(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-addTask'
		projectID=unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore');
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		taskName=unicodedata.normalize('NFKD', request.POST['taskName']).encode('utf-8','ignore');
		task_info=unicodedata.normalize('NFKD', request.POST['task_info']).encode('utf-8','ignore');
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');
		hour=unicodedata.normalize('NFKD', request.POST['hour']).encode('utf-8','ignore');
		minute=unicodedata.normalize('NFKD', request.POST['minute']).encode('utf-8','ignore');
		
		print 'year: ',year, int(year)
		deadline= datetime(int(year),int(month),int(day),int(hour),int(minute))
		#deadline=timezone.make_aware(deadline, timezone.get_current_timezone())
		print 'deadline: ',deadline
		delta=(deadline - datetime(1970,1,1)).total_seconds()

		#print Login.objects.filter(username__iexact=username).exists()
		if not(Login.objects.filter(username__iexact=username).exists()):
			print "username doesnt exist"
			results ={}
			results["successful"]="false"
			results["error"]="1"
			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

		added=0
		for pro in Profile.objects.filter(projectID__iexact=projectID):
			if(pro.username==username):
				added=1
		
		if(added==0):
			print "username isnt added to this project"
			results ={}
			results["successful"]="false"
			results["error"]="2"
			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

		if(added==1):
			
			results ={}
			results["successful"]="true"

			
			newTask=Task(taskName=taskName,task_info=task_info,delta=delta, projectID=projectID,username=username,deadline=deadline,status='0')
			newTask.save()
			task=Task.objects.latest('id').as_json()
			

			#change progress
			a=Task.objects.filter(projectID=projectID)
			b=Task.objects.filter(projectID=projectID,status='2')
			progress=(float(len(b))/float(len(a)))*100
			p=Projects.objects.get(id__exact=projectID)
			p.progress=progress
			p.save()
			
			print "must send notif"
			pro_name=Projects.objects.get(id__exact=projectID).projectName
			message='A task is given to you in project '+ pro_name
			del task["taskName"]
			del task["task_info"]
			del task["deadline"]
			del task["username"]
			del task["status"]
			task["managerUser"]=Projects.objects.get(id__exact=projectID).managerUser

			#save notif to notification table
			new_notif=Notification(username=username,msg=message)
			new_notif.save()


			#msg_type=3 ---> add task	
			data={'message':message,'msg_type':'3','task_info':json.dumps(task)}
				

			for obj in Gcm_users.objects.filter(username__iexact=username):
	
				user_reg_id=obj.reg_id
				
				#add api key
				gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
				reg_id = user_reg_id

				gcm.plaintext_request(registration_id=reg_id, data=data)
				print 'notif sent'


			
			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

				
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- addTask"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - addTask"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()

	
def deleteProject(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-delete project'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		results ={}
		print projectID
		
		Projects.objects.get(id__exact=projectID).delete()	

		for obj in Profile.objects.filter(projectID__exact=projectID):
			obj.delete()

		for task in Task.objects.filter(projectID__exact=projectID):
			task.delete()

		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- deleteProject"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - deleteProject"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


def editProject(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-edit project'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		projectName=unicodedata.normalize('NFKD', request.POST['projectName']).encode('utf-8','ignore');
		project_info=unicodedata.normalize('NFKD', request.POST['project_info']).encode('utf-8','ignore');
		link=unicodedata.normalize('NFKD', request.POST['link']).encode('utf-8','ignore');
		
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');
		
		pDeadline= date(int(year),int(month),int(day))
		pDelta=(pDeadline - date(1970,1,1)).days
		results ={}
		print projectID
		print projectName
		print len(projectName)
		
		p=Projects.objects.get(id__exact=projectID)
		p.projectName=projectName
		p.project_info=project_info
		p.pDeadline=pDeadline
		p.pDelta=pDelta
		p.link=link
		p.save()

		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- editProject"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - editProject"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()
	



def editTask(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-edit task'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		
		taskID=int(unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore'));
		taskName=unicodedata.normalize('NFKD', request.POST['taskName']).encode('utf-8','ignore');
		task_info=unicodedata.normalize('NFKD', request.POST['task_info']).encode('utf-8','ignore');
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');
		hour=unicodedata.normalize('NFKD', request.POST['hour']).encode('utf-8','ignore');
		minute=unicodedata.normalize('NFKD', request.POST['minute']).encode('utf-8','ignore');
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		deadline= datetime(int(year),int(month),int(day),int(hour),int(minute))
		delta=(deadline - datetime(1970,1,1)).total_seconds()

		added=0
		for i in Profile.objects.filter(projectID__iexact=projectID):
			if(i.username==username):
				added=1

		if(added==1):
			results ={}
			print projectID
			
			t=Task.objects.get(id__exact=taskID)
			t.taskName=taskName
			t.task_info=task_info
			t.deadline=deadline
			t.delta=delta
			t.username=username
			t.save()

			results["successful"]="true"

			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

		if(added==0):
			print "this user is not a member of this project"
			results ={}
			results["successful"]="false"
			results["error"]="1"

			print json.dumps(results)
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- edit task"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - edit task"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()
	

def deleteMember(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-delete member'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		print "projectID: ",projectID
		print "username: ", username

		results={}
		Profile.objects.get(projectID__exact=projectID,username__exact=username).delete()
		
		for task in Task.objects.filter(projectID__exact=projectID):
			if task.username==username:
				task.delete()

		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- deleteMember"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - deleteMember"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


def deleteTask(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-delete task'
		taskID=int(unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore'));
		
		print "taskID: ", taskID

		projectID=Task.objects.get(id__exact=taskID).projectID
		Task.objects.get(id__iexact=taskID).delete()

		#change progress
		a=Task.objects.filter(projectID=projectID)
		b=Task.objects.filter(projectID=projectID,status='2')
		progress=(float(len(b))/float(len(a)))*100
		p=Projects.objects.get(id__exact=projectID)
		p.progress=progress
		p.save()

		results={}
		
		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- delete task"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - delete task"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()



def changeStatus(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-change status'
		taskID=int(unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore'));
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		status=unicodedata.normalize('NFKD', request.POST['status']).encode('utf-8','ignore');
		
		print "taskID: ", taskID
		print "projectID: ", projectID
		print "status: ", status

		t=Task.objects.get(id__exact=taskID)
		t.status=status
		t.save()


		#done by user, must notif the manager
		if status=='1':

			print 'must send notif to manager'
			manager_user=Projects.objects.get(id__exact=projectID).managerUser
			user_id=Task.objects.get(id__exact=taskID).username
			name=Login.objects.get(username__iexact=user_id).name

			message=name+' done his/her task'
			task_info=Task.objects.get(id__iexact=taskID)
			task_info.deadline=str(task_info.deadline)
			task_info=task_info.as_json()
			task_info['managerUser']=manager_user
			
			#save notif to notification table
			new_notif=Notification(username=manager_user,msg=message)
			new_notif.save()


			for obj in Gcm_users.objects.filter(username__iexact=manager_user):
					
				manager_reg_id=obj.reg_id

				
				#msg_type=1 ---> task done by user
				data={'message':message, 'task_info': json.dumps(task_info), 'msg_type':'1'}
				

				#add api key
				gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
				reg_id = manager_reg_id

				a=gcm.plaintext_request(registration_id=reg_id, data=data)
				print 'notif sent'
				print 'response',a

				if(a!=None):
					print 'reg_id changed!!'
					user_reg=Gcm_users.objects.get(username__iexact=manager_user,reg_id__iexact=reg_id)
					user_reg.reg_id=a
					user_reg.save()

				


		#accepted by manager
		if status=='2':

			a=Task.objects.filter(projectID=projectID)
			b=Task.objects.filter(projectID=projectID,status='2')
			progress=(float(len(b))/float(len(a)))*100
			p=Projects.objects.get(id__exact=projectID)
			p.progress=progress
			p.save()
			print "new progress: ",Projects.objects.get(id__exact=projectID).progress

				

		results={}
		
		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- delete task"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - delete task"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


def changePassword(request):
	
	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-change password'
		newPassword=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');

		u=Login.objects.get(username__iexact=username)
		u.password=newPassword
		u.save()	

		results={}
		
		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- change password"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - change password"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()




def deleteAccount(request):
	
	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-delete account'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		print "username: ", username

		Login.objects.get(username__iexact=username).delete()

		for obj in Profile.objects.filter(username__iexact=username):
			obj.delete()
		
		for t in Task.objects.filter(username__iexact=username):
			t.delete()
		
		for pro in Projects.objects.filter(managerUser__iexact=username):
			Profile.objects.filter(projectID=pro.projectID).delete()
			Task.objects.filter(projectID=pro.projectID).delete()
			pro.delete()


		results={}
		
		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- delete account"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - delete account"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()



def gcmDatabase(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-save to gcm database'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		reg_id=unicodedata.normalize('NFKD', request.POST['reg_id']).encode('utf-8','ignore');
		
		print "username: ", username
		print "reg_id: ",reg_id
		results={}

		if (reg_id==""):

			print 'reg_id is empty!!'
			results["successful"]= "false"
			results["error"]="reg_id is empty"
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response

		if (Gcm_users.objects.filter(username__iexact=username,reg_id__iexact=reg_id).exists()):
			print 'username & reg_id exists!!'
			results["successful"]= "false"
			results["error"]="username & reg_id exists"
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response




		new = Gcm_users(username=username,reg_id=reg_id)
		new.save()

		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode- gcm database"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - gcm database"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


def signOut(request):

	# when user sign out, clear the gcm record
	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST-sign out'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		reg_id=unicodedata.normalize('NFKD', request.POST['reg_id']).encode('utf-8','ignore');
		
		print "username: ", username
		print "reg_id: ",reg_id
		results={}
		
		if (reg_id==""):
			
			print 'reg_id is empty!!'
			results["successful"]= "true"
			results["error"]="reg_id is empty"
			response = HttpResponse(json.dumps(results), content_type="application/json")
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
			response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
			return response


		Gcm_users.objects.get(username__iexact=username,reg_id__iexact=reg_id).delete()

		results["successful"]="true"

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-sign out"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - sign out"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()


def getNotif(request):

	print "-------------------------------------------"
	t=datetime.utcnow()+timedelta(minutes=210)
	print t.isoformat()

	if request.method == "POST":
		print 'POST- get notifs'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		print "username: ", username
		
		results={}
		lst=[]
		for obj in Notification.objects.filter(username__iexact=username):
			
			obj=obj.as_json()
			lst.append(obj)


		results["successful"]="true"
		results["notification"]=lst

		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

			
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["successful"]="false"
		results["mode"]="option mode-sign out"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response
	elif request.method == "GET":
		print "GET MODE"
		results ={}
		results["successful"]="false"
		results["mode"]="get mode - sign out"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		response['Access-Control-Max-Age'] = "1800"
		return response

	else:
		return HttpResponseBadRequest()
