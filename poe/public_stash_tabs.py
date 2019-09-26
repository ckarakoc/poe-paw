import json
import requests
import poe.base as poe
from itertools import islice


class PST(object):
	def __init__(self, id=0):
		curr = requests.get(f'{poe.base}public-stash-tabs', params={'id': id}).json()
		self.next_change_stack = [curr['next_change_id']]
		self.stashes = curr['stashes']
		self._stash_idx = 0

	def head(self, n=5):
		"""
		Get the first n elements of the list as an iterator.
		:param n:
		:return:
		"""
		if len(self.stashes) < n:
			raise ValueError(f'The list has length: {len(self.stashes)}.')
		return islice(self.stashes, None, n, 1)

	def tail(self, n=5):
		"""
		Get the last n elements of the list as an iterator.
		:param n:
		:return:
		"""
		if len(self.stashes) < n:
			raise ValueError(f'The list has length: {len(self.stashes)}.')
		return islice(self.stashes, len(self.stashes) - n, None, 1)

	def stashes(self, as_json=False):
		"""
		Generator of the stashes on the current page.
		:param as_json:
		:return:
		"""
		for stash in self.stashes:
			yield stash if as_json else Stash(stash)

	def next_page(self):
		next_page = requests.get(f"{poe.base}public-stash-tabs", params={'id': self.next_change_stack[-1]}).json()
		self.stashes = next_page['stashes']
		self.next_change_stack.append(next_page['next_change_id'])

	def prev_page(self):
		self.next_change_stack.pop()
		prev_page = requests.get(f"{poe.base}public-stash-tabs", params={'id': self.next_change_stack[-1]}).json()
		self.stashes = prev_page['stashes']


class Stash(object):
	def __init__(self, stash_json):
		self.id = stash_json['id']
		self.public = stash_json['public']
		self.account_name = stash_json['accountName']
		self.last_character_name = stash_json['lastCharacterName']
		self.stash = stash_json['stash']
		self.stash_type = stash_json['stashType']
		self.league = stash_json['league']
		self.items = stash_json['items']

	def items(self, as_json=False):
		for item in self.items:
			yield item if as_json else Item(item)


class Item(object):
	def __init__(self, item_json):
		# todo
		pass
