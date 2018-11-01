import logging
from destination.fetcher import Fetch
from interact_csv import getSearchDict, writeDictToCSV

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opts = Options()
#opts.headless = True
#assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

try:
    f = Fetch(browser)

    to_search = getSearchDict()
    output = {}

    for destination in to_search:
        try:
            print ('Processing Country : {0} with {1} items'.format(destination, len(to_search[destination])))
            output[destination] = f.get(destination, to_search[destination])
        except Exception as e:
            logging.exception(e)

    writeDictToCSV(output)

except Exception as e:
    logging.exception(e)

finally:
    browser.close()
    quit()

