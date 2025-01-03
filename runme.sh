docker ps -aq | xargs docker stop | xargs docker rm
# docker system prune -a

docker build -t qbot .
docker run --restart=always -v "$(pwd):/qbot" -i qbot
reboot
