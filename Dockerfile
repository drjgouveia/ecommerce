FROM python:3.6.0

COPY manage.py gunicorn-cfg.py requirements.txt sample.json ./
COPY prods prods
COPY sells sells
COPY api api
COPY users users
COPY ecommerce ecommerce

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

ARG loadsample=false
RUN /bin/bash -c "if [[ \"$loadsample\" = \"true\" ]] ; then python manage.py loaddata sample.json; fi"

ENV VIRTUAL_HOST="checkmein.drjgouveia.dev"
EXPOSE 8800
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "ecommerce.wsgi"]