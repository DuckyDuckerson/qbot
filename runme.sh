if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi


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

echo "Do you want to start the bot or kill all running containers? (1. Start, 2. Kill, 3. Prune system)"
read -r choice

case "${choice}" in
    1)
        echo "You chose to start the bot."
        
        echo "Starting bot..."
        docker ps -aq | xargs docker stop | xargs docker rm
        docker build -t qbot .
        #docker run --restart=always -v "$(pwd):/qbot" -i qbot
        echo "Starting qbot..."
        docker run --restart=always -v "$(pwd):/qbot" -d -p 80:80 -p 8080:8080 -p 443:443 qbot
        ;;
    2)
        echo "You chose to kill all running containers."
        
        echo "Killing all running containers..."
        docker ps -aq | xargs docker stop | xargs docker rm
        ;;

    3)
        echo "You chose to prune the system."
        echo "Pruning system..."
        docker system prune -a
        ;;
    *)
        echo "Invalid choice. Please run the script again and select a valid option."
        exit 1
        ;;
esac
echo "Done."
