import httplib
#import http.client
import base64
import ssl
import sys

#parameters

name = sys.argv[1]
first = sys.argv[2]
last = sys.argv[3]
passwd = sys.argv[4]
email = sys.argv[5]
uid_group = sys.argv[6]
expiry_date = "2018-05-29"

# host and authentication credentials
host = "172.17.12.253"
user = "admin"
password = "Wipro@123"

if (uid_group == 'Employee'):
 uid = 'a1740510-8c01-11e6-996c-525400b48521'
elif ( uid_group == 'Faculty'):
 uid = '91635590-f1f4-11e7-a7fc-005056bb38f0'
elif ( uid_group == 'Student'):
 uid = '5dab68e0-0d66-11e8-a1e8-005056bb38f0'

conn = httplib.HTTPSConnection("{}:9060".format(host))
creds = str.encode(':'.join((user, password)))
encodedAuth = bytes.decode(base64.b64encode(creds))

req_body_json = """  {{
    "InternalUser" : {{
        "name" : "{}",
        "enabled" : true,
        "email" : "{}",
        "password" : "{}",
        "firstName" : "{}",
        "lastName" : "{}",
        "changePassword" : true,
        "expiryDateEnabled" : true,
        "expiryDate" : "{}",
        "enablePassword" : "{}",
        "identityGroups" : "{}",
        "customAttributes" : {{
        }},
        "passwordIDStore" : "Internal Users"
    }}
}}
""".format(name,email,passwd,first,last,expiry_date,passwd,uid)

headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'authorization': " ".join(("Basic",encodedAuth)),
    'cache-control': "no-cache",
    }

conn.request("POST", "/ers/config/internaluser/", headers=headers, body=req_body_json)

res = conn.getresponse()
data = res.read()

print("Status: {}".format(res.status))
#print("Header:\n{}".format(res.headers))
print("Body:\n{}".format(data.decode("utf-8")))
