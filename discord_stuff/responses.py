import random

triggers = ['quack', 'fuck', 'duck', 'cuck', 'quck']


def test_responses():

    responses = ['Test complete.', 'Fuck you.', 'Why do you have to \
bother me right now?', 'Test', 'Stop, please... \
I just want sleep', 'Test complete, can you fuck off now?', 'Dad?']

    return random.choice(responses)


def quack_responses():

    quack_sponses = ['Quack, quack', 'Quck you', 'quack quack, bitch',
                     'Quack', 'The fuck you want?',
                     'Do you even know what you said? \
No because you are not a fucking duck!',
                     'Watch your profanity', 'Just stop... you sound \
nothing like a duck',
                     'I am so tired of this...',
                     'How about we stop this for today?',
                     'I quit.', 'Shut the quck up',
                     'I am going to quack you up.']

    return random.choice(quack_sponses)
