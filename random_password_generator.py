"""
Different ways to use:-

python random_password_generator.py
python random_password_generator -s 
python random_password_generator -s -u
python random_password_generator --stats -u
python random_password_generator --stats --use_special
python random_password_generator --help
python random_password_generator --min_length=4 --max_length=8
"""

import random
import string
import argparse
import math


def random_uppercase():
    return random.choice(string.ascii_uppercase)


def random_lowercase():
    return random.choice(string.ascii_lowercase)


def random_punctuation():
    return random.choice(string.punctuation)


def random_digit():
    return random.choice(string.digits)


def generate_password(min_length, max_length, use_punctuation):
    length = random.randint(min_length, max_length)

    char_types = 3 if not use_punctuation else 4

    min_count = math.floor(length / char_types)
    char_counts = [min_count for _ in range(char_types)]

    overflow = length - sum(char_counts)

    x = random.sample(range(char_types), overflow)
    for v in x:
        char_counts[v] += 1

    password = [random_uppercase() for _ in range(char_counts[0])]
    password.extend([random_lowercase() for _ in range(char_counts[1])])
    password.extend([random_digit() for _ in range(char_counts[2])])

    if use_punctuation:
        password.extend([random_punctuation() for _ in range(char_counts[3])])

    random.shuffle(password)

    return ''.join(password)


def print_stats(password):
    counts = [
        sum([1 for x in password if x in string.ascii_uppercase]),
        sum([1 for x in password if x in string.ascii_lowercase]),
        sum([1 for x in password if x in string.digits]),
        sum([1 for x in password if x in string.punctuation])
    ]

    upper_count = counts[0]
    lower_count = counts[1]
    digit_count = counts[2]
    punctuation_count = counts[3]

    upper_template = string.Template('Uppercase Letters: $upper')
    lower_template = string.Template('Lowercase Letters: $lower')
    digit_template = string.Template('Digits: $digit')
    punctuation_template = string.Template('Punctuation: $punctuation')

    stats = ['Password has:',
             upper_template.substitute({'upper': upper_count}),
             lower_template.substitute({'lower': lower_count}),
             digit_template.substitute({'digit': digit_count})]

    if punctuation_count > 0:
        stats.append(punctuation_template.substitute({'punctuation': punctuation_count}))

    print('\n'.join(stats))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Generate a random password')
    argparser.add_argument('--min_length', '-n', type=int,
                           help='Minimum length of the password', default=8)
    argparser.add_argument('--max_length', '-x', type=int,
                           help='Maximum length of the password', default=16)
    argparser.add_argument('--stats', dest='stats', action='store_true',
                           help='Show password stats')
    argparser.add_argument('--use_punctuation', dest='punctuation',
                           action='store_true',
                           help='Include special characters in the password')
    args = argparser.parse_args()

    password = generate_password(args.min_length, args.max_length, args.punctuation)

    print(password)

    if args.stats:
        print_stats(password)


