from gcm import *
message=' it works :D'
gcm = GCM("AIzaSyCWZBvIjLg0kmBELKsObqostZHx2AZWCvQ")
data = {'the_message': message}
reg_id = "APA91bFf5V6QVQN1vaKqheACAF33A3LMVuNxXX1X7Mn3VBr6FCJErxhD-1Hq2qnM3uHudZePy3xcvSgcdbazLdGftEg9ZZhZLazqO4mZxDfKQclpze8TGFs2B_j0SuQX1MjUEuZu1pzHJOJEcKEWDiFfPaX9C34UJA"
gcm.plaintext_request(registration_id=reg_id, data=data)

a=gcm.plaintext_request(registration_id=reg_id, data=data)
print a

#nasi: APA91bGvcB28g_CATZVAsgrSod52jQk4z5wz8c5EyiyrZZH6RrG21hXdXCWAH8q5140cYROPcjUUxEU6MXxhs9G511rHx6bCF0VMj66zy176Fb14Fwdu-ojkHIUmGifFKBoeakZ-jZxKdKB-Td5DZDjLqqtZUm3oQQ
