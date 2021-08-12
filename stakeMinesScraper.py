from selenium import webdriver
import json
browser = webdriver.Chrome()

def write_to_json(conf, amnt):
    with open('stakeMines.json', 'r') as f:
        stakeMines = json.load(f)
    stakeMines[conf] = amnt
    with open('stakeMines.json', 'w') as f:
        json.dump(stakeMines, f)
    

browser.get("https://dicetrue.com/stake-mines-calculator/")
for i in range(1,25):
    for j in range(1,26-i):
        m = browser.find_element_by_xpath('//*[@id="m"]')
        d = browser.find_element_by_xpath('//*[@id="d"]')
        b = browser.find_element_by_xpath('//*[@id="bet"]')
        m.clear()
        d.clear()
        b.clear()
        m.send_keys(str(i))
        d.send_keys(str(j))
        b.send_keys(str(1))
        browser.find_element_by_xpath('//*[@id="calculate"]').click()
        text = browser.find_element_by_xpath('//*[@id="result"]').text
        write_to_json('m'+str(i)+'d'+str(j), text)
