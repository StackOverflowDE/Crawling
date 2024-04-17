import re, json , os, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

# repo_info의 값에서 사용자는 제외하고 뒤의 제목만 가져오기 위해 re라이브러리를 사용했습니다.
def extract_name(repository):
    match = re.match(r'.+?/([^/]+)$', repository)
    if match:
        return match.group(1)
    return None

'''
※필독!※
language와 sort_tag를 정보에 맞게 넣어주세요 language = 개발언어, sort_tag = 'stars' or 'forks'
로그인 상태를 확인해주세요 아이디와 비밀번호를 자신의 비밀번호와 아이디로 넣어주세요
'''

language = 
sort_tag = 
your_id = 
your_password = 

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get("https://github.com/topics/{}?o=desc&s={}".format(language, sort_tag))
    
    repositorys = driver.find_elements(By.CLASS_NAME, "f3 color-fg-muted text-normal lh-condensed")
    
    # 레포지토리 제목을 담을 리스트
    repo_info = []
    
    # 레포지토리 제목을 포함하는 태그 찾기
    repo_list = driver.find_elements(By.TAG_NAME, 'h3')
    
    # 태그에서 텍스트 가져오기
    for link in repo_list:
        repo_info.append(link.text)
    
    # 각 요소에서 공백을 없앤 새로운 리스트 생성
    repo_git_list = [item.replace(" ", "") for item in repo_info]

git_data = []

# assets 폴더가 없으면 생성
folder_name = "assets"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for repo_list in repo_git_list[:-1]:
    # WebDriver 초기화,
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get("https://github.com/" + repo_list)
        
        driver.implicitly_wait(5)
        # 페이지의 HTML 소스를 가져옵니다.
        html_source = driver.page_source

        # 로그인 상태를 나타내는 클래스명을 확인합니다.
        if 'logged-out' in html_source:
            # 내비게이션 바에서 "로그인" 버튼을 찾아 눌러봅시다.
            button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/header/div/div[2]/div/div/div/a")
            ActionChains(driver).click(button).perform()
        
            # "아이디" input 요소에 여러분의 아이디를 입력합니다.
            id_input = driver.find_element(By.XPATH, '//*[@id="login_field"]')
            ActionChains(driver).send_keys_to_element(id_input, your_id).perform()
        
            # "패스워드" input 요소에 여러분의 비밀번호를 입력합니다.
            pw_input = driver.find_element(By.XPATH, '//*[@id="password"]')
            ActionChains(driver).send_keys_to_element(pw_input, your_password).perform()
        
            # "로그인" 버튼을 눌러서 로그인을 완료합니다.
            login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div[4]/form/div/input[13]')
            ActionChains(driver).click(login_button).perform()
        
        driver.implicitly_wait(10)
        
        # 요소 찾기
        repo_watch = driver.find_element(By.ID, 'repo-notifications-counter')
        repo_fork = driver.find_element(By.ID, 'repo-network-counter')
        repo_stars = driver.find_element(By.ID, 'repo-stars-counter-star')
        repo_commit = driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div/main/turbo-frame/div/div/div/div[2]/div[1]/react-partial/div/div/div[3]/div[1]/table/tbody/tr[1]/td/div/div[3]/a/span/span[2]/span')
        
        # 요소를 찾기 위해 find_elements를 사용하여 리스트 형태로 반환합니다.
        recent_t = driver.find_elements(By.TAG_NAME, 'relative-time')
        repo_recent = recent_t[0].get_attribute('title')
        
        # 이미지 요소 찾기
        img_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div/main/div/div[1]/div[1]/div[1]/img')
        
        # 이미지 소스 URL 가져오기
        img_src = img_element.get_attribute("src")
        
        # 이미지 다운로드
        img_name = extract_name(repo_list) + ".jpg"  # 이미지 파일 이름 설정
        img_path = os.path.join("assets", "img", img_name)  # 이미지 파일 경로 설정
        
        # 이미지 다운로드 및 저장
        with open(img_path, "wb") as img_file:
            img_file.write(requests.get(img_src).content)
        
        # 요소의 title 속성값 가져와 git_data에 저장
        git_elem = {
            "name" : extract_name(repo_list),
            "fork" : repo_fork.get_attribute('title'),
            "stars" : repo_stars.get_attribute('title'),
            "recent_time" : repo_recent,
            "number_of_commit" : repo_commit.get_attribute('title'),
        }
        git_data.append(git_elem)

# git_data를 JSON으로 변환
repo_json = json.dumps(git_data)

json_file_path = os.path.join("assets", "data", "git_repo_info.json")

# JSON 파일로 저장
with open(json_file_path, 'w') as json_file:
    json_file.write(repo_json)