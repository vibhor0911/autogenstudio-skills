import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def callFlow_response(callUUid):
    driver = webdriver.Edge()
    vars = {}
    driver.get('https://ngc.skype.net/call/' + callUUid)  
    driver.set_window_size(1936, 1048)
    time.sleep(20)
    driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Pivot-text') and text()='Call Flow']").click()
    driver.find_element(By.XPATH, "//span[text()='Autodetect']").click()
    driver.find_element(By.XPATH, "//span[text()='SIP traffic between the SBC and SIP proxy']").click()
    driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Button-label') and text()='Filters']").click()
    filter_text = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Input string']")
    filter_text.click()
    filter_text.send_keys("SIP")
    driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Button-label') and text()='Add']").click()
    driver.find_element(By.XPATH, "//span[contains(@class, 'ms-Button-label') and text()='Focus']").click()

    row_details = driver.find_elements(By.CSS_SELECTOR, "div.sdRow")
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

    # Define regular expressions
    url_regex = r'sip:(.*?);'
    response_code_regex = r'SIP/2.0 (\d{3})'
    url, response_code = None, None
    # Loop through each element
    for item in row_data:
        # Extract URL
        url_match = re.search(url_regex, item[-1])
        if url_match:
            url = url_match.group(1) 
        
        # Extract Response Code
        response_code_match = re.search(response_code_regex, item[-1])
        if response_code_match:
            response_code = response_code_match.group(1)
        
    return {
        "SipProviderURL": url,
        "SIPreturnCode": response_code,
        "SIPRAWLogs": row_data
    } 

callFlow_response('call UUId')