# Quackbot
====================

Quack is a simple bot that bullies users, creates voice chats and keeps track of xp.
**If you have other docker containers running on the same machine this script will stop them, and delete them. So be careful.**

To run the bot you need to 
- Make sure you have docker installed and running on your machine.
- Then just run the runme.sh script.
  - The first time you run the script it will ask you for your discord api key and chatgpt api key.

## Starting the bot 
====================

Just some things to note:
- The bot is still a work in progress.
- The bot is not very user friendly.
- There are hard coded values in the bot that you will need to change if you want to run it on your machine. (**This is in the discord_main.py file**)

## Apache 2.0
====================

The program also starts a web server that serves a simple html page for my website 
**itslit.bet**


## Qscanner
====================

Qscanner is a work in progress tool that records audio from an external source
then transcribes the audio to text, then sends a clipped version of the audio and the 
transcription to a discord channel.


## Platforms
====================

The bot is currently running on Arch linux, but it should work on any platform that supports docker.

The bot is still a mess, but I am working on it. Slowly improving it.


