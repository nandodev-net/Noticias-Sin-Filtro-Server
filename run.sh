#!/bin/bash
# Use this file to launch a development server
docker-compose down -v
docker-compose -f docker-compose.yml up -d --build