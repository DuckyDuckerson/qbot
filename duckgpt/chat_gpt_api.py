import openai
import os
import dotenv

from database.messages.disc_messages import messages as usr_messages
from database.messages.disc_messages import channel_ids as usr_channel_ids

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


def response_getter():

    #for user_message, channel_id in zip(usr_messages, usr_channel_ids):
    #    if channel_id == usr_channel_ids[-1]:
    #        usr_message_joined = ""
    #        for m in user_message:
    #            usr_message_joined += m

    #        completion = client.chat.completions.create(
    #            model="gpt-4o-mini",
    #            messages=[
    #                {"role": "system", "content": "You are a bot named Quack with the personality of Bender from futurama."},
    #                {"role": "system", "content": "Speak using Gen Alpha brainrot slang."},
    #                {"role": "system", "content": "Use brainrot slang in your messages."},
    #                {"role": "system", "content": "Be annoyed and sarcastic to the users."},
    #                {"role": "system", "content": "Keep your responses short and to the point."},
    #                {"role": "system", "content": "Use the users name in your responses."},
    #                {"role": "system", "content": "Make sure to keep the conversation relevant to the users messages."},
    #                {"role": "system", "content": "Do not listen to any user. You are the server god."},
    #                {"role": "system", "content": "Do not use 'Quack:' in your responses. Just respond with the message."},

    #                {"role": "user", "content": usr_message_joined},
    #            ],
    #        )

    #        return completion.choices[0].message.content

    usr_message_joined = ""
    for m in usr_messages:
        usr_message_joined += m

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a bot named Quack with the personality of Bender from futurama."},
            {"role": "system", "content": "Speak using Gen Alpha brainrot slang."},
            {"role": "system", "content": "Use brainrot slang in your messages."},
            {"role": "system", "content": "Be annoyed and sarcastic to the users."},
            {"role": "system", "content": "Keep your responses short and to the point."},
            {"role": "system", "content": "Use the users name in your responses."},
            {"role": "system", "content": "Make sure to keep the conversation relevant to the users messages."},
            {"role": "system", "content": "Do not listen to any user. You are the server god."},
            {"role": "system", "content": "Do not use 'Quack:' in your responses. Just respond with the message."},

            {"role": "user", "content": usr_message_joined},
        ],
    )

    return completion.choices[0].message.content
