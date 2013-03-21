#!/bin/bash
python manage.py get_new_domains | xargs heroku domains:add
