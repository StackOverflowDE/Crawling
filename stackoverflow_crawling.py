import csv, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def stackoverflow_crawling(language):
    sof_convert = {
        'Apache Spark' : 'apache-spark',
        'Babel' : 'babeljs',
        'C#' : 'c%23',
        'ES6' : 'es6-promise',
        'Google Cloud Platform' : 'google-cloud-platform',
        'HTML5' : 'html',
        'Jest' : 'jestjs',
        'REST API' : 'rest',
        'React Native' : 'react-native',
        'Ruby on Rails' : 'ruby-on-rails',
        'Shell Script' : 'shell',
        'Spring Boot' : 'spring-boot',
        'Amazon Web Services(AWS)' : 'amazon-web-services',
        'C++' : 'c%2b%2b',
        'MVVM(Model-View-ViewModel)' : 'mvvm'
    }
    re_sof_convert = {
        'apache-spark' : 'Apache Spark',
        'babeljs' : 'Babel',
        'c%23' : 'C#',
        'es6-promise' : 'ES6',
        'google-cloud-platform' : 'Google Cloud Platform',
        'html' : 'HTML5',
        'jestjs' : 'Jest',
        'rest' : 'REST API',
        'react-native' : 'React Native',
        'ruby-on-rails' : 'Ruby on Rails',
        'shell' : 'Shell Script',
        'spring-boot' : 'Spring Boot',
        'amazon-web-services' : 'Amazon Web Services(AWS)',
        'c%2b%2b' : 'C++',
        'mvvm' : 'MVVM(Model-View-ViewModel)'
    }
    
    # language 변수의 값이 sof_convert 딕셔너리의 키에 있는지 확인하고 변경
    if language in sof_convert:
        language = sof_convert[language]
    
    driver.get("https://stackoverflow.com/questions/tagged/{}?tab=active&page=1&pagesize=15".format(language))
    
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
    
    # 인덱스가 리스트의 길이보다 작을 때 반복
    while i <= len(id_list):
        # 요소 찾기
        question_title = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/h3/a'.format(id_list[i-1]))
        question_time = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/div[2]/div[2]/time/a/span'.format(id_list[i-1]))
        question_writer = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/div[2]/div[2]/div/div/a'.format(id_list[i-1]))
        question_img = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/div[2]/div[2]/a/div/img'.format(id_list[i-1]))
        question_votes = driver.find_element(By.XPATH, '//*[@id="{}"]/div[1]/div[1]/span[1]'.format(id_list[i-1]))
        question_answers = driver.find_element(By.XPATH, '//*[@id="{}"]/div[1]/div[2]/span[1]'.format(id_list[i-1]))
        question_views = driver.find_element(By.XPATH, '//*[@id="{}"]/div[1]/div[3]/span[1]'.format(id_list[i-1]))
        question_url = driver.find_element(By.XPATH, '//*[@id="{}"]/div[2]/h3/a'.format(id_list[i-1]))
        # 이미지 소스 URL 가져오기
        img_src = question_img.get_attribute("src")
        
        # 요소의 title 속성값 가져와 sof_data에 저장
        sof_elem = {
            "title" : question_title.text,
            "time" : question_time.text,
            "writer" : question_writer.text,
            "votes" : question_votes.text,
            "answers" : question_answers.text,
            "views" : question_views.text,
            "url" : question_url.get_attribute('href'),
            "img" : img_src,
        }
        sof_data.append(sof_elem)
        i+=1
        
    # 이름 재변환
    if language in re_sof_convert:
        language = re_sof_convert[language]

    # assets/data/sof 폴더가 없으면 생성
    folder_git = os.path.join("assets","data","sof")
    if not os.path.exists(folder_git):
        os.makedirs(folder_git)
        
    # CSV 파일로 저장
    csv_file_path = os.path.join("assets", "data", "sof", "sof_info_{}.csv".format(language))
    
    # CSV 파일로 저장
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "time", "writer","votes","answers","views","url", "img"])
        writer.writeheader()
        for elem in sof_data:
            writer.writerow(elem)