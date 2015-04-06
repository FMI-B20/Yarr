import requests
from BeautifulSoup import BeautifulSoup
from unidecode import unidecode
from main.models import Place,Cuisine,LocationType
import re
# -*- coding: utf-8 -*-


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
	restaurant_name = unidecode(anchor.text)

	# Restaurant names have (inchis) at the end if it's closed, so we skip it.
	if restaurant_name.endswith('(inchis)') :
		continue
	
	index = index + 1

	#if anchor.get('href') != 'http://www.restograf.ro/restaurant-hard-rock-cafe-bucuresti/':
		#continue

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

	href_a = href_div.find('a')

	if href_a is None:
		continue

	restaurant_address = unidecode(href_a.text)
	
	print restaurant_address

	phone_number_p = href_div.find('p', attrs={'style' : 'line-height:21px;'})
	phone_numbers = []
	if phone_number_p is not None:
		phone_numbers = "".join(phone_number_p.text.split()).replace('.','').split(',')

	print phone_numbers

	img_container_div = main_content.find('div', attrs={'style' : 'width:284px; height:206px; border-bottom:solid 8px #ECECEC; border-top:solid 8px #ECECEC; border-left:solid 6px #ECECEC; border-right:solid 6px #ECECEC; float:left; margin-left:5px;'})

	restaurant_image_url = None
	
	if img_container_div is not None:
		img_sub_div = img_container_div.find('div', attrs={'style' : 'overflow:hidden; width:284px; height:206px;'})
		img_anchor = img_sub_div.find('a')
		if img_anchor is not None and img_anchor.has_key('href'):
			restaurant_image_url = img_anchor['href']
		else:
			img_node = img_anchor.find('img')
			if img_node is not None and img_node.has_key('src'):
				restaurant_image_url = img_node['src']

	if restaurant_image_url is None or restaurant_image_url == '/img/Arici-pt-poze-implicite.jpg':
		restaurant_image_url = '/images/dummy_restaurant.png'

	print restaurant_image_url

	info_div = main_content.find('div', attrs={'style' : 'width:252px; height:220px; float:left; margin-left:10px; line-height:24px;'})

	if info_div is None:
		continue

	dummy_text = info_div.text
	start = dummy_text.find('Bucatarie:') + len('Bucatarie:')
	end = dummy_text.find('Dominanta:')
	restaurant_cuisines = unidecode(dummy_text[start : end]).split('; ')	

	start = dummy_text.find('Tip:') + len('Tip:')
	end = dummy_text.find('Pozitionare')
	restaurant_types = unidecode(dummy_text[start : end]).split('; ')

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
	new_place = Place.objects.filter(name__iexact = restaurant_name, address__iexact = restaurant_address).first()
	if new_place is None:
		new_place = Place.objects.create(name = restaurant_name, address = restaurant_address, location_lat = latitude, location_lon = longitude, image_url = restaurant_image_url);
	
	new_place.name = restaurant_name
	new_place.address = restaurant_address
	new_place.location_lat = latitude
	new_place.location_lon = longitude
	
	if (len(phone_numbers) > 0):
		new_place.phone_number1 = phone_numbers[0]

	if (len(phone_numbers) > 1):
		new_place.phone_number2 = phone_numbers[1]

	new_place.image_url = restaurant_image_url

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


