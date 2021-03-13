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
        WSGI: store.wsgi:application

  or 

  option_settings:
    aws:elasticbeanstalk:container:python:
      WSGIPath: store.wsgi

> decative 
```
## Part 2 - Global setup 

```sh
> pip install awscli

> eb init -p python-3.6 store ( creates application on aws)

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

> eb create store-env

To handle wsgi error 
>  push code to git repo / eb deploy --staged
```

## DEBUG :
```sh
> https://stackoverflow.com/questions/31169260/your-wsgipath-refers-to-a-file-that-does-not-exist

> https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

```