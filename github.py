import requests

class Github(object):

	def __init__(self, user, repo, branch):
		self.url = 'https://raw.githubusercontent.com'
		self.user = user
		self.repo = repo
		self.branch = branch

	def download(self, path):
		"""
		Download raw file from github.
		"""
		return requests.get('{0}/{1}/{2}/{3}/{4}'.format(self.url, self.user, self.repo, self.branch, path))

	def save(self, path, text):
		"""
		Write text to the given file path.
		"""
		with open(path, 'w') as f:
			bytes = f.write(text)
		return len(bytes)

	def save_files(self, files):
		out = {}
		for f in files:
			out[f] =  save(f, download(f))
		return out