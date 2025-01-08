# Quackbot
====================

Quack is a simple bot that bullies users, creates voice chats and keeps track of xp.

To run the bot you need to 
- Make sure you have docker installed and running on your machine.
**If you have other docker containers running on the same machine this script will stop them, and delete them. So be careful.**
- Then just run the runme.sh script.
  - The first time you run the script it will ask you for your discord api key and chatgpt api key.

## Starting the bot 
====================

Just some things to note:
- The bot is still a work in progress.
- The bot is not very user friendly.
- There are hard coded values in the bot that you will need to change if you want to run it on your machine. (**This is in the discord_main.py file**)

## Qscanner
====================

Qscanner is a work in progress tool that records audio from an external source
then transcribes the audio to text, then sends a clipped version of the audio and the 
transcription to a discord channel.


## Platforms
====================

I have the bot running on a raspberry pi 4 with 4gb of ram and it works fine. I have also tested it on a macOS machine and it works fine there too. **Not sure about windows.**

The bot is still a mess, but I am working on it. Slowly improving it.


