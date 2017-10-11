import os
import sys
import base64
import requests

def get_handwriting(text, bias=0.8, samples=1):
    payload = {'text': text,
               'style': '../data/trainset_diff_no_start_all_labels.nc,1082+554',
               'bias': bias,
               'samples': samples}
    headers = {'Host': 'www.cs.toronto.edu',
               'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Referrer': 'http://www.cs.toronto.edu/~graves/handwriting.cgi',
               'Connection': 'keep-alive',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate'}
    url = 'http://www.cs.toronto.edu/~graves/handwriting.cgi'
    page = requests.get(url, headers=headers, params=payload)
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

os.remove('images')
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
