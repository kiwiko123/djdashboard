#!/bin/bash

cd ../../;python3 manage.py runserver &
cd ./pazaak/react;npm start
