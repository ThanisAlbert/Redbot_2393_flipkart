from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

class WebWait:

    def __init__(self,wait):
        self.wait = wait

            # Wait for the element to be present


    def wait_for_element_byxpath(self,element):
        self.wait.until(expected_conditions.presence_of_element_located((By.XPATH,element)))
        self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, element)))

    def wait_for_element_bytagname(self,element):
        self.wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME,element)))
        self.wait.until(expected_conditions.visibility_of_element_located((By.TAG_NAME,element)))

    def wait_for_element_byname(self, element):
        self.wait.until(expected_conditions.presence_of_element_located((By.NAME, element)))
        self.wait.until(expected_conditions.visibility_of_element_located((By.NAME, element)))

    def wait_for_element_byid(self, element):
        self.wait.until(expected_conditions.presence_of_element_located((By.ID, element)))
        self.wait.until(expected_conditions.visibility_of_element_located((By.ID, element)))

    def wait_for_element_byclassname(self, element):
        self.wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, element)))
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, element)))
