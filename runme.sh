git pull

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

echo "Do you want to start the bot or kill all running containers? (1. Start, 2. Kill)"
read choice
if [ $choice -eq 1 ]; then
    echo "Starting bot..."
    docker ps -aq | xargs docker stop | xargs docker rm
    docker build -t qbot .
    #docker run --restart=always -v "$(pwd):/qbot" -i qbot
    docker run --restart=always -v "$(pwd):/qbot" -d -p 80:80 -p 8080:8080 -p 443:443 qbot
else
    echo "Killing all running containers..."
    docker ps -aq | xargs docker stop | xargs docker rm
fi
