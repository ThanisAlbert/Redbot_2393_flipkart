import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from Chromedriver.Chromedriver import Chromedriver
from Log.Log import Log
from Web.DeleteConsignment import deleteconsignment
from Web.ScheduleSlot import scheduleslot
from Web.UpdateTracker import UpdateTracker
from Web.WebWait import WebWait
from selenium.webdriver.support import expected_conditions as EC

class WebNavigate(WebWait,Log):

    def __init__(self,username,password):
        self.log = self.getLogger()
        self.chrome = Chromedriver(downloadpath="d:\\", headless=False)
        self.driver = self.chrome.chromedriver()
        self.username =username
        self.password = password
        self.wait = WebDriverWait(self.driver, 40)
        WebWait.__init__(self,self.wait)

    def login(self):

        while(True):

            try:

                self.wait = WebDriverWait(self.driver, 180)
                self.driver.maximize_window()
                #time.sleep(5)
                self.driver.get("https://vendorhub.flipkart.com/#/vendor-portal/home")
                self.log.info("Flipkart Page Loaded")
                self.wait_for_element_byid("username")
                time.sleep(5)
                self.driver.find_element_by_id("username").send_keys(self.username)
                self.wait_for_element_byid("password")
                time.sleep(2)
                self.driver.find_element_by_id("password").send_keys(self.password)
                time.sleep(2)

                self.wait_for_element_byxpath("//input[@id='select-vendor-VEN10806']")
                self.driver.find_element_by_xpath("//input[@id='select-vendor-VEN10806']").click()
                self.wait_for_element_byxpath("//button[contains(text(),'NEXT')]")
                self.driver.find_element_by_xpath("//button[contains(text(),'NEXT')]").click()
                #self.driver.minimize_window()
                self.log.info("Logged in successfully")
                break

            except Exception as e:
                self.driver.close()
                self.chrome = Chromedriver(downloadpath="d:\\", headless=False)
                self.driver = self.chrome.chromedriver()
                self.wait = WebDriverWait(self.driver, 40)
                self.log.info("Tried Again ")

    def draftconsignment(self,ponum,tracker_sht):

        self.ponum = ponum; self.tracker_sht = tracker_sht
        self.log.info(f"***************************{self.ponum}***********************************")
        self.driver.get("https://vendorhub.flipkart.com/#/operations/po/details/" + self.ponum)
        self.wait_for_element_byxpath("(//div[contains(text(), 'Status')])[2]/following-sibling::div[1]")
        status = self.driver.find_element_by_xpath("(//div[contains(text(), 'Status')])[2]/following-sibling::div[1]").text

        updatetracker = UpdateTracker(trackersht=self.tracker_sht)
        updatetracker.update_postatus(ponum,status)

        if status.strip().upper()=="APPROVED":

            while True:

                self.driver.get("https://vendorhub.flipkart.com/#/operations/po/details/" + self.ponum)

                while (True):
                    self.deleteconsignment = deleteconsignment(driver=self.driver, ponum=self.ponum)
                    consignment_present = self.deleteconsignment.delete()
                    if consignment_present == 0:
                        break
                    self.log.info(f"Consignment deleted successfully for {ponum}")

                self.driver.get("https://vendorhub.flipkart.com/#/operations/po/details/" + self.ponum)

                self.wait_for_element_byxpath("//button[contains(text(),'Create Consignment')]")

                button = self.driver.find_element_by_xpath("//button[contains(text(), 'Create Consignment')]")

                if button.is_enabled():
                    pass
                else:
                    self.log.info(f"Button is disabled for {ponum}")
                    xpath = "//div[@id='createCsgnBtn']"
                    #how to hover to xpath
                    break

                self.driver.find_element_by_xpath("//button[contains(text(),'Create Consignment')]").click()
                updatetracker = UpdateTracker(trackersht=tracker_sht)

                try:  # if_consignment_creation_possible
                    self.wait = WebDriverWait(self.driver, 5)
                    self.wait_for_element_byxpath("//button[contains(text(),'Update Quantity')]")
                    self.driver.find_element_by_xpath("//button[contains(text(),'Update Quantity')]")
                    try:  # if_slots_not_available
                        self.wait_for_element_byxpath("//div[@class='src__Box-sc-1sbtrzs-0 Message-sc-15k607x-0 hNEOfd fNesib']")
                        message= self.driver.find_element_by_xpath("//div[@class='src__Box-sc-1sbtrzs-0 Message-sc-15k607x-0 hNEOfd fNesib']").text
                        updatetracker.update_consignmentstatus(self.ponum, message)
                        self.log.info(f"{message}  {ponum}")
                        #self.scheduleslot = scheduleslot(driver=self.driver, trackersht=self.tracker_sht,ponum=self.ponum)
                        #self.scheduleslot.schedule()
                        #self.log.info(f"Consignment drafted Successfully for {ponum}")
                        self.deleteconsignment = deleteconsignment(driver=self.driver, ponum=self.ponum)
                        consignment_present = self.deleteconsignment.delete()
                        self.log.info(f"Consignment deleted successfully for {ponum}")
                        break
                    except Exception as e:  # if_slots_available
                        self.scheduleslot = scheduleslot(driver=self.driver,trackersht=self.tracker_sht, ponum=self.ponum)
                        self.scheduleslot.schedule()
                        self.log.info(f"Consignment drafted Successfully for {ponum}")
                        break
                except Exception as e:  # if_consignment_creation_not_possible
                    while (True):
                        self.deleteconsignment = deleteconsignment(driver=self.driver, ponum=self.ponum)
                        consignment_present = self.deleteconsignment.delete()
                        if consignment_present == 0:
                            break
                        self.log.info(f"Consignment drafted successfully for {ponum}")


    def createconsignment(self,consignmentno,selectdate):

        try:
            self.wait = WebDriverWait(self.driver, 20)
            self.log.info(f"***************************{consignmentno}***********************************")
            self.driver.get("https://vendorhub.flipkart.com/#/operations/consignment/list/created")
            self.wait_for_element_byxpath("//button[contains(text(),'Download')]")
            self.wait_for_element_byxpath("//input[@placeholder='Search by Consignment, PO, FSN']")
            self.wait_for_element_byxpath("//button[contains(text(),'Download List')]")
            self.wait_for_element_byxpath("//input[@placeholder='Search by Consignment, PO, FSN']")
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").send_keys(" ")
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").send_keys(Keys.BACK_SPACE)
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").send_keys(consignmentno)
            self.wait_for_element_byxpath("(//li[@class='search-type-list-item'])[1]")
            self.driver.find_element_by_xpath("(//li[@class='search-type-list-item'])[1]").click()
            self.wait = WebDriverWait(self.driver, 10)
            self.wait_for_element_byxpath("//a[contains(text(),'Schedule')]")
            time.sleep(1)
            self.driver.find_element_by_xpath("//a[contains(text(),'Schedule')]").click()
            self.log.info("Calendar page loaded")
            resultdate = "";
            fcnno = ""
            resultdate = self.selectcalendaravailability(selectdate)
            if resultdate != "":
                self.wait_for_element_byxpath("//button[contains(text(),'Schedule')]")
                self.driver.find_element_by_xpath("//button[contains(text(),'Schedule')]").click()  # Livecode
                self.wait_for_element_byxpath("//h3[contains(text(),'Your slot has been confirmed for')]/span")
                slotdate = self.driver.find_element_by_xpath("//h3[contains(text(),'Your slot has been confirmed for')]/span").text
                slottime = self.driver.find_element_by_xpath("//h3[contains(text(),'Reporting Time will be')]/span").text
                fcnno = slotdate + " " + slottime
            else:
                fcnno = "calendarnotselected"

        except Exception as e:
            fcnno="Notfound"

        return fcnno

    def selectcalendaravailability(self,selectdate):

        self.wait_for_element_byxpath("//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr")

        selecteddate=""

        for i in range(1, 7):
            for j in range(1, 8):
                try:
                    day = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").text)
                    qty = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDayCaption-sc-ogb9ok-2 dbirnb']").text)

                    if day==int(selectdate):
                        self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").click()
                        self.log.info(f"{day} _ {qty}")
                        selecteddate=day
                except Exception as e:
                    pass

        self.wait_for_element_byxpath("//button[@aria-label='Move forward to switch to the next month.']")
        self.driver.execute_script("document.querySelector(\"button[aria-label='Move forward to switch to the next month.']\").click();")
        time.sleep(1)

        for i in range(1, 7):
            for j in range(1, 8):
                try:
                    day = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").text)
                    qty = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDayCaption-sc-ogb9ok-2 dbirnb']").text)

                    if day == int(selectdate):
                        selecteddate = day
                        self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").click()
                        self.log.info(f"{day} _ {qty}")
                except Exception as e:
                    pass

        return selecteddate


























