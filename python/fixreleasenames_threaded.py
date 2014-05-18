#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys, os, time
import threading
try:
	import queue
except ImportError:
	import Queue as queue
import subprocess
import string
import signal
import datetime

import lib.info as info
from lib.info import bcolors
conf = info.readConfig()
cur = info.connect()
start_time = time.time()
pathname = os.path.abspath(os.path.dirname(sys.argv[0]))

if len(sys.argv) == 1:
	print(bcolors.ERROR + "\nAn argument is required\n\n"
		+ "python " + sys.argv[0] + " [md5, nfo, filename, par2]     ...: To process all previously unprocessed releases, using [md5, nfo, filename, par2].\n"
		+ "python " + sys.argv[0] + " [nfo, filename, par2] prehashid                ...: To process all releases not matched to prehashID, using [nfo, filename, par2].\n"
		+ "python " + sys.argv[0] + " nfo clean                                  ...: To process all releases processed by filename, using nfo.\n"
		+ "python " + sys.argv[0] + " par2 clean                                 ...: To process all releases processed by filename and nfo, using par2.\n"
		+ "python " + sys.argv[0] + " predbft clean                                  ...: To process all releases using reverse match by PreDB title.\n"
		+ bcolors.ENDC)
	sys.exit()

if sys.argv[1] != "nfo" and sys.argv[1] != "filename" and sys.argv[1] != "md5" and sys.argv[1] != "par2" and sys.argv[1] != "predbft":
	print(bcolors.ERROR + "\n\An invalid argument was supplied\npostprocess_threaded.py [md5, nfo, filename, par2, predbft]\n" + bcolors.ENDC)
	sys.exit()

if len(sys.argv) == 3 and sys.argv[1] == "nfo" and sys.argv[2] == "clean":
	clean = " isrenamed = 0 AND proc_files = 1 "
elif len(sys.argv) == 3 and sys.argv[1] == "par2" and sys.argv[2] == "clean":
	clean = " isrenamed = 0 AND proc_files = 1 AND proc_nfo = 1 "
elif len(sys.argv) == 3 and sys.argv[1] == "nfo" and sys.argv[2] == "prehashid":
	clean = " prehashID = IS NULL "
elif len(sys.argv) == 3 and sys.argv[1] == "par2" and sys.argv[2] == "prehashid":
	clean = " prehashID = IS NULL "
elif len(sys.argv) == 3 and sys.argv[1] == "filename" and sys.argv[2] == "prehashid":
	clean = " prehashID = IS NULL "
else:
	clean = " isrenamed = 0 "

print(bcolors.HEADER + "\nfixReleasesNames {} Threaded Started at {}".format(sys.argv[1],datetime.datetime.now().strftime("%H:%M:%S")) + bcolors.ENDC)

cur[0].execute("SELECT value FROM tmux WHERE setting = 'fixnamethreads'")
run_threads = cur[0].fetchone()
cur[0].execute("SELECT value FROM tmux WHERE setting = 'fixnamesperrun'")
perrun = cur[0].fetchone()

datas = []
maxtries = 0

if len(sys.argv) > 1 and sys.argv[1] == "nfo":
    run = "SELECT DISTINCT rel.ID AS releaseID FROM releases rel INNER JOIN releasenfo nfo ON (nfo.releaseID = rel.ID) WHERE categoryID = 8010 AND proc_nfo = 0 AND" + clean + "ORDER BY postdate DESC LIMIT %s"
    cur[0].execute(run, (int(perrun[0]) * int(run_threads[0])))
    datas = cur[0].fetchall()
elif len(sys.argv) > 1 and (sys.argv[1] == "filename"):
    run = "SELECT DISTINCT rel.ID AS releaseID FROM releases rel INNER JOIN releasefiles relfiles ON (relfiles.releaseID = rel.ID) WHERE categoryID = 8010 AND proc_files = 0 AND" + clean + "ORDER BY postdate ASC LIMIT %s"
    cur[0].execute(run, (int(perrun[0]) * int(run_threads[0])))
    datas = cur[0].fetchall()
