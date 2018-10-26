from destination.fetcher import Fetch
from interact_csv import getSearchDict

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opts = Options()
#opts.headless = True
#assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)


f = Fetch(browser)

to_search = getSearchDict()

for destination in to_search:
    print 'Country : {0}'.format(destination)
    f.get(destination, to_search[destination])


browser.close()
quit()

