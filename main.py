from pulsar import provider
from urllib import unquote_plus
import re

# this read the settings
url = provider.ADDON.getSetting('url_address')
icon = provider.ADDON.getAddonInfo('icon')
name_provider = provider.ADDON.getAddonInfo('name') # gets name
extra = provider.ADDON.getSetting('extra')
key_allowed = provider.ADDON.getSetting('key_allowed')
key_denied = provider.ADDON.getSetting('key_denied')
max_magnets = int(provider.ADDON.getSetting('max_magnets'))  #max_magnets

#define quality variables
quality_allow = ['480p', 'DVD', 'HDTV', '720p','1080p', '3D' , 'WEB', 'Bluray', 'BRRip', 'HDRip', 'MicroHD', 'x264', 'AC3', 'AAC', 'HEVC', 'CAM'] + re.split('\s',key_allowed)
quality_deny = re.split('\s',key_denied)

#quality_movie
movie_q1 = provider.ADDON.getSetting('movie_q1') #480p
movie_q2 = provider.ADDON.getSetting('movie_q2') #DVD
movie_q3 = provider.ADDON.getSetting('movie_q3') #HDTV
movie_q4 = provider.ADDON.getSetting('movie_q4') #720p
movie_q5 = provider.ADDON.getSetting('movie_q5') #1080p
movie_q6 = provider.ADDON.getSetting('movie_q6') #3D
movie_q7 = provider.ADDON.getSetting('movie_q7') #WEB
movie_q8 = provider.ADDON.getSetting('movie_q8') #Bluray
movie_q9 = provider.ADDON.getSetting('movie_q9') #BRRip
movie_q10 = provider.ADDON.getSetting('movie_q10') #HDRip
movie_q11 = provider.ADDON.getSetting('movie_q11') #MicroHD
movie_q12 = provider.ADDON.getSetting('movie_q12') #x264
movie_q13 = provider.ADDON.getSetting('movie_q13') #AC3
movie_q14 = provider.ADDON.getSetting('movie_q14') #AAC
movie_q15 = provider.ADDON.getSetting('movie_q15') #HEVC
movie_q16 = provider.ADDON.getSetting('movie_q16') #CAM
movie_allow = re.split('\s',key_allowed)
movie_deny = re.split('\s',key_denied) 
movie_allow.append('480p') if movie_q1 == 'true' else movie_deny.append('480p')
movie_allow.append('DVD') if movie_q2 == 'true' else movie_deny.append('DVD')
movie_allow.append('HDTV') if movie_q3 == 'true' else movie_deny.append('HDTV')
movie_allow.append('720p') if movie_q4 == 'true' else movie_deny.append('720p')
if movie_q5 == 'true': 
	movie_allow.append('1080p')  
else: 
	if movie_q6 == 'false': movie_deny.append('1080p') 
movie_allow.append('3D') if movie_q6 == 'true' else movie_deny.append('3D')
movie_allow.append('WEB') if movie_q7 == 'true' else movie_deny.append('WEB')
movie_allow.append('Bluray') if movie_q8 == 'true' else movie_deny.append('Bluray')
movie_allow.append('BRRip') if movie_q9 == 'true' else movie_deny.append('BRRip')
movie_allow.append('HDRip') if movie_q10 == 'true' else movie_deny.append('HDRip')
movie_allow.append('MicroHD') if movie_q11 == 'true' else movie_deny.append('MicroHD')
movie_allow.append('x264') if movie_q12 == 'true' else movie_deny.append('x264')
movie_allow.append('AC3') if movie_q13 == 'true' else movie_deny.append('AC3')
movie_allow.append('AAC') if movie_q14 == 'true' else movie_deny.append('AAC')
movie_allow.append('HEVC') if movie_q15 == 'true' else movie_deny.append('HEVC')
movie_allow.append('CAM') if movie_q16 == 'true' else movie_deny.append('CAM')

