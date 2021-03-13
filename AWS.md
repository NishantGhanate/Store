## Part 1 - Local setup 
```sh
> source scripts/Scripts/activate

> pip install awscli

> eb --version 

> mkdir .ebextensions

> ls --all

> touch .ebextensions

> touch .ebextensions/django.config

> nano .ebextensions/django.config

    option_settings:
	aws:elasticbeanstalk:container:python:
		WSGI: store/wsgi.py


> decative 
```
## Part 2 - Global setup 

```sh
> pip install awscli

> eb init -p python=3.6 aws env

aws credtions from account > my security cred > Access keys (access key ID and secret access key)

> some error 

> eb init 

> selection :  location 

> selection:  appname

> selection: python version 

> code commit - no 

> ssh - yes

> default awseb 

> emty for no passphrase

> visit eslatic beans talk > applications 

> eb create store

To handle wsgi error 
>  push code to git repo / eb deploy --staged
```
