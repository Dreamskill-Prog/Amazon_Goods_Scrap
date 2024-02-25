from bs4 import BeautifulSoup
import requests
import os, os.path, csv
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import re
from selenium.webdriver.common.keys import Keys



def main():
    product_dataset = {
        '商品のURL': [],
        'タイトル': [],
        '商品説明': [],
        '金額': [],
        'ASIN': [],
        '評価': [],
        '企業名': [],
        '評価数': [],
        'カラー名': []
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"]) 
    # options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=options)
    sub_browser = webdriver.Chrome(options=options)
    
    wait = WebDriverWait(browser, 20)
    sub_wait = WebDriverWait(sub_browser, 30)
    

    starturl = "https://www.amazon.co.jp/"
    print("スタート!")
    
    browser.get(starturl)
    sub_browser.get(starturl)
    
    lang_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="icp-nav-flyout"]/span')))
    lang_btn.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="icp-language-settings"]/div[2]/div/label/span/span'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="icp-save-button"]/span/input'))).click()
    
    sub_lang_btn = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="icp-nav-flyout"]/span')))
    sub_lang_btn.click()
    sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="icp-language-settings"]/div[2]/div/label/span/span'))).click()
    sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="icp-save-button"]/span/input'))).click()
    
    search_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
    search_input.clear()
    search_input.send_keys("JACKALL ルアー")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="nav-search-submit-button"]'))).click()
    
    result_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[data-component-type="s-product-image"]')))
    goods_count = 0
    print(len(result_elements))
    
    for result in result_elements:
        product_name = ""
        product_descrption = ""
        product_ASIN = ""
        product_review = ""
        product_review_count = ""
        
        try:
            goods_count = goods_count + 1
            
            print(f'{goods_count}   {result.text}')
            # browser.switch_to.window(browser.window_handles[0])
            
            sub_url = result.find_element(By.TAG_NAME, 'a').get_attribute("href")
            # //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]
            # //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/span/div/div/div[1]
            # //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[6]/div/div/span/div/div/div[1]/span/a
            print("商品のURL  ---------->"  +  sub_url)
            # response = requests.get(sub_url)
            # soup = BeautifulSoup(response.text, "html.parser")
            
            
            # sub_browser.switch_to.window(sub_browser.window_handles[0])
            sub_browser.get(sub_url)
            product_name = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productTitle"]'))).text
            product_descrption = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="feature-bullets"]/ul'))).text
            
            # price_element = browser.find_elements(By.XPATH, '//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]')
            # if len(price_element) > 0:
            #     product_price = price_element[0].text
            # else:
            #     product_price = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]'))).text
            
            product_ASIN = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td'))).text
            product_review = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span'))).text
            product_review_count = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="acrCustomerReviewText"]'))).text       
            product_review_count = re.search(r'\d+', product_review_count).group()

            print("タイトル  ---------->" + product_name)
            print("商品説明  ---------->" + product_descrption)
            # print("金額   ---------->" + product_price)
            print("ASIN   ---------->" + product_ASIN)
            print("評価   ---------->" + product_review)
            print("評価数   ---------->" + product_review_count)
            # //*[@id="variation_color_name"]/ul
            
            # browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'w') 
            
            # time.sleep(1000)
            
            # my_dataset.at[goods_count, '商品のURL'] = sub_url
            # my_dataset.at[goods_count, 'タイトル'] = product_name
            # my_dataset.at[goods_count, '商品説明'] = product_descrption
            # my_dataset.at[goods_count, '金額'] = product_price
            
            # my_dataset.at[goods_count, 'ASIN'] = product_ASIN
            # my_dataset.at[goods_count, '評価'] = product_review
            # my_dataset.at[goods_count, '企業名'] = cur_com_url
            # my_dataset.at[goods_count, '評価数'] = product_review_count
            # my_dataset.at[goods_count, 'カラー名'] = cur_com_url
        except Exception as e:
            print({e})
            pass


        # my_dataset.to_csv(f'amazon.csv', index=False)
        
    sub_browser.quit()
    browser.quit()
    
    # "JACKALL ルアー"
    
    
    
    
    
    
    
    # search_input.send_keys(Keys.RETURN)
    
    time.sleep(1000)
    
    
    
    prev_url = cur_url

    response = requests.get(starturl)
    soup = BeautifulSoup(response.text, "html.parser")

    A = soup.find(class_="section A1120")

    big_temps = A.find_all("li")

    for big_temp in big_temps:
        big_category_links.append(big_temp.find(class_="clearfix").get("href"))
        big_category_names.append(big_temp.find(class_="clearfix").find_all('span')[0].get_text())

       
    # print(big_category_links)
    row_big = 16
    
    # open('Log.txt', 'w', encoding='utf-8') as myfile:
    #     print("Sakura")

    
                

    for big_category_linkss in big_category_links:
        
        my_dataset = pd.DataFrame(product_dataset)
            
        print(datetime.datetime.now())

        row_big = row_big + 1
        big_category_link = big_category_links[row_big - 1]

        

        try:
            my_dataset = pd.read_csv(f'{row_big}.csv')
            my_dataset.at[1, '企業サイトURL']  = "asdfasdfsdfa"
            # my_dataset.to_csv(f'{row_big}.csv', index=False)
            print(len(my_dataset))
            # time.sleep(1000)

        except Exception as e:
            print({e})
            pass
        
        prev_url = ""
        prev_com_url = ""
        it = 17817
        while it <= len(my_dataset):
            response = requests.get(my_dataset.loc[it, '製品ページURL'])
            soup = BeautifulSoup(response.text, "html.parser")

            print(f"{it}")
            # print(my_dataset.loc[it, '企業サイトURL']) 
            # # print(my_dataset.loc[it, '企業サイトURL'])
            # # print(my_dataset.loc[it, '企業サイトURL'].find("http"))
            # if(int(my_dataset.loc[it, '企業サイトURL'].find("http")) > -1):
            #     continue


            try:
                cur_url = "https://ls.ipros.jp" + soup.find(class_="content__inner__center").find(class_="content-head__text__company").a.get("href")
            except Exception as e:
                print({e})
                pass

            # print(cur_url)

            try:

                if cur_url != prev_url:
                    browser.get(cur_url)
                    cur_com_url = sub_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="company_info_home_page"]/a'))).get_attribute("href").split("&url=")[1]
                    prev_url = cur_url
            except Exception as e:
                print({e})
                pass

            my_dataset.at[it, '企業サイトURL'] = cur_com_url

            # print(f'{it} -->  {cur_com_url}')

            my_dataset.to_csv(f'{row_big}.csv', index=False)

            it = it + 1

                        

        # print(medium_category_name)




if __name__ == "__main__":
    main()
