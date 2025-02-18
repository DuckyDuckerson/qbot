from duck_log.logger import logger


# Variables ------------------------------------------------------
messages = []
user_names = []
user_ids = []
time_stamps = []
msg_count = []
channel_ids = []
context = 100
# ---------------------------------------------------------------


def list_pop():
    messages.pop(0)
    user_names.pop(0)
    user_ids.pop(0)
    time_stamps.pop(0)


def context_messages(time):
    context = 100
    return context
#    total = 0
#
#    msg_count.append(int(len(messages)))
#
#    for idx, i in enumerate(msg_count):
#        total += i
#    msg_avg = total / len(msg_count)
#
#    if msg_avg < context:
#
#        if len(messages) > context:
#            list_pop()
#
#        logger(f"Average messages per hour: context:{context}")
#        return context
#
#    elif msg_avg > context:
#
#        if len(messages) > context:
#            list_pop()
#        msg_count.clear()
#
#        if msg_avg > (2 * context):
#
#            msv_timeavg = (msg_avg / time)
#            if msv_timeavg < context:
#                logger(f"Average messages per hour: {context}")
#                return context
#
#            logger(f"Average messages per hour: {int(msv_timeavg)}")
#            return int(msv_timeavg)
#
#        logger(f"Average messages per hour: {int(msg_avg)}")
#        return int(msg_avg)


def add_message(message, user_name, user_id, time_stamp, channel_id):
    messages.append(f'{user_name}: {message}\n')
    user_names.append(user_name)
    user_ids.append(user_id)
    time_stamps.append(time_stamp)
    channel_ids.append(channel_id)
