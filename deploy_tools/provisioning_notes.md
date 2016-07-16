## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv
eg, on Ubuntu:

	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv


## nginx Virtual Host config

* see nginx.template.conf
* replace SITENAMR with, eg, www.pleatly.com

## Folder structure:
Assume we have an user account at /home/username

/home/username
|___sites
    |___SITENAME
         |___database
         |___ source
         |___ static
         |___ virtualenv


## Other important points

* Use PhantomJS for headless browser live functional tests
* Since we are using socket, also specify the IP for the SITENAME (which may be the public IP of aws)
* In production set DEBUG=FALSE, TEMPLATE_DEBUG=DEBUG, and ALLOWED_HOSTS=["*"]