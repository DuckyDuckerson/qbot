docker build -t qbot .
docker run -v "$(pwd):/qbot" -i qbot
