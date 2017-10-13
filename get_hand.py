import os
import sys
import base64
import requests

def get_handwriting(text, bias=0.8, samples=1):
    payload = {'text': text,
               'style': '../data/trainset_diff_no_start_all_labels.nc,1082+554',
               'bias': bias,
               'samples': samples}
    url = 'http://www.cs.toronto.edu/~graves/handwriting.cgi'
    page = requests.get(url, params=payload)
    text = page.text
    print('.', end='')
    search_string = '<img src="data:image/jpeg;base64,'
    start = text.find(search_string) + len(search_string)
    image_str = text[start:-5]
    return image_str


with open(sys.argv[1], 'r') as fl:
    lines = [i.strip() for i in fl.readlines()]

start_at = 0
try:
    start_at = int(sys.argv[2])
except IndexError:
    pass

if not os.path.exists('images'):
    print('Creating images folder')
    os.makedirs('images')

 

print('Starting handwriting generation')
for index, line in enumerate(lines):
    if index < start_at:
        continue
    if line.strip() != '':
        print(index, ' - ', line, end='')
        image_str = get_handwriting(line)
        x = base64.b64decode(image_str)
        with open('images/'+str(index)+'.png', 'wb') as fl:
            fl.write(x)
        print('|')
