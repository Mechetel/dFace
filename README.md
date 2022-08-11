ML project to recognise people on cameras
Using docker, django, postgres

To run on localhost:
docker-compose -f docker/dev.yml up --build

To createsuperuser:
docker-compose \
  -f docker/dev.yml \
  run --rm be python manage.py createsuperuser

To stop all containers:
docker stop $(docker ps -a -q)

To delete all containers:
docker rm $(docker ps -a -q)

To delete all images:
docker rmi -f $(docker images -q)

By Dmitry and Pavel
