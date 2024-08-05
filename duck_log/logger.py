import os


def logger(line):

    print(line)

    if not os.path.exists('log.txt'):
        with open('log.txt', 'w') as f:
            f.write(line + '\n')

    else:
        with open('log.txt', 'a') as f:
            f.write(line + '\n')


def report_log(line):
    print(line)

    if not os.path.exists('report.txt'):
        with open('report.txt', 'w') as f:
            f.write(line + '\n')

    else:
        with open('report.txt', 'a') as f:
            f.write(line + '\n')


def error_log(line):
    print(line)

    if not os.path.exists('error.txt'):
        with open('error.txt', 'w') as f:
            f.write(line + '\n')

    else:
        with open('error.txt', 'a') as f:
            f.write(line + '\n')
