import re
import math

def stringExistsIn(pattern, string):
    res = re.findall(pattern, string)
    if len(res) > 0:
        return True
    else:
        return False

def removeEmptyTags(soup):
    for x in soup.find_all():
        if len(x.text.strip()) == 0:
            x.extract()
    return soup

def removeTagsOfClass(soup, class_):
    for x in soup.find_all(class_=class_):
        x.extract()
    return soup

def getBatchesOfSize(data, size):
    result = []
    div = int(math.floor(len(data) / size))
    float_div = float(len(data)) / size

    if float_div > div:
        div = div + 1

    for i in range(div):
        result.append(data[i * size: (i+1) * size])

    return result

