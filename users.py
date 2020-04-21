users = [
	{"name": "notexist_user", "email": "nouser@nouser.com", "password": "1q2w3e"},
	{"name": "yourvalid_user", "email": "valid@mail.com", "password": "123123"},

]

def get_user(name):
    try:
        for i in users:
            if i["name"] == name:
                return i
            else:
                next(iter(users))
    except:
        print("User Not Found!")
