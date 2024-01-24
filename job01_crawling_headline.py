#크롤링하는 방법 중 하나.
#데이터를 얻기 위해 크롤링으로 카테고리 분류해두기.(데이터 전처리)
from bs4 import BeautifulSoup  #pip install bs4로 설치. 크롤링하기 위해.
import requests #이것도 크롤링위해
import re
import pandas as pd
import datetime

# category = ['Politics', 'Economy', 'social', 'Culture', 'World', 'IT']
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
#
# resp = requests.get(url, headers) #requests에 이렇게 주소 주면 서버에 요청보내는 거고 서버에서 리턴을 준다.
# #print(list(resp)) #이러면 리턴값을 볼 수 있는데 보기 어렵게 되있다.
# #원래 브라우저가 리퀘스트 요청할 때 헤더에다 브라우져 정보를 담아서 준다
# #크롤링 리퀘스트는 헤더의 브라우져 정보가 없기때문에 이걸 보고 서버쪽에서 요청을 안 받아주는 경우가 있다.
# #만약 크롤링이 그냥했을 때 막히면 header를 저런식으로 줘서 보내면 해결할 수 있다.
#
# soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup) #이렇게 받으면 줄바꿈되면서 좀 보기 편하게 들어온다.
# title_tags = soup.select('.sh_text_headline') #sh앞의 .은 클래스일 때 붙인다. 이런 클래스쓰고 있는 애들 가져오겠다.
#                                                 #헤드라인기사들만 이 글씨체 쓰기 때문에 헤드라인 기사제목만 긁어올 수 있다.
# print(title_tags)
# print(len(title_tags)) #헤드라인 기사 10개
# print(type(title_tags[0])) #<class 'bs4.element.Tag'> 형태
#
# titles = []
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text)) #title_tag.text는 title_tag를 문자형으로 바꾸는것
#                                                                                #^ 뒤에거 빼고, ' '빈칸을 채워라(title_tag에)
#                                                                                #정규표현식 쓴것
#
# print(titles)




#url 뒤에 숫자만 바꿔주면서 정치,경제~ 세계거 가져오기

category = ['Politics', 'Economy', 'social', 'Culture', 'World', 'IT']
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re_title.sub(' ', title_tag.text))

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
#이 경로에 이런 파일명으로 넣겠다
#datetime은 시간 관련 파이썬 기본 패키지. now함수 호출하면 현재시간 알려줌 ns단위. 이걸 몇년 몇월 몇달로 보려면 strftime사용.
#몇월 몇일 뉴스인지 알기위해 datetime사용.