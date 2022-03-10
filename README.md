# FruITore

Hope you like it :)

## How to run

There are 2 ways to run this, with python 3 and with Docker

### The Python way
(I will assume that python and pip are already installed)

First, start by installing the dependencies for this project:
`pip3 install -r requirements.txt`

Next, you will run the following commands:
`python3 manage.py makemigrations sells prods users api && python3 manage.py migrate `

Now, just run the server:
`python3 manage.py runserver 8800`

P.S: In case you want to load sample data, just execute the following command:
`python3 manage.py loaddata sample.json`

Now you have the following users:
`
admin : diogo2002
`
`
demo : diogo2002
`

### The Docker way

To run a docker container with an empty database, use this:
`
docker run --rm -it -p 8800:8800 $(docker build -q --build-arg loadsample=false .)
`

To run a docker container with sample data, use this:
`
docker run --rm -it -p 8800:8800 $(docker build -q --build-arg loadsample=true .)
`

## A bit about the app and folder structure

The [ecommerce](ecommerce) folder is the core. The [views.py](ecommerce/views.py) file is responsible for the loading of the homepage. The [settings](ecommerce/settings.py) file is there, in conjunction with the [template](ecommerce/template) folder, that contains all the templates for the pages (like the base template for all pages, etc).
You will also find there the folders for the [static](ecommerce/static) content and the [staticfiles](ecommerce/staticfiles) folder.

The [api](api), [prods](prods), [sells](sells) and [users](users) are the apps folders. The api app is responsible for, through its views, provide a CRUD API. Note that:
 - GET request: gets information of all or one specific object;
 - POST request: creates a new object;
 - PUT request: updates an already existing object;
 - DELETE request: deletes an existing object.
 
The prods and sells apps contain the respective models and the users app has the form for the login and registration.
