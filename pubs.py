import urllib2
import simplejson
import stations

OAUTH_TOKEN = 'IB2EOL5QIAIUA1FUMNFKYWOSKIFAZ4MK0ZVHD0CDDDER2ANT&v=20130409'
CATEGORY_PUB = '4bf58dd8d48988d11b941735'
CATEGORY_GASTRO = '4bf58dd8d48988d155941735'
CATEGORY_GAY = '4bf58dd8d48988d1d8941735'
CATEGORY_COCKTAIL = '4bf58dd8d48988d118941735'
CATEGORY_DIVE = '4bf58dd8d48988d118941735'
CATEGORY_KARAOKE = '4bf58dd8d48988d120941735'
CATEGORY_BEER_GARDEN = '4bf58dd8d48988d117941735'
CATEGORY_BAR = '4bf58dd8d48988d116941735'
CATEGORY_SPORTS = '4bf58dd8d48988d11d941735'
CATEGORY_STRIP = '4bf58dd8d48988d1d6941735'
CATEGORY_WINE = '4bf58dd8d48988d123941735'
CATEGORY_WHISKY = '4bf58dd8d48988d122941735'

def find_pubs(pub_type='pub'):
    pub_type = pub_type.lower()
    if pub_type == 'pub':
        category = CATEGORY_PUB
    elif pub_type == 'gastro':
        category = CATEGORY_GASTRO
    elif pub_type == 'gay':
        category = CATEGORY_GAY
    elif pub_type == 'cocktail':
        category = CATEGORY_COCKTAIL
    elif pub_type == 'dive':
        category = CATEGORY_DIVE
    elif pub_type == 'karaoke':
        category = CATEGORY_KARAOKE
    elif pub_type == 'beer garden':
        category = CATEGORY_BEER_GARDEN
    elif pub_type == 'bar':
        category = CATEGORY_BAR
    elif pub_type == 'sports':
        category = CATEGORY_SPORTS
    elif pub_type == 'strip':
        category = CATEGORY_STRIP
    elif pub_type == 'wine':
        category = CATEGORY_WINE
    elif pub_type == 'whiskey':
        category = CATEGORY_WHISKY

    ret_dict = {}
    for station in stations.stations:
        print '{0} {1} {2}'.format(station['name'], station['lat'], station['lng'])
        station_name = station['name'].lower()
        the_url = build_query(station['lat'], station['lng'], 500, category)
        opener = urllib2.build_opener()
        f = opener.open(the_url)
        response = simplejson.load(f)

        best_ratio = .011
        pub_results = response['response']
        best_dict = {}
        best_dict['name'] = ''
        best_dict['rating'] = None
        best_dict['correct_type'] = False
        for venue in pub_results['venues']:
        	if 'stats' in venue:
	            user_count = venue['stats']['usersCount']
	            checkin_count = venue['stats']['usersCount']
	            if user_count == 0:
	            	continue
	            if checkin_count == 0:
	            	continue
	            ratio = checkin_count / user_count
	            if ratio > best_ratio:
	            	val = int(best_ratio * 10.0)
	            	if (val % 10) >= 5:
	            	    val += 10
	            	val /= 5
	            	if val > 5:
	            		val = 5
                    if val < 1:
                    	val = 1
	                best_dict = {}
	                best_dict['name'] = venue['name']
	                best_dict['rating'] = val
	                best_dict['correct_type'] = True

        ret_dict[station_name] = best_dict

    return ret_dict
        # f = urllib.urlopen(the_url)
        # raw_json = f.read()
        # pub_results = simplejson.loads('[%s]' % raw_json[:-1])
        # print pub_results['venues']
        # print pub_results



def build_query(lat, lng, radius, category):
    url_str = 'https://api.foursquare.com/v2/venues/search?'
    url_str += 'll={0},{1}'.format(lat, lng)
    url_str += '&radius={0}'.format(radius)
    url_str += '&categoryId={0}'.format(category)
    url_str += '&intent=browse'
    url_str += '&limit=50'

    url_str += '&oauth_token={0}'.format(OAUTH_TOKEN)

    return url_str


# https://api.foursquare.com/v2/venues/search?ll=40.7,-74&callback=location&
# oauth_token=IB2EOL5QIAIUA1FUMNFKYWOSKIFAZ4MK0ZVHD0CDDDER2ANT&v=20130409
