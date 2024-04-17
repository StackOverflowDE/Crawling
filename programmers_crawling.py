#!/usr/bin/env python
# coding: utf-8

# In[6]:


import csv
from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Chrome()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
code = 26500


url = 'https://career.programmers.co.kr/job_positions/'

def get_job_data(job_url):
    try:
        driver.get(url=job_url)
        driver.implicitly_wait(3)
    
        soup = BeautifulSoup(driver.page_source, "html.parser")

    # 직무 이름 추출
        job_title = soup.find("div", class_="KWImVsDeFt2E93NXqAqt").find("h2").text.strip()

    # 직무 카테고리 추출
        job_role = soup.find("div", class_="KACXxUyP7jEgxQYiU_Bq").find_all("div", role="cell")[1].get_text(strip=True)
        
    # 기술 스택 추출
        tech_stack_elements = soup.find_all("li", class_="QdgvMJO9ZYOaiwrEUqgo nUBs27jXBxRVUu9DLzz4")
        tech_stack = [element.text.strip() for element in tech_stack_elements]

        if tech_stack:  # 기술 스택이 비어있지 않은 경우에만 데이터 반환
            return {"job_title": job_title, "job_role": job_role, "tech_stack": tech_stack}
        else:
            return None
        
    except Exception as e:
        print(e)

data_list = []

for n in range(code, 27200, 1):
    job_url = url + str(n)
    job_data = get_job_data(job_url)
    if job_data:
        data_list.append(job_data)

driver.quit()


# 결과를 csv 형식으로 저장합니다.
csv_file_path = "job_data.csv"
with open(csv_file_path, "w", encoding="utf-8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["job_title", "job_role", "tech_stack"])
    writer.writeheader()
    for job_data in data_list:
        writer.writerow(job_data)


# In[ ]:




