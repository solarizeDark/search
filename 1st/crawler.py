import requests
from bs4 import BeautifulSoup

# lesswrong home page
url_home = 'https://www.lesswrong.com'

# rationality a-z page
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
url = 'https://www.lesswrong.com/rationality#5g5TkQTe9rmPS5vvM'
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'html.parser')
spans = soup.find_all('div', {'class': 'SequencesSmallPostLink-title'})

cnt = 1
links = open('links.csv', 'w', encoding="utf-8")
links.write('number,link\n')
links.flush()
for el in spans:
	element_with_url = el.find('a', href=True)
	page_url = url_home + element_with_url['href']
	# page_name = element_with_url.contents[0]
	links.write(str(cnt) + ',' + page_url + '\n')
	links.flush()
	file = open('pages/' + str(cnt) + '.html', 'w', encoding="utf-8")
	file.write(requests.get(page_url, headers=headers).text)
	file.close()
	cnt += 1
links.close()
