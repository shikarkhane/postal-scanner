# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from utility import stringExistsIn, removeEmptyTags, removeTagsOfClass, getBatchesOfSize
import requests
import time


# 5 out of 17 have captcha
class Fetch:
    def __init__(self, browser):
        self.browser = browser

    def batchCall(self, get_function, item_superset, batch_size, sleep_time):
        outcome = []
        for itemset in getBatchesOfSize(item_superset, batch_size):
            r = get_function(itemset, self.browser)
            outcome.extend(r)
            time.sleep(sleep_time)
        return outcome

    def singleCall(self, get_function, items, sleep_time):
        outcome = []
        for item in items:
            r = get_function(item, self.browser)
            outcome.extend(r)
            time.sleep(sleep_time)
        return outcome

    def get(self, country, itemIds):
        if country == 'CZ':
            return self.batchCall(self.getCZ, itemIds, 20, 5)
        elif country == 'BR':
            return self.batchCall(self.getBR, itemIds, 50, 5)
        elif country == 'CN':
            return self.batchCall(self.getCanada, itemIds, 24, 5)
        elif country == 'PT':
            return self.batchCall(self.getPortugal, itemIds, 25, 5)
        elif country == 'KW':
            return self.singleCall(self.getKuwait, itemIds, 5)
        elif country == 'CH':
            return self.singleCall(self.getChile, itemIds, 5)
        elif country == 'LK':
            return self.singleCall(self.getSriLanka, itemIds, 5)
        else:
            print ('nothing')

    def getCZ(self, itemIds, browser):
        output = []
        url = 'https://www.postaonline.cz/en/trackandtrace/-/zasilka/cislo?parcelNumbers={0}'.format(','.join(itemIds))
        browser.get(url)
        try:
            search_result = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "parcelInfo"))
            )
        finally:
            if search_result:
                tbody = search_result.get_attribute('innerHTML')
                soup = BeautifulSoup(tbody, 'html.parser')

                for row in soup.tbody.findChildren(['tr']):
                    columns = row.findChildren(['td'])
                    item_id = columns[0].strong.a.text.strip()
                    item_status = columns[0].text.strip()
                    if item_status.find('The consignment was delivered') >= 0:
                        item_delivered = True
                    else:
                        item_delivered = False
                    date_delivered = columns[1].text.strip()
                    output.append([item_id, item_delivered, date_delivered])

            else:
                print ('Country: {0}, Website has changed.'.format('Czech'))
        return output

    def getBR(self, itemIds, browser):
        output = []
        main_page = 'https://www2.correios.com.br/sistemas/rastreamento/default.cfm'
        browser.get(main_page)

        try:
            input_area = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "objetos"))
            )
            input_area.clear()
            input_area.send_keys(','.join(itemIds))
            browser.find_element_by_id("btnPesq").click()

            search_results = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tblSroResultado"))
            )

        finally:
            table = search_results.get_attribute('innerHTML')
            soup = BeautifulSoup(table, 'html.parser')
            for row in soup.tbody.findChildren(['tr']):
                columns = row.findChildren(['td'])
                item_id = columns[1].text.strip()
                item_status = columns[2].text.strip()
                if stringExistsIn('Objeto entregue ao destinat.rio', item_status) >= 0:
                    item_delivered = True
                else:
                    item_delivered = False
                date_delivered = columns[3].text.strip().split(' ')[0]
                output.append([item_id, item_delivered, date_delivered])

        return output


    def getIL(self, itemId, browser):
        # problem: english website is not reliable and native site has css ::before selectors used to display results. Selenium is not able to find it
        main_page = "https://mypost.israelpost.co.il/%D7%9E%D7%A2%D7%A7%D7%91-%D7%9E%D7%A9%D7%9C%D7%95%D7%97%D7%99%D7%9D"
        browser.get(main_page)

        try:
            search_box = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "ItemCode"))
            )
            search_box.clear()
            search_box.send_keys(itemId)

            browser.find_element_by_id("btn-ItemCode").click()

            search_results = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
        except Exception as e:
            print (e)
        finally:
            table = search_results.get_attribute('innerHTML')
            soup = BeautifulSoup(table, 'html.parser')
            pass


    def getRO(self, itemIds, browser):
        #romainia has google captcha
        # json response
        #
        # awb=dfsfsf&lang=en&recaptcha=03AMGVjXjQloP241hXzLMDkzitySNqnyVaoECtnzhfh8VzVZU8lWM4OWGqgmpPrObHtOQpIbHOGk73hR_02LfI9IZJqkI3E7k2v5vZMML6YLsKLk78u6x9DbVxud23xza9Mi90oozAmfUee-N5Y1it-Hhrxjyk0nvuCuGwugqFI0MGroNMXm3pfr97nyIzAJi2YB4RhOUL7-spSjG0SxF1I2sJ13TJ5eaYlpx1prABFXdsIxCP44OmiTH6S88u7mohRNnMs34ZPHpnLVdi7AXnWCBKA1VDwRueOQ
        url = 'https://www.posta-romana.ro/cnpr-app/modules/track-and-trace/ajax/status.php'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getKazakistan(self, itemIds, browser):
        # html response
        # couldnt get response
        url = 'https://post.kz/mail/search/track/{0}/detail'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getSriLanka(self, itemId, browser):
        output = []
        url = 'http://globaltracktrace.ptc.post/gtt.web/Search.aspx'
        browser.get(url)

        try:
            search_box = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "txtItemID"))
            )
            search_box.clear()
            search_box.send_keys(itemId)

            browser.find_element_by_id("btnSearch").click()

            search_results = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "resultsPanel"))
            )
        except Exception as e:
            print (e)
        finally:
            table = search_results.get_attribute('innerHTML')
            soup = BeautifulSoup(table, 'html.parser')
            item_id = itemId
            item_status = soup.find_all('table')[0].text.strip()
            if stringExistsIn('Delivered', item_status) >= 0:
                item_delivered = True
            else:
                item_delivered = False
            date_delivered = soup.find_all('table')[1].find_all('tr')[1].td.text
            output.append([item_id, item_delivered, date_delivered])
        return output

    def getCanada(self, itemIds, browser):
        # json response
        output = []
        url = 'https://www.canadapost.ca/trackweb/rs/track/json/package?pins={0}'.format(','.join(itemIds))
        r = requests.get(url)
        rj = r.json()
        for item in rj:
            item_id, item_delivered, date_delivered = item["pin"], item["delivered"], item["actualDlvryDate"]
            output.append([item_id, item_delivered, date_delivered])
        return output

    def getPortugal(self, itemIds, browser):
        output = []

        items_to_search = ','.join(itemIds)
        url = "https://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx?lang=01"

        browser.get(url)

        try:
            search_box = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "objects"))
            )
            search_box.clear()
            search_box.send_keys(items_to_search)

            browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Track Delivery'])[1]/following::input[2]").click()

            search_results = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "objectSearchResult"))
            )
        except Exception as e:
            print (e)
        finally:
            table = search_results.get_attribute('innerHTML')
            soup = BeautifulSoup(table, 'html.parser')
            soup = removeEmptyTags(soup)
            soup = removeTagsOfClass(soup, 'hide')

            for row in soup.tbody.findChildren(['tr']):
                columns = row.findChildren(['td'])
                item_id = columns[0].text.strip()
                item_status = columns[4].text.strip()
                if stringExistsIn('Item delivered', item_status) >= 0:
                    item_delivered = True
                else:
                    item_delivered = False
                date_delivered = columns[1].text.strip()
                output.append([item_id, item_delivered, date_delivered])
        return output

    def getKuwait(self, itemId, browser):
        output = []

        url = "http://tracking.moc.gov.kw/english/"
        browser.get(url)

        try:
            search_box = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.ID, "itemid"))
            )
            search_box.clear()
            search_box.send_keys(itemId)

            browser.find_element_by_name("Submit").click()

            search_results = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "200"))
            )
        except Exception as e:
            print (e)
        finally:
            table = search_results.get_attribute('innerHTML')
            soup = BeautifulSoup(table, 'html.parser')

            last_row = [row for row in soup.tbody.find_all(['tr'])][-1]
            columns = last_row.findChildren(['td'])
            item_id = itemId
            item_status = columns[3].text.strip()
            if stringExistsIn('Deliver item', item_status) >= 0:
                item_delivered = True
            else:
                item_delivered = False
            date_delivered = columns[0].text.strip()
            output.append([item_id, item_delivered, date_delivered])
        return output

    def getChile(self, itemId, browser):
        output = []
        url = 'https://www.correos.cl/SitePages/seguimiento/seguimiento.aspx?envio={0}'.format(itemId)
        browser.get(url)

        try:
            results_frame = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            browser.switch_to_frame('ifSeguimiento')

            search_results = browser.find_elements_by_class_name('tracking')
        except Exception as e:
            print (e)
        finally:
            table = search_results[0].get_attribute('innerHTML')
            soup = BeautifulSoup(table, 'html.parser')

            first_row = [row for row in soup.tbody.find_all(['tr'])][1]
            columns = first_row.findChildren(['td'])
            item_id = itemId
            item_status = columns[0].text.strip()
            if stringExistsIn('ENVIO ENTREGADO', item_status) >= 0:
                item_delivered = True
            else:
                item_delivered = False
            date_delivered = columns[1].text.strip()
            output.append([item_id, item_delivered, date_delivered])
        return output

    def getCroatia(self, itemIds, browser):
        # html response
        # google captcha
        # broj2=RB267096010HR&g-recaptcha-response=03AMGVjXg3DBQLcrdilw004sZCMmgTRQwkk-RfswI3piVeuO0WZeKF2jwfuQrV21bF_W9Fz7ly_ZMR9PwKOCPmSl5RmwEhuhJS47zMKbBzwr8OCJoStHTyPXdCMZve1ujU4Aksth2YwlfdwuA0yXfEU79YNIhkNInOp1rLUzKWjCCnGax5NkVddbYYiePWnt7_XfJIqDm_5qG0BWAKTjTLVSoT47zY5lJgZX6wYxiRwU8-fc7TGYvBbsheeydLw2Ak1qKq7gnrT_tCJ5JYbq7fTNmV5Q6W7isr-g&hiddenRecaptcha=&tracklng=en
        url = 'https://www.posta.hr/tracktrace.aspx'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getSaudiArabia(self, itemIds, browser):
        # html response
        url = 'https://sp.com.sa/en/Electronic/Pages/TrackShipment.aspx?k={0}'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getGreece(self, itemIds, browser):
        # html response
        url = 'https://www.elta.gr/en-us/personal/tracktrace.aspx?qc={0}'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getThailand(self, itemIds, browser):
        # html response
        # some captcha
        url = 'http://track.thailandpost.co.th/tracking/default.aspx?lang=en'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getHungary(self, itemIds, browser):
        # html response
        # google captcha
        url = ''.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getAustralia(self, itemIds, browser):
        # json response
        url = 'https://digitalapi.auspost.com.au/shipmentsgatewayapi/watchlist/shipments?trackingIds={0}'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getUK(self, itemIds, browser):
        # dont have packet id
        url = ''.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getSpain(self, itemIds, browser):
        # captcha
        url = ''.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getSlovania(self, itemIds, browser):
        # captcha
        url = ''.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getLithuania(self, itemIds, browser):
        # html response
        # body
        # parcel_numbers=EE123456789LT&op=Paie%C5%A1ka&form_build_id=form-tQ8qggsQSEGAcec2DiYlye1-GJ-QG4zYPRB9x3DtGwA&form_id=shipment_tracking_search_form
        url = 'https://www.post.lt/lt/pagalba/siuntu-paieska'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getBahrain(self, itemIds, browser):
        # captcha
        url = 'https://www.post.lt/lt/pagalba/siuntu-paieska'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getSlovakia(self, itemIds, browser):
        # parcel id needed
        url = 'https://www.post.lt/lt/pagalba/siuntu-paieska'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getFrance(self, itemIds, browser):
        # html response
        #suivi%5Bnumber%5D=12345678901&provenance=1
        url = 'https://www.laposte.fr/particulier/outils/suivre-vos-envois'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getGermany(self, itemIds, browser):
        # html response
        # form.sendungsnummer=BB1234567890&form.einlieferungsdatum_tag=&form.einlieferungsdatum_monat=&form.einlieferungsdatum_jahr=2018
        url = 'https://www.deutschepost.de/sendung/simpleQueryResult.html'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getBelgium(self, itemIds, browser):
        # json response
        url = 'https://track.bpost.be/btr/api/items?itemIdentifier={0}'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text

    def getSwitzerland(self, itemIds, browser):
        # html response
        url = 'https://service.post.ch/EasyTrack/submitParcelData.do?formattedParcelCodes={0}&from_directentry=True&directSearch=false&p_language=en&VTI-GROUP=1&lang=en&service=ttb'.format(','.join(itemIds))
        results = browser.find_element_by_id('parcelInfo')
        return results[0].text







































