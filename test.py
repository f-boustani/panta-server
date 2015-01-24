from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
data = {'the_message': message}
reg_id = "APA91bHzei_ZWbffypm6Y24nY0b8xK_i9DUfXaBUZqTJ6ekVBiFw8KSONv-RUnvpBfGYIe0wh6rTHsxhEZpwKKRuaaAZyqOzIjco7Q90QGdLX3eQp4RoVX7tdXybOqTvwtb9H63ahmrjbFMooVf4MNPxuKcZqIkONA"
gcm.plaintext_request(registration_id=reg_id, data=data)

a=gcm.plaintext_request(registration_id=reg_id, data=data)
print a


