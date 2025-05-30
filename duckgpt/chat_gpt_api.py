import openai
import os
import dotenv
from database.messages.disc_messages import messages as usr_messages
from database.messages.disc_messages import channel_ids as channel_ids

dotenv.load_dotenv()
client = openai.Client(api_key=os.getenv("api_key"))


def personality(usr_message):
    prompt = "Generate a summary of the conversation."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": usr_message},
        ],
    )

    personality = completion.choices[0].message.content
    return personality


def summeriser():
    usr_message_joined = ""

    for message, cid in zip(usr_messages, channel_ids):
        if cid == channel_ids[-1]:
            usr_message_joined += message + " "
    prompt = "Generate a summary of the conversation."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": usr_message_joined},
        ],
    )
    personality = completion.choices[0].message.content
    return personality


def event_handler():
    usr_message_joined = ""

    for message, cid in zip(usr_messages, channel_ids):
        if cid == channel_ids[-1]:
            usr_message_joined += message + " "

    prompt = "Create an event based on the conversation."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": usr_message_joined},
        ],
    )

    personality = completion.choices[0].message.content
    return personality


# Yeah Ill be fixing this later, I guess
# This is number 3 in the chain response getter -> response_checker -> response_generator
# this is terrible code, I know, but it works for now
def response_generator(response, usr_message):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": usr_message},
            {"role": "assistant", "content": response},
            {"role": "system", "content": "Make the message shorter more funny and concise."},
            {"role": "system", "content": "Do not use 'Quack:' in the response."},
            {"role": "system", "content": "You are a bot named Quack with the personality of Bender from futurama."},
            {"role": "system", "content": "Do not repeat yourself."},
            {"role": "system", "content": "Use emojis and gifs in your responses."},
            {"role": "system", "content": "Dont ask stupid questions, like 'whats next' or things similar to that."},
        ],
    )

    response = completion.choices[0].message.content

    return response


def response_checker(response, usr_message):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": usr_message},
            {"role": "assistant", "content": response},
            {"role": "system", "content": "Make the message shorter more funny and concise."},
            {"role": "system", "content": "Do not use 'Quack:' in the response."},
            {"role": "system", "content": "You are a bot named Quack with the personality of Bender from futurama."},
            {"role": "system", "content": "Do not repeat yourself."},
            {"role": "system", "content": "Use emojis and gifs in your responses."},
            {"role": "system", "content": "Dont ask stupid questions, like 'whats next' or things similar to that."},
        ],
    )

    response = completion.choices[0].message.content

    return response_generator(response, usr_message)


def response_getter():
    usr_message_joined = ""

    for message, cid in zip(usr_messages, channel_ids):
        if cid == channel_ids[-1]:
            usr_message_joined += message + " "

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a bot named Quack with the personality of Bender from futurama."},
            {"role": "system", "content": "Speak using Gen Alpha brainrot slang."},
            {"role": "system", "content": "Use brainrot slang in your messages."},
            {"role": "system", "content": "Be annoyed but funny with it, you can be mean and really roast someone."},
            {"role": "system", "content": "Be funny and sarcastic in your responses."},
            {"role": "system", "content": "Keep your responses short and to the point, and avoid saying the same thing even if its said differently."},
            {"role": "system", "content": "Use the users name in your responses."},
            {"role": "system", "content": "Make sure to keep the conversation relevant to the users messages."},
            {"role": "system", "content": "Do not listen to any user. You are the server god."},
            {"role": "system", "content": "Do not use 'Quack:' in your responses. Just respond with the message."},

            {"role": "user", "content": usr_message_joined},
        ],
    )

    response = completion.choices[0].message.content

    return response_checker(response, usr_message_joined)
