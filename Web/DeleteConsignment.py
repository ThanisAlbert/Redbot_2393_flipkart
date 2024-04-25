from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from Web.WebWait import WebWait

class deleteconsignment(WebWait):

    def __init__(self,driver,ponum):
        self.driver = driver
        self.ponum = ponum
        self.wait = WebDriverWait(self.driver, 3)
        WebWait.__init__(self, self.wait)

    def delete(self):
        try:
            self.driver.get("https://vendorhub.flipkart.com/#/vendor-portal/home")
            self.driver.get("https://vendorhub.flipkart.com/#/operations/consignment/list/created")
            self.wait_for_element_byxpath("//button[contains(text(),'Download List')]")
            self.wait_for_element_byxpath("//input[@placeholder='Search by Consignment, PO, FSN']")
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").send_keys(" ")
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").send_keys(self.ponum)

            self.wait_for_element_byxpath("(//li[@class='search-type-list-item'])[2]")
            self.driver.find_element_by_xpath("(//li[@class='search-type-list-item'])[2]").click()
            self.wait_for_element_byxpath("//a[contains(text(),'Schedule')]")
            self.wait_for_element_byxpath("//a[contains(text(),'Schedule')]/parent::div/following-sibling::div[1]")
            self.driver.find_element_by_xpath("//a[contains(text(),'Schedule')]/parent::div/following-sibling::div[1]").click()
            self.wait_for_element_byxpath("//a[contains(text(),'Schedule')]/parent::div/following-sibling::div[1]/div")
            self.driver.find_element_by_xpath("//a[contains(text(),'Schedule')]/parent::div/following-sibling::div[1]/div").click()
            self.wait_for_element_byxpath("//div[@class='src__Box-sc-1sbtrzs-0 SelectStyles__SelectStyleOverrides-sc-12fap0p-0 bPtRJg jMfDg']")
            self.driver.find_element_by_xpath("//div[@class='src__Box-sc-1sbtrzs-0 SelectStyles__SelectStyleOverrides-sc-12fap0p-0 bPtRJg jMfDg']").click()
            actions = ActionChains(self.driver)
            for i in range(4):
                actions.send_keys(Keys.ARROW_DOWN)
                actions.pause(0.5)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            self.wait_for_element_byxpath("//button[contains(text(),'Delete')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
            return 1
        except Exception as e:
            return 0


    def reusecodes(self):
        inputField = self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']")
        self.driver.execute_script("arguments[0].setAttribute('value', '""')", inputField);
        inputField = self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']")
        self.driver.execute_script("arguments[0].setAttribute('value', '" + self.ponum + "')", inputField)
        self.driver.find_element_by_xpath("//input[@placeholder='Search by Consignment, PO, FSN']").send_keys(Keys.BACK_SPACE)
        self.wait_for_element_byxpath("//div[@class='DayPicker_transitionContainer DayPicker_transitionContainer_1']")
        self.wait_for_element_byxpath("//div[@class='CalendarMonthGrid CalendarMonthGrid_1 CalendarMonthGrid__horizontal CalendarMonthGrid__horizontal_2']")
        self.wait_for_element_byxpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_2']//div//table//tr)[6]//td[1]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']")
        val = self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[6]//td[1]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").text
        self.wait_for_element_byxpath("//div[@class='CalendarMonth CalendarMonth_1']")
        self.wait_for_element_byxpath("//table[@class='CalendarMonth_table CalendarMonth_table_1']")
        username_element = self.driver.find_element_by_id("username")
        self.driver.execute_script("arguments[0].value = arguments[1]", username_element, self.username)
        password_element = self.driver.find_element_by_id("password")
        self.driver.execute_script("arguments[0].value = arguments[1]", password_element, self.password)
        #time.sleep(3)
        self.wait_for_element_bytagname('iframe')
        self.wait_for_element_byid('g-recaptcha-response')
        captcha_iframe = self.driver.find_element_by_tag_name('iframe')
        ActionChains(self.driver).move_to_element(captcha_iframe).click().perform()
        captcha_box = self.driver.find_element_by_id('g-recaptcha-response')
        self.driver.execute_script("arguments[0].click()", captcha_box)
        '''
                        self.wait = WebDriverWait(self.driver, 10)
                        while True:
                            try:
                                self.wait_for_element_byxpath("//button[@class='login-button vpp-button vpp-button-primary']")
                                self.driver.find_element_by_xpath("//button[@class='login-button vpp-button vpp-button-primary']").click()
                                self.wait_for_element_byxpath("//input[@id='select-vendor-VEN10806']")
                                break
                            except Exception as e:
                                pass
                        '''

    def reusecodes2(self):
        pass
        '''
        if today_day < new_date_day:
            for i in range(1, 7):
                for j in range(1, 8):
                    try:
                        day = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").text)
                        qty = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDayCaption-sc-ogb9ok-2 dbirnb']").text)

                        if qty >= poqty and day>=new_date_day and scheduleddate=="" :
                            qtyelem = self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']")
                            self.driver.execute_script("arguments[0].click();", qtyelem)
                            self.wait_for_element_byxpath("//div[contains(text(),'Selected Date:')]")
                            time.sleep(0.5)
                            scheduleddate = str(self.driver.find_element_by_xpath("//div[contains(text(),'Selected Date:')]").text).split(":")[1]
                    except Exception as e:
                        pass

        else:
            self.wait_for_element_byxpath("//button[@aria-label='Move forward to switch to the next month.']")
            self.driver.find_element_by_xpath("//button[@aria-label='Move forward to switch to the next month.']").click()
            for i in range(1, 7):
                for j in range(1, 8):
                    try:
                        day = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']").text)
                        qty = int(self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDayCaption-sc-ogb9ok-2 dbirnb']").text)
                        if qty >= poqty and day >= new_date_day and scheduleddate=="":
                            qtyelem = self.driver.find_element_by_xpath("(//div[@class='CalendarMonthGrid_month__horizontal CalendarMonthGrid_month__horizontal_1']//div//table//tr)[" + str(i) + "]//td[" + str(j) + "]//div[@class='styles__CalendarDay-sc-ogb9ok-1 dbRdnm']")
                            self.driver.execute_script("arguments[0].click();", qtyelem)
                            time.sleep(0.5)
                            scheduleddate = str(self.driver.find_element_by_xpath("//div[contains(text(),'Selected Date:')]").text).split(":")[1]
                    except Exception as e:
                        pass
                        
        #element_xpath = "(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input"
                            #self.driver.execute_script("arguments[0].value = arguments[1];",self.driver.find_element_by_xpath(element_xpath), availqty)
        self.driver.find_element_by_xpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input").click()
        self.driver.find_element_by_xpath("(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input").clear()
        #element_xpath = "(//div[@class='rt-tr-group'])[" + str(i) + "]//div[@class='rt-td'][6]//div//input"
                            #self.driver.execute_script("arguments[0].value = arguments[1];",self.driver.find_element_by_xpath(element_xpath), reqqty)
        
        '''





