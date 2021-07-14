[CHATBOT_myself.pdf](https://github.com/watcharap0n/m-business/files/6683094/CHATBOT_myself.pdf)
# M Business Fullstack FastAPI and Vue.js - MongoDB Deploy Heroku

****
URL : `http://m-bussiness-bot.herokuapp.com`

****

Generate a backend and frontend stack using Python, including interactive API documentation.

###### Interactive API documentation

**page 1**

![Alt text](https://github.com/watcharap0n/m-business/blob/main/static/github/1.png?raw=true "Title")

**page 2**

![Alt text](https://github.com/watcharap0n/m-business/blob/main/static/github/2.png?raw=true "Title")

**Page Sign In**

![Alt text](https://github.com/watcharap0n/m-business/blob/main/static/github/signin.png?raw=true "Title")

**Concept Design Patterns**
    
    (MVC) Model View Controller
    

**Feature**

    - Python FastAPI backend:
        - Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
        - Intuitive: Great editor support. Completion everywhere. Less time debugging.
        - Easy: Designed to be easy to use and learn. Less time reading docs.
        - Short: Minimize code duplication. Multiple features from each parameter declaration.
        - Robust: Get production-ready code. With automatic interactive documentation.
        - Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.
        - Many other features including automatic validation, serialization, interactive documentation, authentication with OAuth2 JWT tokens, etc.
    - Firebase Authentication
    - WebSocket Pusher
    - Vue frontend Generated with Vue CDN and Vuetify
    - Database MongoDB
    - Docker Compose Local

**Testing APP**

    Testing FastAPI (API)
    Testing Database
    Using by Testing Client > test_app.py (test_modules) run script
    
    

**Firebase service authentication**

![Alt text](https://github.com/watcharap0n/m-business/blob/main/static/github/authentication.png?raw=true "Title")

**Config Variable In Heroku**

    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "projectId": os.environ['projectId'],
    "databaseURL": os.environ['databaseURL'],
    "storageBucket": os.environ['storageBucket'],
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId'],
    "measurementId": os.environ['measurementId']

    "type": os.environ['type'],
    "project_id": os.environ['project_id'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'].replace("\\n", "\n"),
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    "auth_uri": os.environ['auth_uri'],
    "token_uri": os.environ['token_uri'],
    "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url": os.environ['client_x509_cert_url']

**Build && Setup Python**

~~~~
$ pip install virtualenv
~~~~

~~~~
$ virtualenv venv
~~~~

~~~~
$ source venv/bin/activate
~~~~

~~~~
$ (venv) pip install -r requirements.txt
~~~~

~~~~
$ brew tap mongodb/brew
$ brew install mongodb-community@4.4
$ brew install --cask robo-3t
 ~~~~

~~~~
$ sudo mongod --dbpath /usr/local/var/mongodb
~~~~

**Deploy On Heroku**

~~~~
$ heroku login
$ heroku git:clone -a (repo-name)
$ cd game-card-watcharapono
$ git add .
$ git commit -am "make it better"
$ git push heroku master
 ~~~~
