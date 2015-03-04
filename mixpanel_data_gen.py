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


users = 100
event_max = 150
from_date = datetime.datetime.today() - datetime.timedelta(days=60)
to_date = datetime.datetime.today()

api_key = "f2d9bb9390fd2ca6435b7518949ac1dd"
api_secret = "77c474a1b8d6f2909ad4d07af8cf504a"
token = "7ed1660dcb607670ac10f96d863d5e59"

errors = 0
people = 0
events = 0

def random_date(start, end):
	delta = end - start
	int_delta = (delta.days * 24 * 60 * 60 + delta.seconds)
	random_second = random.randrange(int_delta)
	return start + datetime.timedelta(seconds=random_second)

def api_request(data, params, endpoint):
	data_encoded = b64encode(data)
	params["data"] = data_encoded
	parameters = urllib.urlencode(params)
	# print endpoint + parameters
	request = urllib.urlopen(endpoint + parameters)
	if request.read() == 0:
		errors += 1
		print request.read()


######## Create event with properties #########

class Event(object):

	def __init__(self, event, props, super_props):
		self.event = event
		self.props = props
		self.super_props = super_props
		self.new_props = self.props[:-1] + ", " + self.super_props[1:]

		endpoint = "http://api.mixpanel.com/import/?"
		data = '{"event": "' + event + '", "properties": ' + str(self.new_props) + '}'
		params = {"api_key": api_key}

		api_request(data, params, endpoint)

######### Create people profile #########

class Person(object):

	def __init__(self):
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

		props["Search Engine"] = ["Google", "Bing", "Yahoo",]
		props["Referrer"] = ["$direct", "github.com", "news.ycombinator.com", "stackoverflow.com", "t.co", "thenextweb.com", "bing.com", "mail.google.com", "facebook.com", "google.com", "twitter.com", "techcrunch.com", "venturebeat.com",]
		props["utm_medium"] = ["Referral", "docs", "email", "twitter",]
		props["utm_source"] = ["Buffer", "Facebook", "Partner", "Dev Weekly",]
		for prop, value in props.iteritems():
			val = random.choice(value)
			super_props[prop] = val

		locations = {"San Francisco":"United States", "Los Angeles":"United States", "San Diego":"United States", "New York":"United States", "Chicago":"United States", "Scottsdale":"United States", "Seattle":"United States", "Dallas":"United States", "Philadelphia":"United States", "Orlando":"United States", "Portland":"United States", "Mexico City":"Mexico", "Cancun":"Mexico", "Rio de Janiero":"Brazil", "Barcelona":"Spain", "Madrid":"Spain", "Sevilla":"Spain", "Beijing":"China", "Shanghai":"China", "Tokyo":"Japan", "London":"UK", "Dublin":"Ireland", "Berlin":"Germany", "Munich":"Germany", "Rome":"Italy", "Florence":"Italy", "Venice":"Italy", "Milan":"Italy", "Paris":"France", "Seoul":"South Korea", "Capetown":"South Africa"}
		super_props["City"] = random.choice(locations.keys())
		super_props["Country"] = locations[super_props["City"]]

		devices = {"Android": ["Android Mobile", "Chrome"], "Blackberry": ["Blackberry"], "Windows Phone": ["Internet Explorer"], "iPad": ["Mobile Safari", "Chrome iOS", "Mozilla"], "iPhone": ["Mobile Safari", "Chrome iOS"], "iPod Touch": ["Mobile Safari"]}
		super_props["Device"] = random.choice(devices.keys())
		super_props["Browser"] =  random.choice(devices[super_props["Device"]])

		super_props["Gender"] = self.gender
		super_props["$first_name"] = self.firstname
		super_props["$last_name"] = self.lastname
		super_props["$email"] = self.email
		super_props["$phone"] = self.phone

		self.super_properties = "mixpanel.register(" + str(super_props)[1:-1] + ")"
		self.properties = json.dumps(super_props)

	def people_profile(self):
		data = '{"$token": "' + token + '", "$distinct_id": "' + self.distinct_id + '", "$set": ' + str(self.properties) + '}'
		params = {}
		endpoint = "http://api.mixpanel.com/engage/?"

		api_request(data, params, endpoint)
		
	def add_events(self, max):
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

		self.first_view_date = random_date(from_date, to_date)
		self.signup_date = random_date(self.first_view_date, to_date)

		Event(event="View Page", props=json.dumps({"Page": "Landing", "Source": random.choice(event_list["View Page"]["Source"]), "distinct_id": self.distinct_id, "token": token, "time": int(self.first_view_date.strftime("%s"))}), super_props=self.properties)

		weight = random.randint(1, 10)
		if weight <= 4:
			Event(event="$signup", props=json.dumps({"distinct_id": self.distinct_id, "token": token, "time": int(self.signup_date.strftime("%s"))}), super_props=self.properties)

		for i in range(max):
			track = random.choice(event_list.keys())
			event_date = random_date(self.signup_date, to_date)
			event_props = {"distinct_id": self.distinct_id, "token": token, "time": int(event_date.strftime("%s"))}

			for prop, prop_name in event_list[track].iteritems():
				event_props[prop] = random.choice(prop_name)

			event_props = json.dumps(event_props)
			Event(event=track, props=event_props, super_props=self.properties)


print "Running...."

for i in range(users):
	new_person = Person()
	new_person.people_profile()
	people += 1

	num_events = random.randint(0, event_max)
	new_person.add_events(num_events)
	events += num_events
	print "People: " + str(people) + ", Events: " + str(events) + ", Errors: " + str(errors)
