import csv
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def collect():
    options = Options()
    options.add_experimental_option("detach", True)
    # options.add_argument("--start-maximized")
    options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    try:
        print("Coletando dados de: https://sicrediconexao.com.br")

        driver.get("https://sicrediconexao.com.br")
        driver.implicitly_wait(3)

        allow_cookies_button = driver.find_element(
            "xpath", "/html/body/div[3]/main/div/section/div/button[2]"
        )

        if allow_cookies_button.is_displayed():
            allow_cookies_button.click()

        product_menu = driver.find_element(
            "xpath", "/html/body/header/div/nav/ul/li[2]/a"
        )

        if not product_menu.is_displayed():
            menu = driver.find_element("xpath", "/html/body/header/div/div[3]")
            menu.click()
            product_menu = driver.find_element(
                "xpath", "/html/body/header/div/nav/ul/li[2]/a"
            )

        product_menu.click()

        all_products = driver.find_element("class name", "section-all-products")

        if all_products:
            products = []
            product_titles = all_products.find_elements("tag name", "h2")
            product_list = all_products.find_elements("css selector", "div.products")

            for i, title in enumerate(product_titles):
                items = product_list[i].find_elements("css selector", "div.product")
                products.extend(
                    [{"Categoria": title.text, "Produto": item.text} for item in items]
                )

            if not products:
                driver.quit()
                return

            with open('./Produtos.csv', 'w', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["Categoria", "Produto"])
                writer.writeheader()
                writer.writerows(products)

        print("Coleta finalizada com succeso")
        driver.quit()
    except Exception:
        print("Erro ao coletar dados")
        traceback.print_exc()
        driver.quit()


collect()
