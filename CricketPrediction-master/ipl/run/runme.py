import sys
import os
import yaml
import random

ifile = "336024.yaml"


bat = open('../clusterInput/batCluster.tsv','r')
bowl = open('../clusterInput/bowlCluster.tsv','r')
i1_batsman_runs = dict()
i2_batsman_runs = dict()
dbat = {}
dbowl = {}

for i in bat.readlines():
	d = i.split(",")
	for i in d[1:]:
		dbat[i.strip()] = d[0]

for i in bowl.readlines():
	d = i.split(",")
	for i in d[1:]:
		dbowl[i.strip()] = d[0]
	

winner = ""

def predictRun(plist):
	r = random.random()
	tl = [sum(plist[:i]) for i in range(len(plist)+1)]
	tl = tl[1:]
	i = 0
	run = 0
	while r > tl[i] :
		if run == 4:
			run = run + 2
		else:
			run = run + 1
		i = i + 1
	return run



def play(innings):
	global count
	global trun
	global target
	global innings1
	global innings2
	batsman_runs = ""
	if(innings == innings1):
		batsman_runs = i1_batsman_runs
	else:
		batsman_runs = i2_batsman_runs

	global winner
	for row in innings:
		count = count + 1
		try:
			a = dbat[row[row.keys()[0]]['batsman']]
		except:
			a = 1
			print "nf:"+row[row.keys()[0]]['batsman']

		try:
			b = dbowl[row[row.keys()[0]]['bowler']]
		except:
			b = 1
			print "nf:"+row[row.keys()[0]]['bowler']

		f = open('iplclusters/'+str(a)+":"+str(b), 'r')

		a0 = 0
		a1 = 0
		a2 = 0
		a3 = 0
		a4 = 0
		a6 = 0

		tballs = 0

		for i in f:
			d = i.split(",")
			if d[3] == '1':
				a1 = a1 + 1
				tballs += 1	
			elif d[3] == '2':
				a2 = a2 + 1
				tballs += 1	
			elif d[3] == '3':
				a3 = a3 + 1
				tballs += 1	
			elif d[3] == '4':
				a4 = a4 + 1
				tballs += 1	
			elif d[3] == '6':
				a6 = a6 + 1
				tballs += 1	
			elif d[3] == '0':
				a0 = a0 + 1
				tballs += 1	
		

		p0 = float(a0)/tballs
		p1 = float(a1)/tballs
		p2 = float(a2)/tballs
		p3 = float(a3)/tballs
		p4 = float(a4)/tballs
		p6 = float(a6)/tballs



		p = predictRun([p0,p1,p2,p3,p4,p6])

		batsman_runs[row[row.keys()[0]]['batsman']] = batsman_runs.get(row[row.keys()[0]]['batsman'],0) + p

		trun = trun + p
	
		print("** Ball - " + str(count) )
		print("\n** Run - " + str(p) + '\n' )
		print "batsman : "+row[row.keys()[0]]['batsman']
		print "bowler : "+row[row.keys()[0]]['bowler']
		print "\n\n"
			
		if(innings == innings2 and trun > target):
			winner = "2"
			break


data = yaml.load(open(ifile,'r').read())
count = 0
trun = 0

innings1 = data['innings'][0]['1st innings']['deliveries']
innings2 = data['innings'][1]['2nd innings']['deliveries']

play(innings1)

target = trun
count = 0
trun = 0

play(innings2)


print "PREDICTED : "
print "\nTarget  : " + str(target)
print "Score  : " + str(trun)


print "\n"
if(winner != "2"):
	print "Winner :Team 1"

else:
	print "Winner : Team 2 "
print "\n"

top3 = sorted(i1_batsman_runs, key = i1_batsman_runs.__getitem__, reverse = True)[:3]
print "Team 1"
for i in top3:
	print i,"-",i1_batsman_runs[i]
print "\n\n"
top3 = sorted(i2_batsman_runs, key = i2_batsman_runs.__getitem__, reverse = True)[:3]

print "Team 2"
for i in top3:
	print i,"-",i2_batsman_runs[i]

def maxrunplayer(ifile):
	data = yaml.load(open(ifile,'r').read())


	innings1 = data['innings'][0]['1st innings']['deliveries']
	innings2 = data['innings'][1]['2nd innings']['deliveries']


	in1_score = 0
	in2_score = 0

	i1_batsman_runs = dict()
	i2_batsman_runs = dict()

	for row in innings1:
		in1_score += row[row.keys()[0]]['runs']['total']
		try:
			i1_batsman_runs[row[row.keys()[0]]['batsman']] += row[row.keys()[0]]['runs']['batsman']
		except KeyError:
			i1_batsman_runs[row[row.keys()[0]]['batsman']] = 0
	
	for row in innings2:
		in2_score += row[row.keys()[0]]['runs']['total']
		try:
			i2_batsman_runs[row[row.keys()[0]]['batsman']] += row[row.keys()[0]]['runs']['batsman']
		except KeyError:
			i2_batsman_runs[row[row.keys()[0]]['batsman']] = 0

	print "\n\n\nACTUAL : \n"
	print "Team 1",in1_score
	print "Team 2",in2_score

	print "\n\n"
	top = sorted(i1_batsman_runs, key = i1_batsman_runs.__getitem__, reverse = True)[0]
	print "Innings 1 ",top,"-",i1_batsman_runs[top]

	top = sorted(i2_batsman_runs, key = i2_batsman_runs.__getitem__, reverse = True)[0]
	print "Innings 1 ",top,"-",i2_batsman_runs[top]

maxrunplayer(ifile)
