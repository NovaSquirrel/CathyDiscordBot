# Based on https://github.com/subalterngames/Not_Constantinople
# Copyright 2018 Subaltern Games, LLC

from os import getcwd, listdir, mkdir
from os.path import isdir
from json import loads
import io
import markovify
import random

# Returns all provinces and their settlements with a given culture.
def get_culture(culture):
    with io.open(getcwd() + "/provinces.json", mode='rt', encoding="utf-8") as f:
        provinces = loads(f.read())
        c_p = dict()
        for key in provinces.keys():
            if provinces[key]["culture"] == culture:
                c_p.update({key: provinces[key]})
        return c_p

# Returns all provinces with a given culture.
def get_provinces(culture):
    provinces = []
    for key in culture.keys():
        p = get_culture(key).keys()
        for i in range(culture[key]):
            provinces.extend(p)
    return provinces

# Returns all settlements with a given culture.
def get_settlements(culture):
    settlements = []
    for key in culture.keys():
        s = get_culture(key)
        for k in s.keys():
            for i in range(culture[key]):
                settlements.extend(s[k]["settlements"])
    return settlements

# Turns lines into sentences that markovify can parse.
def get_text_model(lines):
    for i in range(len(lines)):
        line = ""
        for j in range(len(lines[i])):
            line += lines[i][j]
            if j < len(lines[i]) - 1:
                line += " "
            else:
                line += "."
        lines[i] = line
    text_model = markovify.Text(lines, state_size=2)
    return text_model

# Returns a scrambled markovified word.
def markov(text_model):
    sentence = None
    count = 0
    while sentence == None and count < 10:
        sentence = text_model.make_sentence()
        count += 1
    if sentence == None:
        return None, False
    else:
        # Turn the sentence into a word
        return sentence.replace(" ", "").replace(".", "").title(), True

"""
# Generate gibberish.
def generate(filename, filename_suffix, dataset):
    text_model = get_text_model(dataset)
    added = set()
    generated = []
    for i in range(500):
        item, real = markov(text_model)
        if real and item not in added:
            generated.append(item + "\n")
            added.update({item})
    directory = getcwd() + "/Output"
    if not isdir(directory):
        mkdir(directory)
    with io.open(directory + "/" + filename + "_" + filename_suffix + ".txt", mode="wt", encoding="utf-8") as f:
        f.writelines(generated)

# Load the stored cultural blends and generate some names.
for f in listdir(getcwd() + "/Input"):
    with io.open(getcwd() + "/Input/" + f, mode="rt", encoding="utf-8") as j:
        # Get the saved cultural blend.
        json_culture = loads(j.read())
        # Generate names of provinces and settlements.
        generate(json_culture["name"], "provinces", get_provinces(json_culture["culture"]))
        generate(json_culture["name"], "settlements", get_settlements(json_culture["culture"]))
"""

def generate(dataset, count):
    text_model = get_text_model(dataset)
    added = set()
    generated = []
    for i in range(count):
        item, real = markov(text_model)
        if real and item not in added:
            generated.append(item)
            added.update({item})
    return ', '.join(generated)

all_cultures = ['pommeranian', 'manden', 'greek', 'khazar', 'serbian', 'persian', 'saka', 'assamese', 'alan', 'norse'
'polish', 'sindhi', 'hindustani', 'egyptian_arabic',
'telugu', 'northern_sami', 'karluk', 'sumpa', 'occitan', 'bohemian',
'hungarian', 'komi', 'welsh', 'assyrian', 'khanty', 'sinhala',
'avar', 'gujurati', 'breton', 'croatian', 'old_saxon', 'romanian', 'georgian', 'cuman', 'ethiopian', 'bulgarian',
'baloch', 'german', 'tocharian', 'kannada', 'lombard', 'maghreb_arabic',
'turkish', 'nepali', 'bengali', 'panjabi', 'tangut', 'irish',
'ugricbaltic', 'marathi', 'basque', 'suebi', 'pictish', 'bolghar', 'lithuanian', 'visigothic', 'kirghiz', 'severian', 'lettigallish',
'nubian', 'bedouin_arabic', 'oriya', 'levantine_arabic',
'samoyed', 'ilmenian', 'mordvin', 'tamil', 'italian', 'afghan', 'sogdian', 'zhangzhung', 'prussian', 'pecheneg',
'saxon', 'han', 'old_frankish', 'bodpa', 'finnish', 'volhynian', 'frisian', 'somali', 'kurdish', 'armenian', 'uyghur', 'rajput']

to_generate = 25

def parse_weights(s):
	global to_generate
	to_generate = 25

	weights = {}
	if len(s) == 0:
		for culture in random.sample(all_cultures, random.randint(3, 10)):
			weights[culture] = random.randint(1, 15)
		print("Using " + str(weights))
		return weights
	s = [x.split('=') for x in s.split(' ')]
	if len(s) > 1 and len(s[0]) == 1 and s[0][0].isnumeric():
		to_generate = int(s[0][0])
		if to_generate < 0:
			to_generate = 1
		if to_generate > 50:
			to_generate = 50
	for pair in s:
		if len(pair) == 2:
			weights[pair[0].lower()] = int(pair[1])
	return weights

#HELP_STRING = 'Give input as culture1=weight culture2=weight, etc. using the culture list from <https://github.com/subalterngames/Not_Constantinople>'

def generate_provinces(weight_string):
	return generate(get_provinces(parse_weights(weight_string)), to_generate)

def generate_settlements(weight_string):
	return generate(get_settlements(parse_weights(weight_string)), to_generate)
