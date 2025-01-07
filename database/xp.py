import json
import ctypes

lib = ctypes.CDLL('./functions/cfuncs.so')
lib.xp_alg.argtypes = [ctypes.c_char_p]

try:
    with open('user_xps.json', 'r') as file:
        user_xps = json.load(file)

except FileNotFoundError:
    user_xps = {
    }

level_check = {}


def xp_calculator(message, author_id):
    author_id_str = str(author_id)

    xp = lib.xp_alg(message.encode('utf-8'))

    if author_id_str in user_xps:
        old_xp = user_xps[author_id_str]
        new_xp = old_xp + xp
        user_xps.update({author_id_str: new_xp})

    else:
        user_xps.update({author_id_str: xp})

    with open('user_xps.json', 'w') as file:
        json.dump(user_xps, file)


def xp_to_file(author_id):
    author_id_str = str(author_id)

    if author_id_str in user_xps:
        xp = user_xps[author_id_str]

    else:
        xp = 0

    return xp


def xp_check(author_id, author_name):
    author_id_str = str(author_id)

    if author_id_str in level_check:
        old_level = level_check[author_id_str] + 1000
        new_level = xp_to_file(author_id)

        if new_level > old_level:
            level_check.update({author_id_str: new_level})
            return True

    else:
        level = xp_to_file(author_id)
        level_check.update({author_id_str: level})
        return False


def rank_check(author_id):
    sorted_users = sorted(user_xps.items(), key=lambda x: x[1], reverse=True)

    return sorted_users.index((str(author_id), user_xps[str(author_id)])) + 1
