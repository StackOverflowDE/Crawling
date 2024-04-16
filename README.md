내가 관심있는 개발 직군의 언어 및 기술스택의 랭킹, github의 repo와 StackOverFlow의 질문의 종류, 기술블로그의 동향을 시각화해서 표현

프로그래머스 [﻿https://career.programmers.co.kr/job?page=1&order=recent&job_category_ids={}](https://career.programmers.co.kr/job?page=1&order=recent&job_category_ids={})

직무로 필터링된 페이지의 포지션들의 각각의 링크에 들어간 뒤 기술스택들을 모두 가져와 저장합니다.

github [﻿github.com/topics/python?o=desc&s=stars](https://github.com/topics/python?o=desc&s=stars) 

github의 topics의 repository의 제목들을 크롤링 한 뒤 각각의 URL로 들어가고 Fork의 수와 Star 수, Watch수를 가져와 저장합니다.
repository의 최근 commit의 시간과 repository의 작성자의 아이콘을 추가로 가져오는 작업을 수행하였습니다.

StackOverFlow [﻿https://stackoverflow.com/questions/tagged/python?sort=RecentActivity&edited=true](https://stackoverflow.com/questions/tagged/python?sort=RecentActivity&edited=true)

StackOverFlow의 {기술}의 질문들을 가져온다음 질문의 title을 저장해 줍니다.
추가적으로 질문들의 날짜와 작성자의 id, 아이콘을 저장해줍니다.

~~대기업 기술블로그~~

~~어느 부분부터 어디까지 할지 모르겠습니다..?~~

---

~~python의 repository와 star를 매칭되게 json형태로 저장해보았습니다.</br>~~
~~fork수를 가져와야하는데 [﻿github.com/topics/python?o=desc&s=stars](https://github.com/topics/python?o=desc&s=stars)에는 folk수가 없더라구요</br>~~
~~repository의 이름을 링크에 넣는 방식으로 할지 selenium으로 클릭방식으로 할지 고민입니다.</br>~~
~~만약 후자로 한다면 매번 정보갱신과 크롤링 시간이 오래걸릴것같네요😅~~

---

# Crawling

[﻿github.com/topics/python?o=desc&s=stars](https://github.com/topics/python?o=desc&s=stars) 

[﻿github.com/topics/{}?o=desc&s={}.](https://github.com/topics/python?o=desc&s=forks)fomat(language).fomat(sort) 

크롤링할 내용

> star, folk 수 / 리포지토리 이름

---

~~언어~~

~~데이터엔지니어~~

~~**Python, SQL, Java, R, Scala**~~

~~서버/백엔드~~

~~**Java, Python, JavaScript, Go, C#, Ruby**~~

~~안드로이드~~

~~**Java, Kotlin**~~

~~IOS~~

~~**Swift, Objective-C**~~

~~프론트엔드~~

~~**JavaScript, HTML, CSS**~~
