if [ ! -f discord_stuff/.env ]; then
    echo "Creating .env file"
    touch discord_stuff/.env
    echo "Paste your Discord Bot token here: "
    read discord_token
    echo 'TOKEN="$token"' >> discord_stuff/.env
fi

if [ ! -f duckgpt/.env ]; then
    echo "Creating .env file"
    touch duckgpt/.env
    echo "Paste your Chatgpt token here: "
    read chatgpt_token
    echo 'api_key="$token"' >> duckgpt/.env
fi

docker ps -aq | xargs docker stop | xargs docker rm
docker build -t qbot .
#docker run --restart=always -v "$(pwd):/qbot" -i qbot
docker run --restart=always -v "$(pwd):/qbot" -d -p 80:80 -p 8080:8080 -p 443:443 qbot

