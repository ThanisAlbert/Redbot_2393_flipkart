import time
from datetime import datetime, timedelta
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from Log.Log import Log
from Web.UpdateTracker import UpdateTracker
from Web.WebWait import WebWait

class scheduleslot(WebWait,Log):

    def __init__(self,driver,trackersht,ponum):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.trackersht = trackersht
        self.ponum = ponum
        self.poqty = 0
        self.log = self.getLogger()
        WebWait.__init__(self, self.wait)

    def consignment_confirmation(self):
        updatetracker = UpdateTracker(trackersht=self.trackersht)
        try:
            self.wait_for_element_byxpath("//button[contains(text(),'Next')]")
            self.wait_for_element_byxpath("//button[contains(text(),'Update Quantity')]")
            time.sleep(2)
            self.driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
            scheduleddate = self.getcalendaravailability(self.poqty)
            updatetracker.update_scheduleddate(self.ponum, scheduleddate,self.consginmentno)
            self.log.info(f"Consignment drafted on {scheduleddate}")
        except Exception as e:
            updatetracker.update_scheduleddate(self.ponum, "Consignment Confirmation Error","Consignment Confirmation Error")
            self.log.info(e)

    def schedule(self):
        try:
            updatequantiy_success = self.updatequantity()
            if updatequantiy_success == 1:
                self.log.info("Shedule update quantity success")
                self.consignment_confirmation()
            else:
                self.log.info("Schedule Error with updatequantity failure")
                updatetracker = UpdateTracker(trackersht=self.trackersht)
                updatetracker.update_po_consigmentstatus(self.ponum, "Error")
        except:
            self.log.info("Schedule Error with calendarfailure or updatequantity")
            updatetracker = UpdateTracker(trackersht=self.trackersht)
            updatetracker.update_po_consigmentstatus(self.ponum,"Error")

    def updatequantity(self):
        self.wait_for_element_byxpath("//button[contains(text(),'Update Quantity')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Update Quantity')]").click()
        self.wait_for_element_byxpath("//button[contains(text(),'Cancel')]")
        self.wait_for_element_byxpath("//button[contains(text(),'Confirm')]")
        self.wait_for_element_byxpath("//span[@class='select-wrap -pageSizeOptions']/select")
        select_element = self.driver.find_element_by_xpath("//span[@class='select-wrap -pageSizeOptions']/select")
        dropdown = Select(select_element)
        dropdown.select_by_value('50')
        time.sleep(2)
        self.wait_for_element_byxpath("//span[@class='select-wrap -pageSizeOptions']/select")
        time.sleep(2)
        self.wait_for_element_byxpath("//div[@class='rt-tr-group']")
        updatedivs = self.driver.find_elements_by_xpath("//div[@class='rt-tr-group']")
        maxcapacity = int(str(self.driver.find_element_by_xpath("//div[@class='src__Box-sc-1sbtrzs-0 Message-sc-15k607x-0 hNEOfd ikxXWc']").text).split("Capacity:")[1].strip())
        updateerr = 0

        for i in range(1,len(updatedivs)+1):
            try:
                if self.poqty<=maxcapacity:
                    updatetracker = UpdateTracker(trackersht=self.trackersht)
                    self.wait_for_element_byxpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][1]")
                    product = str(self.driver.find_element_by_xpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][1]").text).split("\n")[0].strip()

                    if product!="":
                        reqqty = int(str(self.driver.find_element_by_xpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div").text).split("/")[1].strip())
                        availqty = int(str(updatetracker.get_availableqty(self.ponum,product)))

                        element_xpath = "(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input"
                        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath(element_xpath))
                        self.driver.execute_script("arguments[0].value = '';",self.driver.find_element_by_xpath(element_xpath))

                        self.log.info(f"Required quantity: {reqqty}, Available quantity {availqty}")

                        if availqty<=reqqty:
                            self.driver.find_element_by_xpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input").send_keys(availqty)
                            self.poqty = self.poqty + availqty
                            updatetracker.update_slottedqty(self.ponum,product,availqty)
                            self.log.info(f"Slotted quantity {availqty}")
                        else:
                            self.driver.find_element_by_xpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input").send_keys(reqqty)
                            self.poqty = self.poqty + reqqty
                            updatetracker.update_slottedqty(self.ponum,product,reqqty)
                            self.log.info(f"Slotted quantity {reqqty}")

            except Exception as e:
                updateerr=1
                updatetracker = UpdateTracker(trackersht=self.trackersht)
                self.log.info("update error " + str(e))
                updatetracker.error(self.ponum,product)

        if updateerr==0:
            self.wait_for_element_byxpath("//button[contains(text(),'Confirm')]")
            confirmelement = self.driver.find_element_by_xpath("//button[contains(text(),'Confirm')]")
            self.driver.execute_script("arguments[0].click();", confirmelement)
            return 1
        else:
            return 0

    def getcalendaravailability(self,poqty):

        self.wait_for_element_byxpath("//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr")

        scheduleddate=""

        for i in range(1, 7):
            for j in range(1, 8):
                try:
                    day = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").text)
                    qty = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDayCaption-sc-ogb9ok-2 dbirnb']").text)

                    if qty >= poqty:
                        self.log.info(f"{day} _ {qty}")
                        scheduleddate = scheduleddate + ";  " + str(f"Day:{day}_Qty:{qty}")
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
                    if qty >= poqty:
                        self.log.info(f"{day} _ {qty}")
                        scheduleddate = scheduleddate + ";  " + str(f"Day:{day}_Qty:{qty}")
                except Exception as e:
                    pass


        self.wait_for_element_byxpath("//h2[@class='Header__PageHeader-sc-dobhjr-1 dSyxVf']")
        self.consginmentno = str(self.driver.find_element_by_xpath("//h2[@class='Header__PageHeader-sc-dobhjr-1 dSyxVf']").text).split("Schedule Consignment")[1].strip()
        print(self.consginmentno)
        return scheduleddate












