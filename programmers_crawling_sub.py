import csv, os, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# page_max를 지정해주세요! 한페이지에 20개의 정보가 있답니다.
page_max = "페이지수"

page_num = '1'
i = 1
pro_data = []

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    while page_num >= page_max:
        driver.get("https://career.programmers.co.kr/job?page={}&order=recent".format(page_num))
        time.sleep(2)
        # 여러 요소를 찾습니다.
        except_elem = driver.find_elements(By.CLASS_NAME, 'external-label')

        # 각 요소에 대해 반복합니다.
        for elem_ex in except_elem:
            # style 속성의 값을 가져옵니다.
            style_attribute = elem_ex.get_attribute('style')

            # style 속성에 display: none;이 포함되어 있는지 확인
            if 'display: none;' in style_attribute:
                # i번째 페이지를 클릭해줍니다.
                button = driver.find_element(By.XPATH, '//*[@id="list-positions-wrapper"]/ul/li[{}]'.format(i))
                ActionChains(driver).click(button).perform()
            
                time.sleep(2)
            
            if len(driver.window_handles) > 1:

                # 새 탭의 핸들을 가져옴
                new_tab_handle = driver.window_handles[1]

                # 새 탭으로 전환
                driver.switch_to.window(new_tab_handle)

                # 새 탭에서 정보를 가져옴
                pro_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'h2')))
                pro_jobs = driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[1]/div[2]')
                pro_stacks = driver.find_elements(By.XPATH, '//*[contains(@class, "QdgvMJO9ZYOaiwrEUqgo") and contains(@class, "nUBs27jXBxRVUu9DLzz4")]')
                
                jobs_list = pro_jobs.text.split(', ')
                
                stacks_list = []
                
                for stack in pro_stacks:
                    stacks_list.append(stack.text)
                
                pro_elem = {
                    "title" : pro_title.text,
                    "jobs" : jobs_list,
                    "stacks" : stacks_list
                }
                pro_data.append(pro_elem)
                
                # 새 창이 열렸을 경우, 새 창을 닫음
                driver.close()  # 새 창 닫음
                driver.switch_to.window(driver.window_handles[0])  # 다시 원래 창으로 이동
            i+=1
        page_num += 1
    
# CSV 파일로 저장
csv_file_path = os.path.join("assets", "data", "pro_info.csv")

# CSV 파일로 저장
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["title", "jobs", "stacks"])
    writer.writeheader()
    for elem in pro_data:
        writer.writerow(elem)