from hashlib import md5
from bs4 import BeautifulSoup
from eload.models import products
import urllib.parse
import requests

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
