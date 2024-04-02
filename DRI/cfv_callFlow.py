import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TestHoops():
  def setup_method(self, url):
    self.driver = webdriver.Edge()
    self.vars = {}
    self.url = url
  
  def teardown_method(self):
    self.driver.quit()
  
  def test_hoops(self):
    self.driver.get(self.url)        
    self.driver.set_window_size(1936, 1048)
    time.sleep(20)

    self.driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Pivot-text') and text()='Call Flow']").click()
    self.driver.find_element(By.XPATH, "//span[text()='Autodetect']").click()
    self.driver.find_element(By.XPATH, "//span[text()='SIP traffic between the SBC and SIP proxy']").click()
    self.driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Button-label') and text()='Filters']").click()
    filter_text = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Input string']")
    filter_text.click()
    filter_text.send_keys("SIP")
    self.driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Button-label') and text()='Add']").click()
    self.driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Button-label') and text()='Focus']").click()
    
    row_details = self.driver.find_elements(By.CSS_SELECTOR, "div.sdRow")
    row_data = []
    
    for row in row_details:
        column_data = []
        column_data.append(row.find_element(By.CSS_SELECTOR,"div.sdLineNumber").text.strip())
        column_data.append(row.find_element(By.CSS_SELECTOR,"div.sdTime").text.strip())
        arrow_element = row.find_element(By.CSS_SELECTOR,"div.sdArrow")
        element_class = arrow_element.get_attribute("class")
        if 'right' in element_class:
            column_data.append("right")
        elif 'left' in element_class:
            column_data.append("left")
        else:
           column_data.append("NA")
        column_data.append(row.find_element(By.CSS_SELECTOR,"div.sdLatency").text.strip())
        column_data.append(row.find_element(By.CSS_SELECTOR,"div.sdNote > span").text.strip())
        row_data.append(column_data)
    
    return row_data

url= "url"
test = TestHoops()
test.setup_method(url)
test.test_hoops()
test.teardown_method()