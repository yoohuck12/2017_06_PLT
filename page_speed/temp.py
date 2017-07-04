__author__ = 'jnejati'
import re
import codecs


def already_minified(my_file2):
        #f = open(my_file2, 'r')
        f = codecs.open(my_file2, 'r', encoding='utf-8')
        try:
            my_chunk = f.read(50)
        except UnicodeDecodeError:
            return True
        if re.search(r"\s", my_chunk):
            return True
        else:
            return False

def main():
    if (already_minified("./mouseOver.js")):
        print('minified')
    else:
        print('not minified')


if __name__ == '__main__':
    main()