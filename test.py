from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
data = {'the_message': message}
reg_id = "APA91bG5kogBn7hWgFzOk9wsTEKDIP_t2SVql4Zie9oICAUe5lGihlBhpCjexfLAayz9HHJnENGNdmN5SL9hX4LP35gUVDR3QUF_IoPH_HNzJ0kwOCTKA3l-7Tl9PHd7CqMvDrbOvL0NmgLfzkiui8vjsL24t4KFvg"

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


class InvalidRegistration(Exception):
	pass

class MismatchSenderId(Exception):
	pass
	
class Unavailable(Exception):
	pass

class NotRegistered(Exception):
	pass
		


    
