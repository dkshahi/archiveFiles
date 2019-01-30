import ConfigParser
import os
import sys
import time
from utilities import Utilities

if __name__ == '__main__':
	DEBUG = False
	mesAno = time.strftime("%B%Y")
	mesDia = time.strftime("%m%d")
	backup = None
	backupName = None
	backupDir = None
	backupFile = None
	archiveLocation = None
	archivedFile = None
	error = False
	mesAnoDir = None
	fileName = ''
	utils = Utilities()
	logger = None
	compress = False
	config = None
	configFile = None
	return_value = False
	tarfile = None
	try:
		if len(sys.argv) == 4:
			try:
				config = ConfigParser.ConfigParser()
				configFile = sys.argv[1]
				if os.path.isfile(configFile):
					config.read(configFile)
					utils.set_logger(config.get('runtime', 'logFile'), config.get('runtime', 'logLevel'))
					logger = utils.get_logging()
					compress = config.get('runtime', 'compress')

					backupName = sys.argv[2]
					archiveLocation = sys.argv[3]
					utils.log_output(logger, "Starting archive {0} process...".format(backupName), 'info')
					backupDir = config.get('runtime', 'baseDir')
					if os.path.exists(backupDir):
						utils.log_output(logger, "Working inside {0}".format(backupDir), 'debug')
						backup = os.path.join(backupDir, backupName)
						if os.path.exists(backup):
							# backupFile = os.path.join(os.sep, backupDir, fileName)
							# backupFile = os.path.join(backupDir, fileName)
							utils.log_output(logger, "Backup file: {0}".format(backup), 'debug')

							# Check to see if this a directory
							if os.path.isdir(backup):
								# create a tgz file of the directory
								print('Need to create tar file of the {0} directory'.format(backup))
								tarfile = os.path.join(backupDir, config.get('tar', 'tarfile'))
								if utils.create_tarfile(tarfile, backup):
									backupFile = tarfile
								else:
									error = True
							else:
								backupFile = backup

							if error:
								print('Something is wrong')
							else:
								print("Will now be saving {0} to {1}".format(backupFile, archiveLocation))
								if os.path.isfile(backupFile):
									# Ensure month/year archivedDir exists
									# mesAnoDir = os.path.join(os.sep, backupDir, mesAno)
									mesAnoDir = os.path.join(backupDir, archiveLocation, mesAno)

									if not (os.path.exists(mesAnoDir)):
										os.makedirs(mesAnoDir)
									else:
										utils.log_output(logger, "{0} already exists.".format(mesAnoDir), 'info')

									# archivedDir = os.path.join(os.sep, mesAnoDir, mesDia)
									archivedDir = os.path.join(mesAnoDir, mesDia)
									if not (os.path.exists(archivedDir)):
										os.makedirs(archivedDir)
									else:
										utils.log_output(logger, "{0} already exists.".format(archivedDir), 'info')

									try:
										# archivedFile = os.path.join(os.sep,archivedDir,fileName)
										fileName = os.path.split(backupFile)[1]
										archivedFile = os.path.join(archivedDir, fileName)
										# Cancel if backup file already exist in directory
										if os.path.exists(archivedFile):
											utils.log_output(logger, "There is already a file named {0} in the {1} directory".format(fileName, archivedDir), 'error')
										else:
											os.rename(backupFile, archivedFile)
											utils.log_output(logger, "{0} has been moved to {1}".format(backupFile, archivedFile), 'info')
											if compress.lower() == 'true':
												try:
													return_value = utils.create_zipfile(archivedFile)
													if return_value:
														try:
															os.remove(archivedFile)
															utils.log_output(logger, "{0} has been removed.".format(archivedFile), 'info')
														except:
															utils.capture_exception(logger, "Error removing {0}.".format(archivedFile), sys.exc_info())
													else:
														utils.log_output(logger, "Unable to compress {0}".format(archivedFile), 'error')
												except:
													utils.capture_exception(logger, "Error trying to compress {0}".format(archivedFile), 'error')
									except:
										utils.capture_exception(logger, "Error trying to rename {0} to {1}".format(backupFile, archivedFile), sys.exc_info())
									# utls.log_output(logger, "Unable rename {0} to {1}".format(backupFile, archivedFile), 'error')
								else:
									utils.log_output(logger, "{0} not found. Nothing to backup.".format(backupFile), 'error')
					else:
						utils.log_output(logger, "{0} does not exists!".format(backupDir), 'error')
				else:
					print("Unable to find config file!")
			except:
				utils.capture_exception(logger, "Error archiving backup!", sys.exc_info())
		else:
			print("Usage: {0} config_file backup_name storage_location ".format(sys.argv[0]))
	except:
		print("Error starting archiving backup\n{0}".format(sys.exc_info()))
