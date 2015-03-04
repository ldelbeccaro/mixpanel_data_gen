#! /usr/bin/env python
#
# Mixpanel, Inc. -- http://mixpanel.com/
#
# Python API client library to write mixpanel.com analytics data.

from base64 import b64encode
from calendar import timegm
import urllib
import datetime
import random
import uuid
try:
    import json
except ImportError:
    import simplejson as json


users = 10
events = 15
from_date = datetime.datetime.today() - datetime.timedelta(days=36)
to_date = datetime.datetime.today() - datetime.timedelta(days=6)
api_key = "f2d9bb9390fd2ca6435b7518949ac1dd"
api_secret = "77c474a1b8d6f2909ad4d07af8cf504a"
token = "7ed1660dcb607670ac10f96d863d5e59"


def random_date(start, end):
	delta = end - start
	int_delta = (delta.days * 24 * 60 * 60 + delta.seconds)
	random_second = random.randrange(int_delta)
	return start + datetime.timedelta(seconds=random_second)

# def api_request(data, params, endpoint):
# 	data_encoded = b64encode(data)
# 	params["data"] = data_encoded
# 	parameters = urllib.urlencode(params)
# 	request = urllib.urlopen(endpoint + parameters)


######## Create event with properties #########

class Event(object):

	def __init__(self, event, props):
		self.event = event
		self.props = props

		endpoint = "http://api.mixpanel.com/import/?"

		data = '{"event": "' + event + '", "properties": ' + str(self.props) + '}'


		data_encoded = b64encode(data)

		params = urllib.urlencode({"data": data_encoded, "api_key": api_key})
		f = urllib.urlopen(endpoint + params)

######### Create people profile #########

