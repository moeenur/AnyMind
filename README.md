# AnyMind
This assignment has been completed using Python 3.7

To run the app please go to the project root directory and execute the below commands in the terminal.

### Development environment preparation

Create a Python Virtual Environment using the venv module
```bash
python3 -m venv venv
```

Activate the Python Virtual Environment in terminal
```bash
source venv/bin/activate
```

Install the necessary libraries for the app
```bash
pip install -U pip
pip install wheel
pip install -r requirements.txt
```

### Development server
Start server to run the application
```bash
python manage.py runserver
```

### Requests
- Get the list of tweets with the given hashtag
```bash
$ curl -H "Accept: application/json" -X GET http://localhost:xxxx/hashtags/Python?limit=40
```

- Get the list of tweets that the user has on his feed
```bash
$ curl -H "Accept: application/json" -X GET http://localhost:xxxx/users/twitter?limit=20
```

### Unit Tests
Verify functional behavior of the application
```bash
python manage.py test
```