#quality_TV
TV_q1 = provider.ADDON.getSetting('TV_q1') #480p
TV_q2 = provider.ADDON.getSetting('TV_q2') #DVD
TV_q3 = provider.ADDON.getSetting('TV_q3') #HDTV
TV_q4 = provider.ADDON.getSetting('TV_q4') #720p
TV_q5 = provider.ADDON.getSetting('TV_q5') #1080p
TV_q7 = provider.ADDON.getSetting('TV_q7') #WEB
TV_q8 = provider.ADDON.getSetting('TV_q8') #Bluray
TV_q9 = provider.ADDON.getSetting('TV_q9') #BRRip
TV_q10 = provider.ADDON.getSetting('TV_q10') #HDRip
TV_q12 = provider.ADDON.getSetting('TV_q12') #x264
TV_q15 = provider.ADDON.getSetting('TV_q15') #HEVC
TV_allow = re.split('\s',key_allowed)
TV_deny = re.split('\s',key_denied) 
TV_allow.append('480p') if TV_q1 == 'true' else TV_deny.append('480p')
TV_allow.append('DVD') if TV_q2 == 'true' else TV_deny.append('DVD')
TV_allow.append('HDTV') if TV_q3 == 'true' else TV_deny.append('HDTV')
TV_allow.append('720p') if TV_q4 == 'true' else TV_deny.append('720p')
TV_allow.append('1080p') if TV_q5 == 'true' else TV_deny.append('1080p')
TV_allow.append('WEB') if TV_q7 == 'true' else TV_deny.append('WEB')
TV_allow.append('Bluray') if TV_q8 == 'true' else TV_deny.append('Bluray')
TV_allow.append('BRRip') if TV_q9 == 'true' else TV_deny.append('BRRip')
TV_allow.append('HDRip') if TV_q10 == 'true' else TV_deny.append('HDRip')
TV_allow.append('x264') if TV_q12 == 'true' else TV_deny.append('x264')
TV_allow.append('HEVC') if TV_q15 == 'true' else TV_deny.append('HEVC')

# function to validate
def included(value, keys):
	res = False
	for item in keys:
		if item.upper() in value.upper():
			res = True 
			break
	return res

# clean_html
def clean_html(data):
	lines = re.findall('<!--(.*?)-->',data)
	for line in lines:
		data = data.replace(line,'')
	return data

# using function from Steeve to add Provider's name
def extract_magnets(data):
	try:
		data = clean_html(data)
		size = re.findall(', Size (.*?)B,', data) # list the size
		cont = 0
		for cm, magnet in enumerate(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)):
			name = re.search('dn=(.*?)&tr=',magnet).group(1) #find name in the magnet
			name = unquote_plus(name).replace('.',' ') + ' - ' + size[cm].replace('&nbsp;',' ') + 'B' + ' - ' + name_provider
			if included(name, quality_allow) and not included(name, quality_deny):
					yield {"name": name, "uri": magnet} #return le torrent
					cont+= 1
			if cont == max_magnets: #limit magnets
				break
		provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
	except:
		provider.log.info('>>>>>>>ERROR parsing data<<<<<<<')


def search(info):
	query = info['query'] + extra
	provider.notify(message = 'Searching: ' + query.upper() + '...', header = None, time = 1500, image = icon)
	response = provider.GET("%s/search/%s/0/7/200" % (url,query.replace(' ','%20')))
	return extract_magnets(response.data)

def search_movie(info):
	global quality_allow, quality_deny
	quality_allow = movie_allow
	quality_deny = movie_deny
	query = '"' + info['title'] + '" ' + str(info['year']) #define query
	return search({'query': query})

def search_episode(info):
	global quality_allow, quality_deny
	quality_allow = TV_allow
	quality_deny = TV_deny
	query = '"' + info['title'] + '" S%02dE%02d '% (info['season'],info['episode'])  #define query
	return search({'query': query})

# This registers your module for use
provider.register(search, search_movie, search_episode)