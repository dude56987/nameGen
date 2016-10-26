#! /usr/bin/python
########################################################################
# Generates a random username using word lists
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
from random import randrange
from sys import argv
from sys import stdout
############################################################################
class nameGen():
	'''
	nameGen is designed to read two files, one with an adjectives and
	one with a nouns, combine the two and generate a username.
	'''
	def __init__(self):
		# store file contents in a dict for faster access
		self.fileCache = dict()
	def pullConfig(self, filePath):
		'''
		Open a config file, strip line endings and whitespace.
		Return a list of all the lines.
		'''
		if filePath not in self.fileCache.keys():
			fileObject=open(filePath,'r')
			lineArray=[]
			for line in fileObject:
				# remove line endings and spaces
				line = line.replace(' ','')
				line = line.strip()
				lineArray.append(line)
			# store the processed file in the file cache
			self.fileCache[filePath] = lineArray
		# return the stored file array
		return self.fileCache[filePath]
	############################################################################
	def showHelp(self):
		'''
		Print the help on the screen.
		'''
		helpInfo = "#"*80+"\n"
		helpInfo+= "NameGen"+"\n"
		helpInfo+= "#"*80+"\n"
		helpInfo+= "--help"+"\n"
		helpInfo+= "    Displays this message."+"\n"
		helpInfo+= "--stats"+"\n"
		helpInfo+= "    Run test run to see how generated names might be duplicated."+"\n"
		helpInfo+= "    You can use a number after this argument in order to set the "+"\n"
		helpInfo+= "    amount of tests to run for statistics."+"\n"
		helpInfo+= "--no-number"+"\n"
		helpInfo+= "    Do not generate numbers at the end."+"\n"
		helpInfo+= "--hide-output"+"\n"
		helpInfo+= "    Disable output of generated name to standard output."+"\n"
		helpInfo+= "#"*80+"\n"
		helpInfo+= "Below is the default output."+"\n"
		helpInfo+= "#"*80
		print helpInfo
	############################################################################
	def main(self, arguments):
		'''
		Generate a random username.
		'''
		if "--stats" in arguments:
			# load up the config files
			adj = self.pullConfig("adj.conf")
			noun = self.pullConfig("noun.conf")
			# set the number of times to run the test in order to
			# generate statistics
			testNames = 50000
			# check for number arguments on the end of stats
			if len(arguments) > arguments.index('--stats')+1:
				tempTestNames = arguments[arguments.index('--stats')+1]
				if ('-' not in tempTestNames) and ('/' not in tempTestNames):
					testNames = int(tempTestNames)
			# create a dict to store the statistics
			stats = dict()
			# print out the probable names available
			print(str(len(adj)*len(noun))+' possible name combinations')
			# modify arguments for running stats
			arguments.remove('--stats')
			arguments.append('--hide-output')
			for index in range(testNames):
				stdout.write('Running test '+str(index)+' out of '+str(testNames)+'\r')
				# call the main program
				tempName = self.main(arguments)
				if tempName in stats.keys():
					stats[tempName] += 1
				else:
					stats[tempName] = 1
			# sort the list of stat keys
			sortedStatsList = sorted(stats, key=stats.get)
			# print the sorted list of stat keys
			for key in sortedStatsList:
				print(str(key)+' found '+str(stats[key])+' times')
		else:
			# check for help in arguments
			if "--help" in arguments:
				self.showHelp()
			# load config files
			adj = self.pullConfig("adj.conf")
			noun = self.pullConfig("noun.conf")
			# randomly pick a line from each config file
			adjIndex = randrange(0,len(adj))
			nounIndex = randrange(0,len(noun))
			# check if numbers have been disabled
			if "--no-number" in arguments:
				# dont gen a number if --no-number is called
				number = ''
			else:
				number = str(randrange(0,9999))
			# store the generated name in a variable
			generatedName = (adj[adjIndex]+noun[nounIndex]+number)
			# print the name to stdout and return the generated name value
			if '--hide-output' not in arguments:
				print generatedName
			return generatedName
############################################################################
# Execute the program
nameGen().main(argv)
