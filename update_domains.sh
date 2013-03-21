#!/bin/bash
heroku run python manage.py /accounts/get_domains.py >> new_domains
for domain:new_domains:
    heroku domains:add domain
