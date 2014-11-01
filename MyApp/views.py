from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context
import datetime

from myapp.models import Login,Profile


def register(request):
    
    if request.method == "POST":
		print '#########################'
		username=unicodedata.normalize('NFKD', request.POST['username']).encode('utf-8','ignore');
		password=unicodedata.normalize('NFKD', request.POST['password']).encode('utf-8','ignore');
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
		newUser=UserPass(username=username,password=hash)
		newUser.save()
		results["successful"]="true"
		print json.dumps(results)
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
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
			
		response = HttpResponse(json.dumps(results), content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		response['Access-Control-Allow-Methods'] = "POST ,GET ,OPTIONS"
		response['Access-Control-Allow-Headers'] = "X-Requested-With,x-requested-with,content-type"
		return response
	
	else:
		return HttpResponseBadRequest()
    
