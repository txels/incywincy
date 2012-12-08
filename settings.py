from requests.auth import HTTPBasicAuth

# root = 'http://uktv.co.uk/'
# start = 'http://uktv.co.uk/eden/'
user, password = 'uktv', 'digitalrefresh'
user, password = 'uktvdev', 'analogrefresh'
auth = HTTPBasicAuth(user, password)