elif len(sys.argv) > 1 and (sys.argv[1] == "md5"):
    while len(datas) == 0 and maxtries >= -5:
        run = "SELECT DISTINCT rel.ID FROM releases rel INNER JOIN releasefiles rf ON rel.ID = rf.releaseID WHERE rel.dehashstatus BETWEEN %s AND 0 AND (rel.ishashed = 1 OR rf.ishashed = 1) AND prehashID = 0 ORDER BY postdate ASC LIMIT %s"
        cur[0].execute(run, (maxtries, int(perrun[0])*int(run_threads[0])))
        datas = cur[0].fetchall()
        maxtries = maxtries - 1
elif len(sys.argv) > 1 and (sys.argv[1] == "par2"):
	#This one does from oldest posts to newest posts, since nfo pp does same thing but newest to oldest
    run = "SELECT ID AS releaseID, guid, groupID FROM releases WHERE categoryID = 8010 AND proc_par2 = 0 AND" + clean + "ORDER BY postdate ASC LIMIT %s"
    cur[0].execute(run, (int(perrun[0]) * int(run_threads[0])))
    datas = cur[0].fetchall()
elif len(sys.argv) > 1 and (sys.argv[1] == "predbft"):
	#This one does from oldest posts to newest posts since there are many other more efficient PreDB matching schemes
	run = "SELECT ID AS preid FROM prehash WHERE LENGTH(title) >= 15 AND searched = 0 AND title NOT REGEXP '[\"\<\> ]' ORDER BY predate ASC LIMIT %s"
	cur[0].execute(run, (int(perrun[0])/10 * int(run_threads[0])))
	datas = cur[0].fetchall()

#close connection to mysql
info.disconnect(cur[0], cur[1])

if not datas:
	print(bcolors.HEADER + "No Work to Process" + bcolors.ENDC)
	sys.exit()

my_queue = queue.Queue()
time_of_last_run = time.time()

class queue_runner(threading.Thread):
	def __init__(self, my_queue):
		threading.Thread.__init__(self)
		self.my_queue = my_queue

	def run(self):
		global time_of_last_run

		while True:
			try:
				my_id = self.my_queue.get(True, 1)
			except:
				if time.time() - time_of_last_run > 3:
					return
			else:
				if my_id:
					time_of_last_run = time.time()
					subprocess.call(["php", pathname+"/../bin/fixreleasenames.php", ""+my_id])
					time.sleep(.03)
					self.my_queue.task_done()

def main():
	global time_of_last_run
	time_of_last_run = time.time()

	if sys.argv[1] == 'md5':
		print(bcolors.HEADER + "We will be using a max of {} threads, a queue of {} {} releases. dehashstatus range {} to 0".format(run_threads[0], "{:,}".format(len(datas)), sys.argv[1], maxtries + 1) + bcolors.ENDC)
	else:
		print(bcolors.HEADER + "We will be using a max of {} threads, a queue of {} releases using {}".format(run_threads[0], "{:,}".format(len(datas)), sys.argv[1]) + bcolors.ENDC)
	time.sleep(2)

	def signal_handler(signal, frame):
		sys.exit(0)

	signal.signal(signal.SIGINT, signal_handler)

	if True:
		#spawn a pool of place worker threads
		for i in range(int(run_threads[0])):
			p = queue_runner(my_queue)
			p.setDaemon(False)
			p.start()

	#now load some arbitrary jobs into the queue
	if sys.argv[1] == "nfo":
		for release in datas:
			time.sleep(.03)
			my_queue.put("%s %s" % ("nfo", release[0]))
	elif sys.argv[1] == "filename":
		for release in datas:
			time.sleep(.03)
			my_queue.put("%s %s" % ("filename", release[0]))
	elif sys.argv[1] == "md5":
		for release in datas:
			time.sleep(.03)
			my_queue.put("%s %s" % ("md5", release[0]))
	elif sys.argv[1] == "par2":
		for release in datas:
			time.sleep(.03)
			my_queue.put("%s %s %s %s" % ("par2", release[0], release[1], release[2]))
	elif sys.argv[1] == "predbft":
		for release in datas:
		time.sleep(.03)
	 		my_queue.put("%s %s" % ("predbft", release[0]))

	my_queue.join()

	print(bcolors.HEADER + "\nfixReleaseNames {} Threaded Completed at {}".format(sys.argv[1],datetime.datetime.now().strftime("%H:%M:%S")) + bcolors.ENDC)
	print(bcolors.HEADER + "Running time: {}\n\n".format(str(datetime.timedelta(seconds=time.time() - start_time))) + bcolors.ENDC)

if __name__ == '__main__':
	main()
