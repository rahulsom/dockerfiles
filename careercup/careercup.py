import os
import re
import requests
import sys
import glob
from builtins import len
from lxml import html


def strip_margin(text):
    return re.sub('\n[ \t]*\|', '\n', text)


def decorate(text, language):
    commenting = {
        'groovy': '//',
        'py': '#',
        'hs': '--',
        'java': '//',
        'scala': '//',
        'kt': '//',
        'rb': '#',
        'sh': '#',
    }
    commentSymbol = commenting[language]
    return commentSymbol + re.sub('\n', '\n' + commentSymbol, text)


def fetch_question(question_number, extension):
    url = "https://www.careercup.com/question?id=" + question_number
    page = requests.get(url)
    tree = html.fromstring(page.content)
    content = tree.xpath('//meta[@property="og:description"]/@content')[0]
    file = open('q' + question_number + '.' + extension, 'w')
    file.write(decorate(url + '\n\n' + content, extension))
    file.close()
    return True


def fetch_page(pagenum, extension, max, ignored):
    print("Reading from page %d" % (pagenum))
    page = requests.get("https://www.careercup.com/page?n=" + str(pagenum))
    tree = html.fromstring(page.content)
    count = 0
    skipped = 0
    for e in tree.cssselect('#question_preview li.question span.entry > a'):
        link = e.get("href")
        number = link.split('=')[1]
        isUnsolved = os.path.isfile('q' + number + '.' + extension)
        isDone = os.path.isfile('done/q' + number + '.' + extension)
        isIgnored = number in ignored
        if isUnsolved or isDone or isIgnored:
            skipped += 1
        else:
            if fetch_question(number, extension):
                print("  -> Fetched question " + number)
                count = count + 1
        if count == max:
            break
    print("Skipped %d. Read %d" % (skipped, count))
    return count


def ignore_question(question_number):
    q = glob.glob('q' + question_number + '.*')
    for f in q:
        os.remove(f)
    f = open('.ccignore', 'a')
    f.write(question_number + '\n')
    f.close()
    return


def fetch(max):
    if not os.path.isfile('.ccignore'):
        f = open('.ccignore', 'w')
        f.write('# Ignored questions from CareerCup\n')
        f.close()
    if not os.path.isdir('done'):
        os.mkdir('done')
    with open('.ccignore') as f:
        lines = f.read().splitlines()
    page = 1
    while True:
        max -= fetch_page(page, sys.argv[2], max, lines)
        page += 1
        if max == 0:
            break


def help():
    print(strip_margin("""
    |careercup
    |  CLI to fetch questions from CareerCup.com
    |
    |Usage:
    |  careercup fetch <language> [<questions>]
    |    Fetches <questions> questions from CareerCup. <questions> defaults to 10.
    |    Creates a file called q<question number>.<language>
    |  careercup ignore <question number>
    |    Puts question in ignored list and never fetches question again. You can
    |      look at .ccignore for list of ignored questions.
    """))


if len(sys.argv) == 3 and sys.argv[1] == 'ignore':
    ignore_question(sys.argv[2])
elif len(sys.argv) == 3 and sys.argv[1] == 'fetch':
    fetch(10)
elif len(sys.argv) == 4 and sys.argv[1] == 'fetch':
    fetch(int(sys.argv[3]))
else:
    help()
