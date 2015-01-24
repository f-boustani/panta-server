from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
data = {'the_message': message}
reg_id = "APA91bFgFwRa271nk1i9wcFFEcHj8QowcLA1KytPLTZFhBFyHRAnkGjl9DuuZagXj4ODPTsx22ZcbVWt_JaXJH20-MoH-Uk7Ud62Z6-LB69u_t4O_kJaD8bz6qFS7BpXkn4ykmtJoZCC9Wlj4uT-MVYQjPBu6m89mw"
gcm.plaintext_request(registration_id=reg_id, data=data)

a=gcm.plaintext_request(registration_id=reg_id, data=data)
print a


