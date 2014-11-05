from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import Context
import datetime
import json
from MyApp.models import Login,Profile


def register(request):
	if request.method == "POST":
		print '#register- post mode'
		#username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		#password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		#name=unicodedata.normalize('NFKD', request.POST['name']).encode('utf-8','ignore');
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

		salt = bcrypt.gensalt()
		hash = bcrypt.hashpw(password, salt)
		newUser=Login(username=username,password=hash,name=name)
		newUser.save()
		results ={}
		results["successful"]="true"
		print username

		results["profile"]=[ob.as_json() for ob in Profile.objects.filter(username__iexact=username)]
		lst=[]
		for pro in Profile.objects.filter(username__iexact=username):
			lst.append(Projects.objects.get(projectID__iexact=pro.projectID).as_json())
		
		results["projects"]=lst	
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
	
		
	elif request.method == "OPTIONS":
		print '##############OPTIONS###########'
		results ={}
		results["mode"]="option mode"
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
		print '#########################'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
		salt = bcrypt.gensalt()
		hash = bcrypt.hashpw(password, salt)
		
		if(Login.objects.filter(username__iexact=username).exists()):
			passwd=Login.objects.get(username__iexact=username).password.encode('utf-8','ignore');
			if(passwd==bcrypt.hashpw(password,passwd)):
				results ={}
				results["successful"]="true"
				results["profile"]=[ob.as_json() for ob in Profile.objects.filter(username__iexact=username)]
				lst=[]
				for pro in Profile.objects.filter(username__iexact=username):
					lst.append(Projects.objects.get(projectID__iexact=pro.projectID).as_json())
		
				results["projects"]=lst	

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
		print '#############'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		print username
		results ={}
		results["profile"]=[ob.as_json() for ob in Profile.objects.filter(username__iexact=username)]
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
    
