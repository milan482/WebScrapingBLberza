from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

service = Service(GeckoDriverManager().install())
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True  

driver = webdriver.Firefox(service=service, options=firefox_options)

# Ovde menjaš ili dodaješ druge kompanije
codes = ["BMNT"]

def clean_number(number_text, column_name):
    # Ostavlja kolone AOP i Opis nepromenjene 
    if column_name in ["AOP", "Opis"]:
        return number_text.strip() if number_text.strip() else "0"
    
    if number_text:
        number_text = number_text.replace(".", "")
        number_text = number_text.replace(",", ".")
        try:
            return float(number_text)
        except ValueError:
            return 0.0
    return 0.0

type_data = {1: [], 2: [], 3: []}

report_names = {
    1: "bilans_stanja",
    2: "bilans_uspeha",
    3: "bilans_novcanih_tokova"
}

for code in codes:
    for type_id in range(1, 4):
        for year in range(2021, 2024):  # Ovde menjaš godine 
            url = f'https://www.blberza.com/Pages/FinRepBalance.aspx?code={code}&type={type_id}&year={year}&semiannual=0'
            driver.get(url)

            try:
                table = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ctl00_ctl00_Content_SideContent_dgBilans"))
                )
                print(f"Učitani podatci za kompaniju {code}, {year}, tip izvještaja {type_id}!")
            except Exception as e:
                print(f"Greška u učitavanju podataka za kompaniju {code},  {year}, tip izvještaja {type_id}: {e}")
                continue  

            # ----------------- Ekstrakcija podataka ------------------------
            rows = table.find_elements(By.TAG_NAME, "tr")
            data = []

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                row_data = []

                for idx, col in enumerate(cols):
                    col_text = col.text.strip()
                    column_name = "AOP" if idx == 0 else "Opis" if idx == 1 else "Other"
                    row_data.append(clean_number(col_text, column_name)) 

                if row_data:
                    if type_id == 1:
                        row_data = row_data[:5]
                    elif type_id in [2, 3]:
                        row_data = row_data[:3]

                    row_data.append(code)
                    row_data.append(year)

                    data.append(row_data)

            print(f"Dobijeno {len(data)} linija podataka za kompaniju {code}, {year}, tip izvještaja {type_id}.")
            
            # skladištenje podataka po tipu
            type_data[type_id].extend(data)

            time.sleep(1)

driver.quit()

# ------------------- Pisanje podatak u Excel -------------------------

file_names = {
    1: "bilans_stanja.xlsx",
    2: "bilans_uspeha.xlsx",
    3: "bilans_novcanih_tokova.xlsx"
}

for type_id in range(1, 4):
    report_name = report_names.get(type_id, f"Tip_{type_id}")
    file_name = file_names.get(type_id, f"report_{type_id}.xlsx")

    if type_id == 1:
        columns = ["AOP", "Opis", "Bruto tekuća", "Ispravka vrijednosti", "Neto tekuća", "Kompanija", "Godina"]
    else:
        columns = ["AOP", "Opis", "Bruto tekuća", "Kompanija", "Godina"]

    if type_data[type_id]:
        df = pd.DataFrame(type_data[type_id], columns=columns)

        df.to_excel(file_name, index=False)
        print(f"Podatci za {report_name} su sačuvani u Excel fajl '{file_name}'.")
    else:
        print(f"Nema podataka za {report_name}.")
