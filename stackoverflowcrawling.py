import re, json, os, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

language = "개발언어"

# assets 폴더가 없으면 생성
folder_name = "assets"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# assets/img/sof 폴더가 없으면 생성
folder_sof = "assets/img/sof"
if not os.path.exists(folder_sof):
    os.makedirs(folder_sof)

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get("https://stackoverflow.com/questions/tagged/{}?tab=active&page=1&pagesize=50".format(language))
    
    i = 1
    sof_data = []
    
    # title 경로 찾기
    id_list = []
    
    # 질문 요소들을 찾기 위한 XPath
    id_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "s-post-summary    js-post-summary")]')
    
    # 각 질문 요소에 대해 반복
    for id_element in id_elements:
        # 질문 요소의 id 속성 가져오기
        question_id = id_element.get_attribute("id")
        id_list.append(question_id)
    
    # 몇개의 단어를 뽑아올지 몰라서 일단 페이지 최대 갯수로 해보았습니다.
    while i <= 50:
        # 요소 찾기
        question_title = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/h3/a'.format(id_list[i-1]))
        question_time = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/div[2]/div[2]/time/a/span'.format(id_list[i-1]))
        question_writer = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/div[2]/div[2]/div/div/a'.format(id_list[i-1]))
        question_img = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/div[2]/div[2]/a/div/img'.format(id_list[i-1]))
        
        # 이미지 소스 URL 가져오기
        img_src = question_img.get_attribute("src")
        
        # 이미지 다운로드
        img_name = question_writer.text + ".jpg"  # 이미지 파일 이름 설정
        img_path = os.path.join("assets", "img", "sof", img_name)  # 이미지 파일 경로 설정
        
        # 이미지 다운로드 및 저장
        with open(img_path, "wb") as img_file:
            img_file.write(requests.get(img_src).content)
        
        # 요소의 title 속성값 가져와 git_data에 저장
        sof_elem = {
            "name" : question_title.text,
            "time" : question_time.text,
            "stars" : question_writer.text,
        }
        sof_data.append(sof_elem)
        i+=1
    
    # sof_data를 JSON으로 변환
    sof_json = json.dumps(sof_data)
    
    json_file_path = os.path.join("assets", "data", "sof_info.json")
    
    # JSON 파일로 저장
    with open(json_file_path, 'w') as json_file:
        json_file.write(sof_json)