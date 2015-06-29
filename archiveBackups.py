import ConfigParser
import os
import sys
import time

from utilities import *

if __name__ == '__main__':
	DEBUG = False
	mesAno = time.strftime("%B%Y")
	mesDia = time.strftime("%m%d")
	backupName = None
	backupDir = None
	backupFile = None
	archivedDir = None
	archivedFile = None
	mesAnoDir = None
	fileName = ''
	utls = None
	logger = None
	compress = False
	config = None
	configFile = None
	retval = False
	try:
		if (len(sys.argv) == 4):
			try:
				config = ConfigParser.ConfigParser()
				configFile = sys.argv[1]
				if os.path.isfile(configFile):
					config.read(configFile)
					utls = utilities()
					utls.setLogger(config.get('runtime','logFile'), config.get('runtime','logLevel'))
					logger = utls.getLogging()
					compress = config.get('runtime','compress')
	
					backupName = sys.argv[2]
					fileName = sys.argv[3]
					utls.logOutput(logger, "Starting archive {0} process...".format(backupName), 'info')
					backupDir = os.path.join(config.get('runtime','baseDir'), os.sep, backupName)
					if (os.path.exists(backupDir)):
						utls.logOutput(logger, "Working inside {0}".format(backupDir), 'debug')
						backupFile = os.path.join(os.sep, backupDir, fileName)
						utls.logOutput(logger, "Backup file: {0}".format(backupFile), 'debug')

						if (os.path.isfile(backupFile)):
							#Esnure month/year archivedDir exists
							mesAnoDir = os.path.join(os.sep, backupDir, mesAno)
							if not (os.path.exists(mesAnoDir)):
								os.makedirs(mesAnoDir)
							else:
								utls.logOutput(logger, "{0} already exists.".format(mesAnoDir), 'info')

							archivedDir = os.path.join(os.sep, mesAnoDir, mesDia)
							if not (os.path.exists(archivedDir)):
								os.makedirs(archivedDir)
							else:
								utls.logOutput(logger,"{0} already exists.".format(archivedDir), 'info')

							try:
								archivedFile = os.path.join(os.sep,archivedDir,fileName)
								os.rename(backupFile, archivedFile)
								utls.logOutput(logger, "{0} has been moved to {1}".format(backupFile,archivedFile), 'info' )
								if compress.lower() == 'true':
									try:
										retval = utls.createzipfile(archivedFile)
										if retval:
											try:
												os.remove(archivedFile)
												utls.logOutput(logger, "{0} has been removed.".format(archivedFile), 'info')
											except:
												utls.captureException(logger, "Error removing {0}.".format(archivedFile), sys.exc_info())
										else:
											utls.logOutput(logger, "Unable to compress {0}".format(archivedFile), 'error')
									except:
										utls.captureException(logger, "Error trying to compress {0}".format(archivedFile), 'error')
							except:
								utls.captureException(logger, "Error trying to rename {0} to {1}".format(backupFile,archivedFile),logger,sys.exc_info())
								#utls.logOutput(logger, "Unable rename {0} to {1}".format(backupFile, archivedFile), 'error')
						else:
							utls.logOutput(logger, "{0} not found. Nothing to backup.".format(backupFile), 'error')
					else:
						utls.logOutput(logger, "{0} does not exists!".format(backupDir), 'error')
				else:
					print("Unable to find config file!")
			except:
				print("Error archiving backup".format(sys.exc_info()))
		else:
			print("Incorrect call to {0}".format(sys.argv[0]))
	except:
		print("Error archiving backup\n{0}".format(sys.exc_info()))
