from destination.fetcher import Fetch
from interact_csv import getSearchDict, writeDictToCSV

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opts = Options()
#opts.headless = True
#assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)


f = Fetch(browser)

to_search = getSearchDict()
output = {}

for destination in to_search:
    print ('Processing Country : {0} with {1} items'.format(destination, len(to_search[destination])))
    output[destination] = f.get(destination, to_search[destination])

writeDictToCSV(output)

browser.close()
quit()

