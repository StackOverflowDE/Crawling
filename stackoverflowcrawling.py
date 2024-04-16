user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

import requests
from bs4 import BeautifulSoup

# 필터로 어떤걸 가져올지 몰라 'RecentActivity'로 필터링했습니다. 
# 'MostVotes'로 필터링할 시 너무 오래된 정보가 나오기 때문에 기간을 정할 수 없어서 최근에 활발한 질문을 가져오는게 취지에 부합하다는 생각이 들었습니다.
# 'language'는 입력해주세요
res = requests.get("https://stackoverflow.com/questions/tagged/{}?sort=RecentActivity&edited=true".format(language), user_agent)
soup = BeautifulSoup(res.text, "html.parser")

sof_data = []
title = soup.find_all("h3", class_=("s-post-summary--content-title"))


for title_result in title:
    sof_list={
        "title" : title_result.text.strip('\n')
    }
    sof_data.append(sof_list)