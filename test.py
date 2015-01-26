from gcm import *

message=' it works :D'
gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
data = {'the_message': message}
reg_id = "APA91bFIhg5dDv9vnJUgslIW3GUky0Sx4SNQI0_qIzn7ZKu9DAN11m73aKC-qJ72ju54FyDAt7OMcrafsxXIs-ADP6KjEj2BCVL_A7s9bo222Cwehmm_ViSii9HPuDzzAtjrNLp63wbqxq4VL8OdbocKD6mQ75bVQg"

try:
    canonical_id = gcm.plaintext_request(registration_id=reg_id, data=data)
    print 'id:' ,canonical_id
    if canonical_id:
    	print 'reg_id change,must replace'
        
       
except:
    print 'except'
   



    
