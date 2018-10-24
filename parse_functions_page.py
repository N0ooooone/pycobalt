#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.cobaltstrike.com/aggressor-script/functions.html'
out = 'aggressor.py'

sleep_functions = [
    'print',
    'println',
]

def main():
    print('downloading list')

    data = ''
    data += """
#
# For calling aggressor functions
#
# Warning: This file is auto-generated by ./parse_functions_page.py
#

import communicate

"""

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    print('parsing')

    # <h2><a href="#-is64">-is64</a></h2>
    functions = {}
    container = soup.find('div', {'class': 'col-lg-12'})
    
    # get names
    names = []
    for h2 in container.find_all('h2'):
        for a in h2.find_all('a'):
            names.append(a.text)

    # get docs
    docs = []
    for div in container.find_all('div'):
        doc = '\n'.join(['# ' + line.rstrip() for line in div.text.splitlines()])
        docs.append(doc)

    # zip together
    for name, doc in zip(names, docs):
        functions[name] = doc

    # add sleep functions
    for func in sleep_functions:
        functions[func] = None

    print('found {} functions'.format(len(functions)))

    for func, doc in functions.items():
        #max_arg = 0

        # add doc
        if doc:
            data += doc

            # find max arg
            #if '# Arguments' in doc:
            #    for match in re.finditer('\$([0-9]+)', doc):
            #        num = int(match.group(1))
            #        max_arg = max(num, max_arg)

        data += """
def {pyname}(*args):
    return communicate.call('{name}', args)

""".format(name=func, pyname=func.replace('-', ''))

    print('writing to {}'.format(out))
    with open(out, 'w+') as out_fp:
        out_fp.write(data)

if __name__ == '__main__':
    main()