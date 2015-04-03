import requests
from BeautifulSoup import BeautifulSoup
from main.models import Place,Cuisine,LocationType
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

	if main_content is None:
		continue

	container_div = main_content.find('div', attrs={'style' : 'width:298px; min-height:300px; float:right; margin-left:15px;'})
	
	if container_div is None:
		continue
	
	sub_div = container_div.find('div', attrs={'style' : 'width:294px;  min-height:51px; border:solid 1px #EBEBEB; float:left;'})
	
	if sub_div is None:
		continue

	href_div = sub_div.find('div', attrs={'style' : 'min-height:51px; width:283px; float:left; margin:8px 3px 6px 9px;'})

	if href_div is None:
		continue

	restaurant_address = href_div.a.text.encode('cp850', errors='replace').decode('cp850')
	
	print restaurant_address

	info_div = main_content.find('div', attrs={'style' : 'width:252px; height:220px; float:left; margin-left:10px; line-height:24px;'})

	if info_div is None:
		continue

	dummy_text = info_div.text
	start = dummy_text.find('Bucatarie:') + len('Bucatarie:')
	end = dummy_text.find('Dominanta:')
	restaurant_cuisines = dummy_text[start : end].split('; ')	

	start = dummy_text.find('Tip:') + len('Tip:')
	end = dummy_text.find('Pozitionare')
	restaurant_types = dummy_text[start : end].split('; ')

	print restaurant_types
	print restaurant_cuisines

	# The lat lon are located in a script >.<
	search_lat_variable_result = re.search('lat\s*=\s*parseFloat\s*\(\s*\'\s*-?\d+(\.{1}\d*)?\s*\'\s*\)\s*;', restaurant_response.text)

	if search_lat_variable_result is None:
		continue

	latitude = re.search('-?\d+(\.{1}\d*)?', search_lat_variable_result.group()).group();

	search_lon_variable_result = re.search('long\s*=\s*parseFloat\s*\(\s*\'\s*-?\d+(\.{1}\d*)?\s*\'\s*\)\s*;', restaurant_response.text)
	
	if search_lon_variable_result is None:
		continue

	longitude = re.search('-?\d+(\.{1}\d*)?', search_lon_variable_result.group()).group()

	print latitude + " , " + longitude
	print "----------------------------"

	# Add them into database
	new_place = Place.objects.filter(name__iexact = restaurant_name).first()
	if new_place is None:
		new_place = Place.objects.create(name = restaurant_name, address = restaurant_address, location_lat = latitude, location_lon = longitude);
	
	new_place.name = restaurant_name
	new_place.address = restaurant_address
	new_place.location_lat = latitude
	new_place.location_lon = longitude
	new_place.location_types.clear()
	new_place.cuisines.clear()
	
	for restaurant_type in restaurant_types:
		existing_type = LocationType.objects.filter(name__iexact = restaurant_type).first()
		if existing_type is None:
			existing_type = LocationType.objects.create(name = restaurant_type)
			existing_type.save()
		new_place.location_types.add(existing_type)

	for restaurant_cuisine in restaurant_cuisines:
		existing_cuisine = Cuisine.objects.filter(name__iexact = restaurant_cuisine).first()
		if existing_cuisine is None:
			existing_cuisine = Cuisine.objects.create(name = restaurant_cuisine)
			existing_cuisine.save()
		new_place.cuisines.add(existing_cuisine)

	new_place.save()


