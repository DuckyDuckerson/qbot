
# Variables ------------------------------------------------------
context = 5
messages = []
user_names = []
user_ids = []
time_stamps = []
# ---------------------------------------------------------------


def list_pop():
    messages.pop(0)
    user_names.pop(0)
    user_ids.pop(0)
    time_stamps.pop(0)


def add_message(message, user_name, user_id, time_stamp):
    # print('Messages: {messages}')
    # print(f'User names: {user_names}')
    # print(f'User ids: {user_ids}')
    # print(f'Time: {time_stamps}')

    messages.append(message)
    user_names.append(user_name)
    user_ids.append(user_id)
    time_stamps.append(time_stamp)


def remove_old_data():
    if len(messages) > context:
        list_pop()
