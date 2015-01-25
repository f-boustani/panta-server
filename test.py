from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyBJ2eSyVNiT9Xfh-KsvmjjSvoY_rs7VvSA")
data = {'the_message': message}
reg_id = "APA91bHzei_ZWbffypm6Y24nY0b8xK_i9DUfXaBUZqTJ6ekVBiFw8KSONv-RUnvpBfGYIe0wh6rTHsxhEZpwKKRuaaAZyqOzIjco7Q90QGdLX3eQp4RoVX7tdXybOqTvwtb9H63ahmrjbFMooVf4MNPxuKcZqIkONA"

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
