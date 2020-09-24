from hashlib import md5
from bs4 import BeautifulSoup
from eload.models import products
import urllib.parse
import requests

# {'uid': '639234332224', 'auth': '24708c5f2898ed8b75d36da4e19c753c', 'pcode': 'ZTEST1', 'to': '09060583920', 'rrn': 'CLY2647004542'}
# https://loadcentral.net/sellapi.do?uid=639234332224&auth=24708c5f2898ed8b75d36da4e19c753c&pcode=ZTEST1&to=09060583920&rrn=CLY2647004542

# <RRN>CLY2647004542</RRN><RESP>0</RESP><TID>WB2871388051</TID><BAL>12.5725</BAL><EPIN>PIN1 124601 PIN2 655466</EPIN><ERR>Success</ERR>

# {'uid': '639234332224', 'auth': '24708c5f2898ed8b75d36da4e19c753c', 'rrn': 'CLY2647004542'}
# https://loadcentral.net/sellapiinq.do?uid=639234332224&auth=24708c5f2898ed8b75d36da4e19c753c&rrn=CLY2647004542

# <RRN>CLY2647004542</RRN><RESP>0</RESP><EBAL>12.5725</EBAL><TID>47666467</TID><RET>0</RET><REF>WB2871388051</REF><EPIN>PIN1 124601 PIN2 655466</EPIN><ERR>Success</ERR>


class LoadCentral():
	def __init__(self, uid, password, host = 'https://loadcentral.net/'):
		self.uid = uid
		self.password = password
		self.host = host

	def _request(self, options):
		endpoint  = options['url']
		method = options['method'] if options['method'] else 'GET'
		rrn = options['params']['rrn']
		auth = md5((md5(rrn.encode()).hexdigest() + md5((self.uid + self.password).encode()).hexdigest()).encode()).hexdigest()

		data = {
			'uid': self.uid,
			'auth': auth
		}
		url = self.host + endpoint

		if method == 'GET':
			response = requests.get(url, params={**data, **options['params']})

		if method == 'POST':
			response = requests.post(url, json = options['params'])

		return response.text

	def sell(self, params):
		return self._request({
			'url': 'sellapi.do',
			'method': 'GET',
			'params': params
			})

	def inquire(self, rrn):
		return self._request({
			'url': 'sellapiinq.do',
			'method': 'GET',
			'params': {
				'rrn': rrn
				}
			})

def update_product_list(url='http://loadcentral.com.ph/products'):
	s = requests.Session()
	response = s.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	table = soup.find('table', id='tablepress-66')
	data_list = table.find('tbody')

	entries = []

	for row in data_list.find_all('tr'):
		p_name = row.find('td', class_='column-1').get_text()
		p_code = row.find('td', class_='column-2').get_text()
		p_desc = row.find('td', class_='column-3').get_text()
		entries.append(
			products(product_code = p_code, product_name = p_name, product_description = p_desc)
		)
	try:
		products.objects.bulk_create(entries)
		return True
	except:
		return False
