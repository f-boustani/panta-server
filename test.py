from gcm import *
class InvalidRegistration(Exception):
	pass

class MismatchSenderId(Exception):
	pass
	
class Unavailable(Exception):
	pass

class NotRegistered(Exception):
	pass
		


message=' it works :D'
gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
data = {'the_message': message}
reg_id = " APA91bFgFwRa271nk1i9wcFFEcHj8QowcLA1KytPLTZFhBFyHRAnkGjl9DuuZagXj4ODPTsx22ZcbVWt_JaXJH20-MoH-Uk7Ud62Z6-LB69u_t4O_kJaD8bz6qFS7BpXkn4ykmtJoZCC9Wlj4uT-MVYQjPBu6m89mw"

try:
    canonical_id = gcm.plaintext_request(registration_id=reg_id, data=data)
    print 'id:' ,canonical_id
    if canonical_id:
    	print 'reg_id change,must replace'
        
       
except InvalidRegistration:
    print 'Invalid Reg_id'
   
except NotRegistered:
    print not registered

except Unavailable :
    print 'Unavailable'

except MismatchSenderId :
    print 'Unavailable'



    
