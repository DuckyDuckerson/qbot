import os


def logger(line):

    print(line)

    if not os.path.exists('log.txt'):
        with open('log.txt', 'w') as f:
            f.write(line + '\n')

    else:
        with open('log.txt', 'a') as f:
            f.write(line + '\n')


def random_string(length):
    import random
    import string

    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def report_log(report):

    if not os.path.exists('logs/report.txt'):
        with open('logs/report.txt', 'w') as f:
            f.write(report + '\n')

    else:
        with open('logs/report.txt', 'a') as f:
            f.write(report + '\n')


def error_log(line):
    print(line)

    if not os.path.exists('error.txt'):
        with open('error.txt', 'w') as f:
            f.write(line + '\n')

    else:
        with open('error.txt', 'a') as f:
            f.write(line + '\n')
