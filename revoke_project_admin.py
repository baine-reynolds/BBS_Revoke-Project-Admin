import requests
import getpass
import json

url = input("Please enter the Source instance's Base URL (i.e. https://bitbucket.mycompany.com (Server)):\n")
admin_user = input("Please enter the Admin username for your source environment:\n")
admin_password = getpass.getpass("Please enter the Admin password for your source environment:\n")

session = requests.Session()
session.auth = (admin_user, admin_password)

def get_projects(start=None, limit=None):
	while True:
		params = {'start': start, 'limit': limit}
		try:
			r = session.get(url + '/rest/api/1.0/projects', params=params)
		except requests.exceptions.SSLError:
			r = session.get(url + '/rest/api/1.0/projects', params=params, verify=False)
		r_data = r.json()
		for project_json in r_data['values']:
			yield project_json
		if r_data['isLastPage'] == True:
			return
		start = r_data['nextPageStart']

def get_project_user_perms(project, start=None, limit=None):
    while True:
        params = {'start': start, 'limit': limit}
        endpoint = url + "/rest/api/1.0/projects/" + project['key'] + "/permissions/users"
        try:
            r = session.get(endpoint, params=params)
        except requests.exceptions.SSLError:
            r = session.get(endpoint, params=params, verify=False)
        r_data = r.json()
        for user_json in r_data['values']:
            yield user_json
        if r_data['isLastPage'] == True:
            return
        start = r_data['nextPageStart']

def get_project_group_perms(project, start=None, limit=None):
    while True:
        params = {'start': start, 'limit': limit}
        endpoint = url + "/rest/api/1.0/projects/" + project['key'] + "/permissions/groups"
        try:
            r = session.get(endpoint, params=params)
        except requests.exceptions.SSLError:
            r = session.get(endpoint, params=params, verify=False)
        r_data = r.json()
        for group_json in r_data['values']:
            yield group_json
        if r_data['isLastPage'] == True:
            return
        start = r_data['nextPageStart']

def reduce_user_permission(project, user):
    # "PROJECT_WRITE" is one step down from "PROJECT_ADMIN"
    params = {'name': user['user']['name'], 'permission': 'PROJECT_WRITE'}
    endpoint = url + "/rest/api/1.0/projects/" + project['key'] + "/permissions/users"
    try:
        r = session.put(endpoint, params=params)
    except requests.exceptions.SSLError:
        r = session.put(endpoint, params=params, verify=False)
    r = session.put(endpoint, params=params)
    if r.status_code in range(200,299):
        print(f"Successfully reduced the user \"{user['user']['name']}\" from ADMIN to WRITE for project \"{project['name']}\"")

def reduce_group_permission(project, group):
    # "PROJECT_WRITE" is one step down from "PROJECT_ADMIN"
    params = {'name': group['group']['name'], 'permission': 'PROJECT_WRITE'}
    endpoint = url + "/rest/api/1.0/projects/" + project['key'] + "/permissions/groups"
    try:
        r = session.put(endpoint, params=params)
    except requests.exceptions.SSLError:
        r = session.put(endpoint, params=params, verify=False)
    if r.status_code in range(200,299):
        print(f"Successfully reduced the group \"{group['group']['name']}\" from ADMIN to WRITE for project \"{project['name']}\"")

def start():
    for project in get_projects():
        for user in get_project_user_perms(project):
            if user['permission'] == "PROJECT_ADMIN":
                reduce_user_permission(project, user)
        for group in get_project_group_perms(project):
            if group['permission'] == "PROJECT_ADMIN":
                reduce_group_permission(project, group)

if __name__ == '__main__':
    start()