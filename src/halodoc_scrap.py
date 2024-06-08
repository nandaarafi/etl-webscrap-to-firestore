from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup


if __name__ == "__main__":
    url = "https://www.halodoc.com/"
    print("[INFO] Memulai Browser...")
    driver = webdriver.Chrome()
    print("[INFO] Browser berhasil dibuka.")
    driver.get(url)
    data = []
    jenis_obat = ''
    dosis_data = ''
    cara_minum = ''
    try:
        card_elements = driver.find_elements(By.CLASS_NAME, 'hd-base-card')
        for index, card_element in enumerate(card_elements):
            if index == 1:
                card_element.click()
                break
            # countHome += 1
        time.sleep(3)
        obat_kategori = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "category-dropdown")))
        obat_kategori.click()
        kategori_list = driver.find_elements(By.CLASS_NAME, "category-menu-icon")
        for index, kategori in enumerate(kategori_list):
            kategori.click()
            time.sleep(5)
            list_obat = driver.find_elements(By.CLASS_NAME, "custom-container__list__container__item--link")
            i = 1
            for index in range(10) :
                link = driver.find_element(By.XPATH, f"(//a[@rel='canonical'])[{i}]")
                link.click()
                
                time.sleep(2)
                

                #Product Detail Screen
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                img_tag = soup.find('img', class_="product-image")
                img_src = img_tag['src']
                product_text = soup.find('h1', class_="product-label").text
                print(f"Image Source: {img_src} || Label: {product_text}")
                roottags = soup.find_all('div', class_='property')
                for roottag in roottags:
                    details_product = roottag.find('div', class_='ttl-list')
                    if details_product:
                        detail_product = details_product.text
                        if detail_product.lower() == 'dosis':
                            dosis_data = roottag.find('div', class_='drug-detail')
                            if dosis_data:
                                dosis_text = dosis_data.text
                                # unwanted_prefix = "PENGGUNAAN OBAT INI HARUS SESUAI DENGAN PETUNJUK DOKTER."
                                # if dosis_text.startswith(unwanted_prefix):
                                #     dosis_text = dosis_text[len(unwanted_prefix):].strip()
                            else:
                                print("Dosis information not found.")
                        elif detail_product.lower() == 'golongan produk':
                            jenis_obat = roottag.find('div', class_='drug-detail')
                            if jenis_obat:
                                jenis_text = jenis_obat.text
                                print("Jenis Obat:", jenis_text)
                            else:
                                print("Jenis obat information not found.")
                        elif detail_product.lower() == 'aturan pakai':
                            cara_minum = roottag.find('div', class_='drug-detail')
                            if cara_minum:
                                cara_minum_text = cara_minum.text
                                print("Cara Minum:", cara_minum_text)
                            else:
                                print("Cara minum information not found.")
                    else:
                        print("Error None")
                data.append({
                    'Gambar': img_src,
                    'Jenis Obat': jenis_text,
                    'Nama': product_text,
                    'Dosis': dosis_text,
                    # 'Waktu': product_shop_name,
                    'Cara Minum': cara_minum_text
                
                })
                # driver.back()
                driver.execute_script("window.history.go(-1)")
                i += 1

                time.sleep(5)

            df = pd.DataFrame(data)
            df.to_csv("../resources/produk_raw.csv",index=False)
        
                

    except TimeoutException:
        print("Loading took too much time or element not found.")

    finally:
        driver.quit()