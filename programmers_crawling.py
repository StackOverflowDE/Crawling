#!/usr/bin/env python
# coding: utf-8

# In[16]:


import json
from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Chrome()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
code = 26950


url = 'https://career.programmers.co.kr/job_positions/'

def get_job_data(job_url):
    try:
        driver.get(url=job_url)
        driver.implicitly_wait(3)
    
        soup = BeautifulSoup(driver.page_source, "html.parser")

    # 직무 이름 추출
        job_title = soup.find("div", class_="KWImVsDeFt2E93NXqAqt").text.strip()
        
    # 기술 스택 추출
        tech_stack_elements = soup.find_all("li", class_="QdgvMJO9ZYOaiwrEUqgo nUBs27jXBxRVUu9DLzz4")
        tech_stack = [element.text.strip() for element in tech_stack_elements]

        return {"job_title": job_title, "tech_stack": tech_stack}
        
    except Exception as e:
        print(e)

data_list = []

for n in range(code, 27100, 1):
    job_url = url + str(n)
    job_data = get_job_data(job_url)
    if job_data:
        data_list.append(job_data)

driver.quit()

# 결과를 JSON 형식으로 저장합니다.
with open("job_data.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)


