from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
data = {'the_message': message}
reg_id = "APA91bEdCf95WLdavLh_Pv4GPemoJZkra9hFVI-RK5XRVHxb5n4S580THd1m5f-8BDYU1x6I74JAyvDoT9Zh4uWm9PGwNE72YCFee3NbREkcZpnEyZAi5xF2WaEgMxh7GcB2v0Wia2J-vK_dPI44RI3pYbYl7I_o6g"
gcm.plaintext_request(registration_id=reg_id, data=data)

a=gcm.plaintext_request(registration_id=reg_id, data=data)
print a


