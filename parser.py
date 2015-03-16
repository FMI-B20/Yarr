import requests
from BeautifulSoup import BeautifulSoup
import re

headers = {
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
}

# The url for the list of all restaurants here
search_url = "http://www.restograf.ro/srchpage/?a=&submit.x=25&submit.y=7&submit=Cautare"
response = requests.get(search_url, headers = headers)

print search_url + " : " + str(response.status_code) + " " + str(response.reason)

if response.status_code != 200:
	exit()

main_soup = BeautifulSoup(response.text)

content = main_soup.body.find('div', attrs={'class' : 'SrchGroupResult'})
group_soup = BeautifulSoup(str(content))
index = 0
for div in group_soup.findAll('div'):
	anchor = div.span.a
	restaurant_name = anchor.text.encode('cp850', errors='replace').decode('cp850')
	
	# Restaurant names have (inchis) at the end if it's closed, so we skip it.
	if restaurant_name.endswith('(inchis)') :
		continue
	
	index = index + 1
	
	restaurant_response = requests.get(anchor.get('href'), headers = headers)
	print anchor.get('href') + " : " + str(restaurant_response.status_code) + " " + str(response.reason)
	
	if restaurant_response.status_code != 200 :
		continue

	print str(index) + ". " + restaurant_name
	
	restaurant_soup = BeautifulSoup(restaurant_response.text);
	main_content = restaurant_soup.find('div', attrs={'id' : 'main_content'})
	container_divs = main_content.findAll('div', attrs={'style' : 'width:298px; min-height:300px; float:right; margin-left:15px;'})
	
	if not container_divs:
		continue
	
	sub_divs = container_divs[0].findAll('div', attrs={'style' : 'width:294px;  min-height:51px; border:solid 1px #EBEBEB; float:left;'})
	
	if not sub_divs:
		continue

	href_divs = sub_divs[0].findAll('div', attrs={'style' : 'min-height:51px; width:283px; float:left; margin:8px 3px 6px 9px;'})

	if not href_divs:
		continue

	restaurant_address = href_divs[0].a.text.encode('cp850', errors='replace').decode('cp850')
	
	print restaurant_address

	info_divs = main_content.findAll('div', attrs={'style' : 'width:252px; height:220px; float:left; margin-left:10px; line-height:24px;'})

	if not info_divs:
		continue

	dummy_text =info_divs[0].text
	start = dummy_text.find('Bucatarie:') + len('Bucatarie:')
	end = dummy_text.find('Dominanta:')
	restaurant_cuisine = dummy_text[start : end].split('; ')

	print restaurant_cuisine

	# The lat lon are located in a script >.<
	result_lat = re.search('lat\s*=\s*parseFloat\s*\(\s*\'\s*-?\d*\.{1}\d*\s*\'\s*\)\s*;', restaurant_response.text).group()
	result_lon = re.search('long\s*=\s*parseFloat\s*\(\s*\'\s*-?\d*\.{1}\d*\s*\'\s*\)\s*;', restaurant_response.text).group()
	latitude = re.search('-?\d*\.{1}\d*', result_lat).group();
	longitude = re.search('-?\d*\.{1}\d*', result_lon).group();
	print latitude + " , " + longitude
