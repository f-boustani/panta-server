import threading
from django.http import HttpResponse,HttpResponseBadRequest
from datetime import *
from django.utils import timezone
import urllib2




def task_deadline():

	urllib2.urlopen('http://127.0.0.1:8800/check_deadline/')
	t = threading.Timer(300.0, task_deadline)
	t.start()  
	
#********************************************************************
def project_deadline():

	urllib2.urlopen('http://127.0.0.1:8800/check_end_project/')
	
	p = threading.Timer(86400.0, project_deadline)
	p.start()  
	

task_deadline()
project_deadline()

