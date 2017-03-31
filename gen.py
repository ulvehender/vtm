#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import logging
import re

_LATEX_SUBS = (
	(re.compile(r'\\'), r'\\textbackslash'),
	(re.compile(r'_'), r'\\textunderscore '),
	(re.compile(r'([{}_#%&$])'), r'\\\1'),
	(re.compile(r'~'), r'\~{}'),
	(re.compile(r'\^'), r'\^{}'),
	(re.compile(r'"'), r"''"),
	(re.compile(r'\.\.\.+'), r'\\ldots'),
)
_log = logging.getLogger(__name__)

# return a latex compatible jinja2 syntax
# basically replace { } by ()
def getEnv():
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
	env.block_start_string  = '((*'
	env.block_end_string = '*))'
	env.variable_start_string  = '((('
	env.variable_end_string = ')))'
	env.comment_start_string  = '((='
	env.comment_end_string = '=))'
	env.filters['tex'] = escape_tex
	env.filters['vars'] = vars
	return env

def escape_tex(value):
	"""Escape Tex special character in the given value."""
	if not value: # handles properly '' and None
		return ''
	newval = str(value)
	for pattern, replacement in _LATEX_SUBS:
		newval = pattern.sub(replacement, newval)
	return newval

class Player(object):
	def __init__(self, name):
		self.name = None

	@property
	def attributes(self):
		return [attr for attr in self._attributes] # a copy

	@property
	def data(self):
		return {'attributes': [(attr[:3], attr.capitalize()) for attr in self.attributes]}

def attribute(attr):
	def decorator(cls):
		cls._attributes.append(attr)
		return cls
	return decorator

@attribute('strength')
@attribute('dexterity')
@attribute('stamina')
@attribute('manipulation')
@attribute('appearance')
@attribute('charisma')
@attribute('perception')
@attribute('intelligence')
@attribute('wits')
class Vampire(Player):
	_attributes = []


if __name__=='__main__':
	env=getEnv()
	rpg = env.get_template('rpg.template')
	semi = Vampire(u'Semi')
	with open('rpg.sty', 'w') as f:
		f.write(rpg.render(**semi.data))

