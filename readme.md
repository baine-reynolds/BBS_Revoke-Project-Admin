## Dependency
* Python 3
* [Requests Package](http://docs.python-requests.org/en/master/)

`
pip3 install requests --user
`

## Usage
Option 1.
Run the script. This will prompt you for your environment url (i.e. https://bitbucket.example.com) and an admin username/password.

Option 2.
Update lines 5-7 with the string values of your URL, username, and password so that the script does not need to prompt for these values.

## Running the Script
```python
python3 /path/to/revoke_project_admin.py
```

## Examples
For lines 5-7: (optional)
```python
url = "https://bitbucket.example.com"
admin_user = "admin"
admin_password = "password"
```