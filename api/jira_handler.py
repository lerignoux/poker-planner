import logging
import requests

log = logging.getLogger(__name__)

class JiraHandler():
	def __init__(self, url):
		self.url = url

	def get_stories(self, jql, username, password):
		requests.get()
		return []