import argparse
import os
import sys
import base64
import requests
from PIL import Image


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Plain text to handwriting generator.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-f', '--file', help='text file to generate handwriting from')
    group.add_argument(
        '-t', '--text', help='text to generate handwriting from')
    parser.add_argument(
        '-s', '--style', help='handwriting style from 0 to 5, where 5 is random style',
        type=int, default=5)
    parser.add_argument(
        '-b', '--bias', help='handwriting bias from 0.1 to 1',
        type=float, default=0.8)
    parser.add_argument(
        '-p', '--position', help='start at specific position',
        type=int, default=0)
    parser.add_argument(
        '-c', '--color', help='add custom RGB color values to generated text',
        type=str, default='0,0,0')

    return parser.parse_args()


def get_handwriting(text, style, bias, samples=1):
    style_models = (
            '../data/trainset_diff_no_start_all_labels.nc,973+905',
            '../data/trainset_diff_no_start_all_labels.nc,1082+554',
            '../data/trainset_diff_no_start_all_labels.nc,1495+898',
            '../data/trainset_diff_no_start_all_labels.nc,1970+378',
            '../data/trainset_diff_no_start_all_labels.nc,1561+872',
            '')

    payload = {'text': text,
               'style': style_models[style],
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


def add_color(color, image_out):
    img = Image.open(image_out)
    width, height = img.size
    for x in range(width):
        for y in range(height):
            old_color = list(img.getpixel((x, y)))
            new_color = [old_color[x] + color[x]
                         for x in range(3)]
            img.putpixel((x, y), tuple(new_color))
    img.save(image_out)


def command_line():
    args = get_arguments()

    if args.file:
        with open(args.file, 'r') as fl:
            text_in = [i.strip() for i in fl.readlines()]
    elif args.text:
        text_in = [args.text]

    style = args.style
    start_at = args.position
    bias = args.bias

    color = args.color
    color = color.replace(' ', '')
    color = color.split(',')
    color = list(map(int, color))

    if not os.path.exists('images'):
        print('Creating images folder')
        os.makedirs('images')

    print('Starting handwriting generation')
    for index, line in enumerate(text_in):
        if index < start_at:
            continue
        if not line.strip() == '':
            print(index, ' - ', line, end='')
            image_str = get_handwriting(line, style, bias)
            x = base64.b64decode(image_str)
            image_out = os.path.join('images', str(index) + '.png')
            with open(image_out, 'wb') as fl:
                fl.write(x)
            print('|')

    if not color == [0, 0, 0]:
        add_color(color, image_out)


if __name__ == '__main__':

    command_line()
