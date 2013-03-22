#!/bin/bash
heroku run python manage.py get_new_domains | grep ^* | xargs heroku domains:add
