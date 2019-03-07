import ConfigParser
import os
import shutil
import sys
import time
from utilities import Utilities

if __name__ == '__main__':
    DEBUG = False
    archiveLocation = None
    archivedFile = None
    backup = None
    backupName = None
    backupDir = None
    backupFile = None
    blnContinue = True
    compress = False
    config = None
    configFile = None
    deleteDirectory = None
    error = False
    fileName = ''
    logger = None
    mesAnoDir = None
    mesAno = time.strftime("%B%Y")
    mesDia = time.strftime("%m%d")
    return_value = False
    tarfile = None
    utils = Utilities()
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
                    backupDir = config.get('runtime', 'baseDir')
                    utils.log_output(logger, "Starting archive of {0}...".format(backupName), 'info')
                    if os.path.exists(backupDir):
                        utils.log_output(logger, "Backup directory: {0}".format(backupDir), 'debug')
                        backup = os.path.join(backupDir, backupName)
                        if os.path.exists(backup):
                            # backupFile = os.path.join(os.sep, backupDir, fileName)
                            # backupFile = os.path.join(backupDir, fileName)
                            # Check to see if this a directory
                            if os.path.isdir(backup):
                                # create a tgz file of the directory
                                tarfile = os.path.join(backupDir, config.get('tar', 'tarfile'))
                                utils.log_output(logger, "Tarring the {0} directory to {1}...".format(backup, tarfile), 'info')
                                if utils.create_tarfile(tarfile, backup):
                                    backupFile = tarfile
                                    utils.log_output(logger, "Tar file {0} has been created".format(backupFile), 'info')

                                    deleteDirectory = config.get('tar', 'deleteDirectory')
                                    if deleteDirectory:
                                        # Remove the directory
                                        shutil.rmtree(backup)
                                else:
                                    error = True
                                    utils.log_output(logger, "Error creating {0}".format(tarfile), 'error')
                            else:
                                utils.log_output(logger, "{0} is a file. May need to compress it.".format(backup), 'info')
                                backupFile = backup

                            if error:
                                utils.log_output(logger, "Error creating the tar file. Review the log", 'error')
                            else:
                                utils.log_output(logger, "Saving {0} to {1}".format(backupFile, archiveLocation), 'info')
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

                                        # Archive any existing file, appending the date/time
                                        if os.path.exists(archivedFile):
                                            utils.log_output(logger, "There is already a file named {0} in the {1} directory".format(fileName, archivedDir), 'error')
                                            utils.log_output(logger, "Attempting to archive {0}...".format(archivedFile), 'info')
                                            arr = utils.archive_file(archivedFile)
                                            blnContinue = arr[0]
                                            if blnContinue:
                                                utils.log_output(logger, "{0} has been archived as {1}".format(archivedFile, arr[1]), 'debug')

                                        if blnContinue:
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
                                        else:
                                            utils.log_output(logger, "Unable to rename existing {0} file. Manual intervention needed.".format(fileName), 'info')
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
