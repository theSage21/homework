Handwritten
===========

Homework could have been so much easier if only it could be submitted as a typed copy.  
Using Alex Graves' paper on handwriting generation is a step I liked. 
This script uses his amazing paper (actually the free service he has set up online) to
generate handwritten homework for given text.

Usage
-----

```
usage: get_hand.py [-h] (-f FILE | -t TEXT) [-s STYLE] [-b BIAS] [-p POSITION]
                   [-c COLOR]

Plain text to handwriting generator.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  text file to generate handwriting from (default: None)
  -t TEXT, --text TEXT  text to generate handwriting from (default: None)
  -s STYLE, --style STYLE
                        handwriting style from 0 to 5, where 5 is random style
                        (default: 5)
  -b BIAS, --bias BIAS  handwriting bias from 0.1 to 1 (default: 0.8)
  -p POSITION, --position POSITION
                        start at specific position (default: 0)
  -c COLOR, --color COLOR
                        add custom RGB color values to generated text
                        (default: 0,0,0)
```

Example
-------

Generating handwritten text page from a file (with no more than 100 characters in each line) with handwriting style 4:
```
python get_hand.py -f desc.txt -s 4
python make_page.py
```
Now open `pages/1.png`:

![sample handwriting](https://i.imgur.com/9SPwYnd.png)

Generating handwritten text using a string in blue color & custom bias with handwriting style 2:
```
python get_hand.py -t "Homework could have been easier" -s 2 -c 0,0,200 -b 0.85
```
Now open `images/0.png`:

![blue ink](https://i.imgur.com/IrGDNx3.png)


More Info
---------

[The paper](http://arxiv.org/abs/1308.0850)  
[The man behind it all. Alex Graves](http://www.cs.toronto.edu/~graves/)  
[What I am using](http://www.cs.toronto.edu/~graves/handwriting.html)
