import argparse
import os
import sys
import base64
import requests


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Plain text to handwriting generator.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-f', '--file', help='text file to generate handwriting from')
    group.add_argument(
        '-s', '--string', help='string to generate handwriting from')
    parser.add_argument(
        '-b', '--bias', help='handwriting bias from 0.1 to 1',
        type=float, default=0.8)
    parser.add_argument(
        '-p', '--position', help='start at specific position',
        type=int, default=0)

    return parser.parse_args()


def get_handwriting(text, bias=0.8, samples=1):
    payload = {'text': text,
               'style': '../data/trainset_diff_no_start_all_labels.nc,1082+554',
               'bias': bias,
               'samples': samples}
    url = 'http://www.cs.toronto.edu/~graves/handwriting.cgi'
    page = requests.get(url, params=payload)
    text = page.text
    print('.', end='')
    # print('.', end='')
    search_string = '<img src="data:image/jpeg;base64,'
    start = text.find(search_string) + len(search_string)
    image_str = text[start:-5]
    return image_str


def command_line():
    args = get_arguments()

    if args.file:
        with open(args.file, 'r') as fl:
            text_in = [i.strip() for i in fl.readlines()]
    elif args.string:
        text_in = [args.string]

    start_at = args.position
    bias = args.bias

    if not os.path.exists('images'):
        print('Creating images folder')
        os.makedirs('images')

    print('Starting handwriting generation')
    for index, line in enumerate(text_in):
        if index < start_at:
            continue
        if not line.strip() == '':
            print(index, ' - ', line, end='')
            image_str = get_handwriting(line, bias)
            x = base64.b64decode(image_str)
            image_out = os.path.join('images', str(index) + '.png')
            with open(image_out, 'wb') as fl:
                fl.write(x)
            print('|')


if __name__ == '__main__':

    command_line()
