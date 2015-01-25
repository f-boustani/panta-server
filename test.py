from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
data = {'the_message': message}
reg_id = "APA91bG5kogBn7hWgFzOk9wsTEKDIP_t2SVql4Zie9oICAUe5lGihlBhpCjexfLAayz9HHJnENGNdmN5SL9hX4LP35gUVDR3QUF_IoPH_HNzJ0kwOCTKA3l-7Tl9PHd7CqMvDrbOvL0NmgLfzkiui8vjsL24t4KFvg"

#response=gcm.plaintext_request(registration_id=reg_id, data=data)
#print response
try:
    canonical_id = gcm.plaintext_request(registration_id=reg_id, data=data)
    print canonical_id
    if canonical_id:
    	print 'reg_id change,must replace'
        
       # entry = entity.filter(registration_id=reg_id)
        #entry.registration_id = canonical_id
        #entry.save()
except GCMNotRegisteredException:
    print 'notregistered,Remove from db'
   # entity.filter(registration_id=reg_id).delete()
except GCMUnavailableException:
    print 'gcm unavailable,resend'

#nasi: APA91bGvcB28g_CATZVAsgrSod52jQk4z5wz8c5EyiyrZZH6RrG21hXdXCWAH8q5140cYROPcjUUxEU6MXxhs9G511rHx6bCF0VMj66zy176Fb14Fwdu-ojkHIUmGifFKBoeakZ-jZxKdKB-Td5DZDjLqqtZUm3oQQ
