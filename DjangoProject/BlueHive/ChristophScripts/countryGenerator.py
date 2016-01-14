import csv

with open("countries.csv", "rb") as f:
	reader = csv.reader(f, delimiter="\t")
	for i, line in enumerate(reader):
		#print 'line[{}] = {}'.format(i, line)
		#print i+1
		#print line[0]
		print "{"
		print "\"model\": \"BlueHive.Nationality\","
		print "\"pk\": " + str(i+1) + ","
		print "\"fields\": {"
		print "\"date_created\": \"2015-11-11T17:41:28+00:00\","
		print "\"date_altered\": \"2015-11-11T17:41:28+00:00\","
		print "\"code\": \"" + line[0] +"\","
		print "\"value\": \"" + line[1] + "\""
		print "}"
		print "},"