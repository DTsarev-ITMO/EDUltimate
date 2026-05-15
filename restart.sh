#!/bin/sh

sudo docker stop fastapi_db fastapi_app frontend_app
sudo docker system prune -a --volumes
/bin/sh /home/dvtsarev/PycharmProjects/EDUltimate/run.sh
sudo docker logs -f fastapi_app
