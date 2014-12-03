from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import Context
import datetime
import time
import json
import unicodedata
from django.db.models import Q
from MyApp.models import *
#import khayyam
#from dateutil import tz
project_counter=0
task_counter=0


def register(request):
	print "-------------------------------------------"
	print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
	#from_zone = tz.gettz('UTC')
	#to_zone = tz.gettz('Asia/Tehran')
	#utc = datetime.datetime.now()
	#lcl = utc.astimezone(to_zone)
	#print khayyam.JalaliDatetime.now().strftime("%C")
	if request.method == "POST":
		print 'register- post mode'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		name=unicodedata.normalize('NFKD', request.POST['name']).encode('utf-8','ignore');
		print name
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

		
		lst=[]
		
		for pro in Profile.objects.filter(username__iexact=username):
	
			project=Projects.objects.get(id__iexact=pro.projectID)
			project.pDeadline=str(project.pDeadline)
			
			task=[]
			for t in Task.objects.filter(Q(projectID__iexact=pro.projectID) & Q(username__iexact=username)):
				t.deadline=str(t.deadline)
				tmp1=t.as_json()
				del tmp1["task_info"]
				del tmp1["deadline"]
				del tmp1["status"]
				del tmp1["projectID"]
				del tmp1["username"]
				task.append(tmp1)

			temp=project.as_json()
			del temp["pDeadline"]
			del temp["progress"]
			del temp["managerName"]
			del temp["managerUser"]
			del temp["project_info"]
				
			temp["tasks"]=task
			lst.append(temp)
			
		results["projects"]=lst	
		


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
	t=datetime.datetime.now()
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


			
				lst=[]
				
				for pro in Profile.objects.filter(username__iexact=username):
	
					project=Projects.objects.get(id__iexact=pro.projectID)
					project.pDeadline=str(project.pDeadline)
					
					task=[]
					for t in Task.objects.filter(Q(projectID__iexact=pro.projectID) & Q(username__iexact=username)):
						t.deadline=str(t.deadline)
						tmp1=t.as_json()
						del tmp1["task_info"]
						del tmp1["deadline"]
						del tmp1["status"]
						del tmp1["projectID"]
						del tmp1["username"]
						task.append(tmp1)
					temp=project.as_json()
					del temp["pDeadline"]
					del temp["progress"]
					del temp["managerName"]
					del temp["managerUser"]
					del temp["project_info"]
			

					temp["tasks"]=task
					lst.append(temp)
				
				"""
				for pro in Profile.objects.filter(username__iexact=username):
					project=Projects.objects.get(id__iexact=pro.projectID)
					project.pDeadline=str(project.pDeadline)
					lst.append(project.as_json())
				
				"""
				results["projects"]=lst
			

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
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-profile'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		results ={}
		lst=[]

		for pro in Profile.objects.filter(username__iexact=username):
	
			project=Projects.objects.get(id__iexact=pro.projectID)
			project.pDeadline=str(project.pDeadline)
			
			task=[]
			for t in Task.objects.filter(Q(projectID__iexact=pro.projectID) & Q(username__iexact=username)):
				t.deadline=str(t.deadline)
				tmp1=t.as_json()
				del tmp1["task_info"]
				del tmp1["deadline"]
				del tmp1["status"]
				del tmp1["projectID"]
				del tmp1["username"]
				task.append(tmp1)

			temp=project.as_json()
			del temp["pDeadline"]
			del temp["progress"]
			del temp["managerName"]
			del temp["managerUser"]
			del temp["project_info"]
			
			
			
			
			temp["tasks"]=task
			lst.append(temp)
			
			
		results["projects"]=lst
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
			lst.append(Login.objects.get(username__iexact=pro.username).as_json())
		
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


def taskInfo(request):

	print "-------------------------------------------"
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-taskInfo'
		taskID=int(unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore'));
		
		results ={}
		results["successful"]="true"
		task_info=Task.objects.get(id__iexact=taskID)
		task_info.deadline=str(task_info.deadline)
		
		results["taskInfo"]=task_info.as_json()
			
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
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-addMember'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		for obj in Profile.objects.filter(username__iexact=username):
			#print type(obj.projectID)
			#print type(projectID)
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
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-addProject'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		projectName=unicodedata.normalize('NFKD', request.POST['projectName']).encode('utf-8','ignore');
		project_info=unicodedata.normalize('NFKD', request.POST['project_info']).encode('utf-8','ignore');
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');
		
		pDeadline= datetime.date(int(year),int(month),int(day))


		managerName=Login.objects.get(username__iexact=username).name
		#print project_counter
		#project_counter += 1
		results ={}
		results["successful"]="true"

		newProject=Projects(projectName=projectName, managerUser=username, managerName=managerName, project_info=project_info,progress=0, pDeadline=pDeadline)
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
	t=datetime.datetime.now()
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
		
		deadline= datetime.date(int(year),int(month),int(day))
		print Login.objects.filter(username__iexact=username).exists()
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

			newTask=Task(taskName=taskName,task_info=task_info, projectID=projectID,username=username,deadline=deadline,status='1')
			newTask.save()

			
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
	t=datetime.datetime.now()
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
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-edit project'
		projectID=int(unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore'));
		projectName=unicodedata.normalize('NFKD', request.POST['projectName']).encode('utf-8','ignore');
		project_info=unicodedata.normalize('NFKD', request.POST['project_info']).encode('utf-8','ignore');
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');
		
		pDeadline= datetime.date(int(year),int(month),int(day))
		results ={}
		print projectID
		
		Projects.objects.get(id__exact=projectID).update(projectName=projectName,project_info=project_info,pDeadline=pDeadline)	

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
	t=datetime.datetime.now()
	print t.isoformat()

	if request.method == "POST":
		print 'POST-edit task'
		taskID=int(unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore'));
		taskName=unicodedata.normalize('NFKD', request.POST['taskName']).encode('utf-8','ignore');
		task_info=unicodedata.normalize('NFKD', request.POST['task_info']).encode('utf-8','ignore');
		year=unicodedata.normalize('NFKD', request.POST['year']).encode('utf-8','ignore');
		month=unicodedata.normalize('NFKD', request.POST['month']).encode('utf-8','ignore');
		day=unicodedata.normalize('NFKD', request.POST['day']).encode('utf-8','ignore');
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		
		deadline= datetime.date(int(year),int(month),int(day))
		results ={}
		print projectID
		
		Projects.objects.get(id__exact=taskID).update(taskName=taskName,task_info=task_info,deadline=deadline,username=username)	

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
	
