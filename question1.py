from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

keywords = ['ipad','air','bud','apple','huawei']

result = {'ipad':0,'air':0,'bud':0,'apple':0,'huawei':0}

base_url = 'http://10.113.178.219/'


def findAllItems(driver, keyword):
    parent_div = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]')
    # get all child div
    child_divs = parent_div.find_elements(By.XPATH, './div')

    matching_div_indices = []

    for index, child_div in enumerate(child_divs):
        try:
            title_element = child_div.find_element(By.XPATH, './div/div/a/div/strong')
            title_text = title_element.text
            if keyword in title_text:
                matching_div_indices.append(index + 1)  # 索引从1开始
        except:
            continue
    
    return matching_div_indices

def main():
    driver = webdriver.Chrome()
    driver.get(base_url)
    for index in range(3):
        for pageNum in range(1,17):
            driver.get(base_url + "page/" + str(index))
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div[2]/div[1]/div/div/a/div/strong'))
            )
            matching_div_indices = findAllItems(driver, keywords[index])
            if(matching_div_indices != []):
                price_list = []
                for divNum in matching_div_indices:
                    divXpath = f'//*[@id="root"]/main/div/div[2]/div[{divNum}]/div/div/h3'

                    h3_element = driver.find_element(By.XPATH, divXpath)
                    priceNum = int(h3_element.text.replace("$", ""))
                    
                    price_list.append(priceNum)
                

                if (index <3):
                    price = sum(price_list) / len(price_list)
                    result[keywords[index]] = price
                    return result
                else:
                    if(pageNum != 16):
                        continue
                    else:
                        price = sum(price_list) / len(price_list)
                        result[keywords[index]] = price
                        return result
            else:
                continue


    driver.quit()

print(main())