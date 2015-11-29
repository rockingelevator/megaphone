# megaphone
Simple demo web app based on [aiohttp.web](http://aiohttp.readthedocs.org/en/stable/web.html), websockets and React components

![Preview](http://s23.postimg.org/w2hu3mhvv/preview.jpg)

## Run

#####Make virtual env:

_Python 3.5 is required._

`$ mkvirtualenv --python=/path/to/python3 megaphone`

  
Check python version:

`$ python -V`

_More about [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest)_

   
#####Install dependecies:

`$ pip install -r requirements.txt`

   
#####Cryptography package:
Cryptography package is used to work with passwords. 

Try: 

`$ pip install cryptography`

For information about installation take a look at [cryptography docs](http://cryptography.readthedocs.org/en/latest/installation/)

For example, installation on OS X may look like this:

```
$ brew install openssl
$ env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography
```
  
#####Install Node modules  

`$ npm install`

#####Run server

`$ python manage.py`

Visit [http://127.0.0.1:8080](http://127.0.0.1:8080)

App using Heroku postgres database so you dont have to install and configure your own database for demo purposies.
