#!/bin/bash
# This file will run when the web service starts
cd vsf_crawler
# nohup bash -c "scrapyd >& /dev/null &" && sleep 6
cd ..
gunicorn noticias_sin_filtro_server.wsgi:application --bind 0.0.0.0:8000 && run_scrapyd_server.sh