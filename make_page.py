import os
import sys
from PIL import Image


if os.path.exists('pages'):
    os.rmdir('pages')
print('Creating pages folder')
os.makedirs('pages')

try:
    line_count = sys.argv[1]
except IndexError:
    line_count = 20


def make_page(lines, count):
    images = [Image.open(i) for i in lines]
    no_of_lines = len(lines)
    size = (1500, 100)
    page_size = (size[0], size[1] * no_of_lines)
    page = Image.new('RGB', page_size, color='white')
    offset = 0

    for im in images:
        im.thumbnail(size)
        page.paste(im, (0, offset))
        offset += 100
    page.save('pages/' + str(count) + '.png')


lines = os.listdir('images')
ranked_paths = [(int(i[:-4]), 'images/' + i) for i in lines]
ranked_paths.sort()
paths = [i[1] for i in reversed(ranked_paths)]
count = 1
while paths:
    page = []
    for i in range(line_count):
        try:
            x = paths.pop()
        except IndexError:
            continue
        else:
            page.append(x)
    make_page(page, count)
    count += 1
