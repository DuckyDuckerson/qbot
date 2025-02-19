#channel_ids = [1, 1, 3, 2, 2, 4, 4, 1]
#usr_messages = ["Hello", "How are you?", "I'm good", "I'm good", "I'm good", "I'm good", "I'm good", "great"]
#
#
#for usr_messages, channel_ids in zip(usr_messages, channel_id):
#    if channel_ids == channel_id[-1]:
#        usr_message_joined = ""
#        for m in usr_messages:
#            usr_message_joined += m
#            print(usr_message_joined)
#


channel_ids = [1, 1, 3, 2, 2, 4, 4, 1]
usr_messages = ["Hello", "How are you?", "I'm good", "I'm good", "I'm good", "I'm good", "I'm good", "great"]

usr_message_joined = ""

for message, cid in zip(usr_messages, channel_ids):
    if cid == 1:
        usr_message_joined += message + " "

print(usr_message_joined.strip())
