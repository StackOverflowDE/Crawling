import os
from github_crawling import *
from stackoverflow_crawling import *

'''
※필독!※
language와 sort_tag를 정보에 맞게 넣어주세요 language = 개발언어, sort_tag = 'stars' or 'forks'
로그인 상태를 확인해주세요 아이디와 비밀번호를 자신의 비밀번호와 아이디로 넣어주세요
'''

stack_list = []

language = "개발언어"
your_id = "아이디"
your_password = "비밀번호"

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    for i in stack_list:
        git_crawling(i,"아이디", "비밀번호")

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    for i in stack_list:
        stackoverflow_crawling(i)