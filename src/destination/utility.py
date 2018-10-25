import re


def stringExistsIn(pattern, string):
    res = re.findall(pattern, string)
    if len(res) > 0:
        return True
    else:
        return False

def removeEmptyTags(soup):
    for x in soup.find_all():
        if len(x.text) == 0:
            x.extract()
    return soup

def removeTagsOfClass(soup, class_):
    for x in soup.find_all(class_=class_):
        x.extract()
    return soup