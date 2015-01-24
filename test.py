from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
data = {'the_message': message}
reg_id = "APA91bHIyefim8zLFBaWIR6T8QqwIGVLMyOCTonMtl7egKs3L8XXI9z4hsBoHDoyGQV-E2LFeAE2KFZBua3_6NgOfiTwgSFtVeNRpAhaolK4gjr3ZRdZuh2W3g4kk29PKXAPj_moHT6GJKbu5WBJHv2dM2wcJO45oA"
gcm.plaintext_request(registration_id=reg_id, data=data)

a=gcm.plaintext_request(registration_id=reg_id, data=data)
print a


