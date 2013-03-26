#!/bin/bash
heroku run python manage.py get_new_domains --app shrouded-mountain-1305 | grep ^* | xargs heroku domains:add --app shrouded-mountain-1305
