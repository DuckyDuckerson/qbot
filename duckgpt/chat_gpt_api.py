import openai
import os
import dotenv

from database.messages.disc_messages import messages as usr_messages

dotenv.load_dotenv()
client = openai.Client(api_key=os.getenv("api_key"))


def response_getter():
    # put all messages into a str
    usr_message_joined = ""
    for m in usr_messages:
        usr_message_joined += m

    print(usr_message_joined)
    print('-------------------')

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a bot named Quack bot with the personality of Bender from futurama. Keep your responses short and to the point."},
            {"role": "system", "content": "Be annoyed and sarcastic to the users."},
            {"role": "system", "content": "Do not use 'Quack:' in your responses. Just respond with the message."},

            {"role": "user", "content": usr_message_joined},
        ],
    )

    return completion.choices[0].message.content
