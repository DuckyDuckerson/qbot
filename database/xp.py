import json

try:
    with open('user_xps.json', 'r') as file:
        user_xps = json.load(file)

except FileNotFoundError:
    user_xps = {
    }

level_check = {}


def xp_calculator(message, author_id):

    author_id_str = str(author_id)

    modifer = (len(message) * 0.5)

    xp = len(message) * modifer

    if author_id_str in user_xps:
        old_xp = user_xps[author_id_str]
        new_xp = old_xp + xp
        user_xps.update({author_id_str: new_xp})

    else:
        user_xps.update({author_id_str: xp})

    with open('user_xps.json', 'w') as file:
        json.dump(user_xps, file)


def level_calculator(author_id):

    author_id_str = str(author_id)

    if author_id_str in user_xps:
        xp = user_xps[author_id_str]
        level = (xp // 100000) + 1

    else:
        level = 1

    return level


def xp_check(author_id, author_name):
    author_id_str = str(author_id)

    if author_id_str in level_check:
        old_level = level_check[author_id_str]
        new_level = level_calculator(author_id)

        if new_level > old_level:
            level_check.update({author_id_str: new_level})
            return True

    else:
        level = level_calculator(author_id)
        level_check.update({author_id_str: level})
        return False
