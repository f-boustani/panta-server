from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
data = {'the_message': message}
reg_id = "APA91bF6SCQRJ_d8g7-A6o5c9PZsBtOo0TYxPgejM_4P3ByZJyJd2KOEvZTYo0l7BWoO8BBp4lPR-1hNRo6SHZ_M4hAg5jaya3ja5IrU-01uIuslD40X_ZcWvUSLyXElXckCCT2mw-Zvrs-goH2273A6l4dQlLdOHQ"

try:
    canonical_id = gcm.plaintext_request(registration_id=reg_id, data=data)
    print 'id:' ,canonical_id
    if canonical_id:
    	print 'reg_id change,must replace'
        
       
except 'InvalidRegistration':
    print 'Invalid Reg_id'
   
except 'NotRegistered':
    print 'not registered'

except 'Unavailable' :
    print 'Unavailable'

except 'MismatchSenderId' :
    print 'Unavailable'


    
