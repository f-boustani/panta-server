from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import Context
import datetime
import json
import unicodedata
from MyApp.models import *


def register(request):
	if request.method == "POST":
		print 'register- post mode'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		name=unicodedata.normalize('NFKD', request.POST['name']).encode('utf-8','ignore');
		if(Login.objects.filter(username__iexact=username).exists()):
			results ={}
			results["successful"]="false"
			results["err"]="exists"
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
		for ob in Profile.objects.filter(username__iexact=username):
			lst.append(Projects.objects.get(projectID__iexact=pro.projectID).as_json())
	
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
     
	if request.method == "POST":
		print 'POST-login'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		#salt = bcrypt.gensalt()
		#hash = bcrypt.hashpw(password, salt)
		
		if(Login.objects.filter(username__iexact=username).exists()):
			passwd=Login.objects.get(username__iexact=username).password.encode('utf-8','ignore');
			if(passwd==password):
				results ={}
				results["successful"]="true"
				lst=[]
				for pro in Profile.objects.filter(username__iexact=username):
					lst.append(Projects.objects.get(projectID__iexact=pro.projectID).as_json())
		
				results["projects"]=lst
				results["user_info"]=Login.objects.get(username__iexact=username).as_json()	
				
				print json.dumps(results)
				response = HttpResponse(json.dumps(results), content_type="application/json")
				response['Access-Control-Allow-Origin'] = "*"
				response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
				response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
				return response
		results ={}	
		results["successful"]="false"
		results["err"]="incorrect"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response				

	else:
		return HttpResponseBadRequest()


def view_profile(request):

	if request.method == "POST":
		print 'POST-profile'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		print username
		results ={}
		lst=[]
		for pro in Profile.objects.filter(username__iexact=username):
			lst.append(Projects.objects.get(projectID__iexact=pro.projectID).as_json())
			
		results["projects"]=lst
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response

	else:
		return HttpResponseBadRequest()
    

def projectInfo(request):

	if request.method == "POST":
		print 'POST-projectInfo'
		projectID=unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore');

		results ={}
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

	if request.method == "POST":
		print 'POST-project_users'
		projectID=unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore');

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

	if request.method == "POST":
		print 'POST-project_tasks'
		projectID=unicodedata.normalize('NFKD', request.POST['projectID']).encode('utf-8','ignore');

		results ={}
		results["successful"]="true"
		lst=[]
		for task in Task.objects.filter(projectID__iexact=projectID):
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
	if request.method == "POST":
		print 'POST-taskInfo'
		taskID=unicodedata.normalize('NFKD', request.POST['taskID']).encode('utf-8','ignore');

		results ={}
		results["successful"]="true"
		results["taskInfo"]=(Task.objects.get(taskID__iexact=taskID).as_json())
			
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
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
