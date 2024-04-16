user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

import re
import requests
from bs4 import BeautifulSoup

'''
language와 sort_tag를 정보에 맞게 넣어주세요 language = 개발언어, sort_tag = 'stars' or 'forks'
language = 
sort_tag = 
'''

# repo_info의 값에서 사용자는 제외하고 뒤의 제목만 가져오기 위해 re라이브러리를 사용했습니다.
def extract_name(repository):
    match = re.match(r'.+?/([^/]+)$', repository)
    if match:
        return match.group(1)
    return None


res = requests.get("https://github.com/topics/{}}?o=desc&s={}".format(language, sort_tag), user_agent)
soup = BeautifulSoup(res.text, "html.parser")

# repository의 타이틀을 가져와 각각의 페이지로 이동하기 위해 저장해줍니다..
repositorys = soup.find_all("h3", class_=("f3 color-fg-muted text-normal lh-condensed"))
repo_info = []
for repository in repositorys:
    repo_info.append(repository.text.replace('\n', '').replace(' ', ''))

# 제목, watch, forks, stars수를 저장할 리스트를 만들어줍니다.
git_data = []


# 각 repo별 url 요청
for repo_list in repo_info:
    res_repo = requests.get("https://github.com/" + repo_list , user_agent)
    soup_repo = BeautifulSoup(res_repo.text, "html.parser")
    
    # repo_watch는 안긁어와지는데 해결가능할까요
    # watch, forks, stars수 수집
    repo_watch = soup_repo.find("span", id= "repo-notifications-counter")
    repo_fork = soup_repo.find("span", id="repo-network-counter")
    repo_stars = soup_repo.find("span", id="repo-stars-counter-star")

    # 최종 데이터 dictionary 및 데이터 리스트에 추가
    git_elem = {
        "name" : extract_name(repo_list),
        "watch" : repo_watch,
        "fork" : repo_fork['title'],
        "stars" : repo_stars['title']
    }
    git_data.append(git_elem)
    
    
'''
# 수집된 데이터 파일 저장       
with open("../data/github.pkl", "wb") as f:
    pickle.dump(git_data, f)
'''
    
'''
# 마지막으로 JSON을 만드는 코드입니다.
import json

# 리스트를 딕셔너리로 변환
repo_dict = dict(git_data)

# 딕셔너리를 JSON으로 변환
repo_json = json.dumps(repo_dict)

# JSON 파일로 저장
with open('repo_info.json', 'w') as json_file:
    json_file.write(repo_json)
'''