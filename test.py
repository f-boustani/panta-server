from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
data = {'the_message': message}
reg_id = "APA91bGdwPMNU0rh5ccVuTtfipz_Z7yHhEdSkoA91v6WOzWpbdxLcS7Gkc3IF7qN4jf3rdLh-p3Vm5Ntx1aEJpTQxzyPMMouRSuylpjNBP-iXzkbmP2aj9AMEfMaLHCCEvBa5kEp0EOZRYqSnx-9mkoBj5T3gv2CQQ"

#response=gcm.plaintext_request(registration_id=reg_id, data=data)
#print response
try:
    canonical_id = gcm.plaintext_request(registration_id=reg_id, data=data)
    print 'canonical_id'
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