class Person(object):

	def __init__(self, count):
		self.count = count

		genders = ["Female", "Male",]
		female_firstnames = ["Chloe", "Emily", "Emma", "Olivia", "Jennifer", "Beckie", "Laura", "Brenda", "Danielle", "Ellen", "Sarah", "Hannah", "Lola", "Jessica", "Lily", "Savannah", "Isabella", "Rebecca", "Charlotte", "Ella", "Elizabeth", "Mia", "Abigail", "Zoe", "Lauren", "Grace", "Sophia", "Sam", "Samantha", "Rachel", "Natalie", "Lexi", "Paige", "Alice", "Amanda", "Alyssa", "Lucy", "Vanessa",]
		male_firstnames = ["Michael", "Jacob", "Bryan", "Brian", "Shawn", "Aaron", "Muhammad", "Daniel", "Jonah", "Liam", "Ryan", "Ali", "James", "Ethan", "Harry", "David", "Kyle", "Will", "Alex", "Luke", "Matt", "Matthew", "Mike", "Joe", "Joseph", "Adam", "Jack", "Tyler", "Kevin", "Austin", "Aiden", "Anthony", "Jackson", "Blake", "Max", "Brandon", "Brendan", "Chris", "Nathan", "Spencer", "Jordan",]
		lastnames = ["Smith", "Brown", "Ahmed", "Chakma", "Hasan", "Islam", "Wang" "Li", "Zhu", "Lin", "Kumar", "Das", "Cohen", "Suzuki", "Kim", "Johnson", "Williams", "Garcia", "Rodriguez", "Martinez", "Lopez", "White", "Gorman", "Moss", "Robinson", "Scott", "King", "Davis", "Lee", "Green", "Evans", "Reed", "Brooks", "Ross", "Long", "Cole", "West", "Kennedy", "Tucker", "Washington", "Armstrong",]
		email_domains = ["gmail.com", "hotmail.com", "yahoo.com", "aol.com", "google.com", "facebook.com", "comcast.net", "att.net", "gmx.com", "verizon.net", "ymail.com", "rocketmail.com", "email.com", "mail.com", "mac.com", "me.com", "hotmail.co.uk", "msn.com", "sbcglobal.net", "live.com", "inbox.com", "qq.com", "yahoo.fr", "hotmail.de", "rambler.ru",]

		self.gender = (random.choice(genders))
		if self.gender == "Female":
			self.firstname = (random.choice(female_firstnames))
		elif self.gender == "Male":
			self.firstname = (random.choice(male_firstnames))
		self.lastname = (random.choice(lastnames))
		self.email = self.firstname[0].lower() + self.lastname.lower() + "@" + (random.choice(email_domains))
		self.phone = random.randint(1000000000, 9999999999)
		self.distinct_id = uuid.uuid4().hex
		
		props = {}
		super_props = {}

		props["Browser"] = ["Chrome", "Safari", "Firefox", "Opera", "Android Mobile", "BlackBerry", "Chrome iOS", "Internet Explorer", "Mobile Safari", "Mozilla",]
		props["Search Engine"] = ["Google", "Bing", "Yahoo",]
		props["Referrer"] = ["$direct", "github.com", "news.ycombinator.com", "stackoverflow.com", "t.co", "thenextweb.com", "bing.com", "mail.google.com", "facebook.com", "google.com", "twitter.com", "techcrunch.com", "venturebeat.com",]
		props["Device"] = ["Android", "BlackBerry", "Windows Phone", "iPad", "iPhone", "iPod Touch",]
		props["utm_medium"] = ["Referral", "docs", "email", "twitter",]
		props["utm_source"] = ["Buffer", "Facebook", "Partner", "Dev Weekly",]
		for prop, value in props.iteritems():
			val = random.choice(value)
			super_props[prop] = val

		locations = {"San Francisco":"United States", "Los Angeles":"United States", "San Diego":"United States", "New York":"United States", "Chicago":"United States", "Scottsdale":"United States", "Seattle":"United States", "Dallas":"United States", "Philadelphia":"United States", "Orlando":"United States", "Portland":"United States", "Mexico City":"Mexico", "Cancun":"Mexico", "Rio de Janiero":"Brazil", "Barcelona":"Spain", "Madrid":"Spain", "Sevilla":"Spain", "Beijing":"China", "Shanghai":"China", "Tokyo":"Japan", "London":"UK", "Dublin":"Ireland", "Berlin":"Germany", "Munich":"Germany", "Rome":"Italy", "Florence":"Italy", "Venice":"Italy", "Milan":"Italy", "Paris":"France", "Seoul":"South Korea", "Capetown":"South Africa"}
		super_props["City"] = (random.choice(locations.keys()))
		super_props["Country"] = locations[super_props["City"]]

		super_props["Gender"] = self.gender
		super_props["$first_name"] = self.firstname
		super_props["$last_name"] = self.lastname
		super_props["$email"] = self.email
		super_props["$phone"] = self.phone

		self.super_properties = "mixpanel.register(" + str(super_props)[1:-1] + ")"
		self.people_properties = super_props

	def people_profile(self):
		data = '{"$token": "' + token + '", "$distinct_id": ' + self.distinct_id + '", "$set": "' + str(self.people_properties) + '}'
		
	def add_events(self):
		event_list = {
			"View Page": {
				"Page": ["Pricing", "Tour", "Contact",], 
				"Source": ["Internal", "Facebook", "Techcrunch",],
			},
			"Do Something": {
				"Property": ["Value",],
			},
			"Something Else": {
				"Prop1": ["Val1",],
				"Prop2": ["Val2",],
			},
		}

		self.first_event_date = from_date

		for i in range(random.randint(0, events)):

			print 'Person ' + str(self.count+1) + ', Event ' + str(i+1)

			track = random.choice(event_list.keys())
			event_date = random_date(from_date, to_date)
			event_props = {"distinct_id": self.distinct_id, "token": token, "time": int(event_date.strftime("%s"))}

			for prop, prop_name in event_list[track].iteritems():
				event_props[prop] = random.choice(prop_name)

			event_props = json.dumps(event_props)
			Event(event=track, props=event_props)

			if i == 0:
				self.first_event_date = event_date
			elif self.first_event_date > event_date:
				self.first_event_date = event_date

		self.first_view_date = random_date(from_date - datetime.timedelta(days=5), self.first_event_date)
		Event(event="View Page", props=json.dumps({"Page": "Landing", "Source": random.choice(event_list["View Page"]["Source"]), "distinct_id": self.distinct_id, "token": token, "time": int(self.first_event_date.strftime("%s"))}))

		weight = random.randint(1, 10)
		if weight <= 4:
			signup_date = random_date(self.first_view_date, self.first_event_date).strftime("%s")
			Event(event="$signup", props=json.dumps({"distinct_id": self.distinct_id, "token": token, "time": int(signup_date)}))

for i in range(users):
	new_person = Person(i)
	# new_person.people_profile()
	new_person.add_events()




















