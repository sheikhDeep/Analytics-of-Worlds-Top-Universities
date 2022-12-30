from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time



columns = ["Rank", "University", "Location", "Country", "Overall Score", "IRN", "H-index", "Citations Per Paper", "Academic Reputation", "Employer Reputation"]
ranking_details = []

def get_uni_details(row):
    details = row.text.split('\n')
    # print(len(details))
    # print(details)
    contents = {}
    if "QS Stars" in details:
        contents['Rank'] = details[0].replace("=", "")
        contents['University'] = details[1]
        if ',' in details[2]:
            contents['Location'] = details[2].split(',')[0]
            contents['Country'] = details[2].split(',')[1].strip()
        else:
            contents['Location'] = details[2].strip()
            contents['Country'] = details[2].strip()
        contents['Overall Score'] = details[5]
        contents['IRN'] = details[6]
        contents['H-index'] = details[7]
        contents['Citations Per Paper'] = details[8]
        contents['Academic Reputation'] = details[9]
        contents['Employer Reputation'] = details[10]
    else:
        contents['Rank'] = details[0].replace("=", "")
        contents['University'] = details[1]
        if ',' in details[2]:
            contents['Location'] = details[2].split(',')[0]
            contents['Country'] = details[2].split(',')[1].strip()
        else:
            contents['Location'] = details[2].strip()
            contents['Country'] = details[2].strip()
        contents['Overall Score'] = details[3]
        contents['IRN'] = details[4]
        contents['H-index'] = details[5]
        contents['Citations Per Paper'] = details[6]
        contents['Academic Reputation'] = details[7]
        contents['Employer Reputation'] = details[8]
    return contents

def main():
    url = " https://www.topuniversities.com/subject-rankings/2022"
    web_driver_path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(web_driver_path)
    driver.get(url)
    

    #Social science button
    button = driver.find_element(By.CLASS_NAME, "block-block-contentcc88f621-01da-4a95-bcfb-a1b58a482cb7").find_element(By.CLASS_NAME, "btn-orrange")
    time.sleep(5)
    ActionChains(driver).move_to_element(button).click(button).perform()
    time.sleep(5)
    current = driver.current_url
    driver.get(current)

    #Ranking indicator button
    button = driver.find_element(By.CLASS_NAME, "ranking_tabs").find_element(By.CLASS_NAME, "last")
    ActionChains(driver).move_to_element(button).click(button).perform()
    time.sleep(5)

    for _ in range(51):
        rows = driver.find_elements(By.CLASS_NAME, "ind-row")
        for idx, row in enumerate(rows):
            ranking_details.append(get_uni_details(row))
        
        #Pagination button
        button = driver.find_element(By.CSS_SELECTOR, ".page-link.next")
        ActionChains(driver).move_to_element(button).click(button).perform()
        time.sleep(5)
    
    driver.close()

    # print(len(ranking_details))
    # print(ranking_details)
    df = pd.DataFrame(data=ranking_details, columns=columns)
    
    df.to_csv("world_uni_rank_by_soc_sci_and_man.csv", index=False)
    return

def dataset_cleaning():
    df = pd.read_csv(".\world_uni_rank_by_soc_sci_and_man.csv")
    print(len(df))
    overall_score_nil = df[df["Overall Score"] == "-"].index
    print(len(overall_score_nil))
    df.drop(overall_score_nil, inplace=True)
    print(len(df))
    df.to_csv("world_uni_rank_clean.csv")
    #print(df.head())




if __name__ == "__main__":
    main()
    dataset_cleaning()