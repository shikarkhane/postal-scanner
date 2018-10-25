from destination.fetcher import Fetch

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)




itemId_CZ = ['LM129846996SE','LM129847020SE','LM129847081SE','LM129847245SE','LM129847501SE','LM129847603SE',
             'LM129847784SE','LM129848405SE','LM129848590SE','LM129848714SE']

item_br = ['LB159046570SE','LB159046583SE']

item_il = ['LB158853994SE', 'LB158854059SE', 'LB158854080SE', 'RE906210072SE', 'RE906210205SE']

item_srilanka = ['RE165006654SE','RE165006813SE','RE165006844SE','RE165006929SE','RE165006950SE','RE165007164SE',
                'RE165007283SE', 'RE165007460SE','RE165007535SE','RE165007589SE']

item_canada = ['CD330678425SE','CD380838845SE']

item_portugal = ['LM129847634SE']

item_kuwait = ['RD211078576SE']

item_chile = ['RD211070334SE']

f = Fetch('None')

# (u'LM129846996SE', True, u'18.9.2018')
# 20 codes max
# res = f.getCZ(itemId_CZ, browser)

# 50 codes max
#res = f.getBR(item_br, browser)

# [f.getSriLanka(i, browser) for i in item_srilanka]

#canada max 24
#f.getCanada(item_canada, browser)

# portugal max 25
#f.getPortugal(item_portugal, browser)

#[f.getKuwait(i, browser) for i in item_kuwait]

#[f.getChile(i, browser) for i in item_chile]



browser.close()
quit()

