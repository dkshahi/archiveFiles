import zipfile
import logging
import os
import sys
import traceback

class utilities:
    logger = None

    def __init__(self):
        pass;

    def captureException(self, logger, mess, ex):
        err = ''
        tblst = None
        lineno = None
        details = None
        try:
            err = ex[1]
            tblst = traceback.extract_tb( ex[2] )[0]
            lineno = tblst[1]
            details = tblst[3]
        except:
            err = sys.exc_info()[1]
            tblst = traceback.extract_tb( sys.exc_info()[2] )[0]
            lineno = tblst[1]
            details = tblst[3]
        finally:
            self.logOutput(logger, "{0}.\nType: {1}\nLine number: {2}\nDetails: {3}".format(mess,  str(err), str(lineno), str(details) ), 'error')

    def createzipfile(self, f):
        f_in = None
        f_out = None
        blnZipCreated = False
        zip_file = None
        try:
            zip_file = "{0}.gz".format(f)
            zf = zipfile.ZipFile(zip_file, mode='w')
            try:
                zf.write(f)
                blnZipCreated = True
                self.logOutput(self,"{0} was successfully compressed.".format(f), 'info')
            except:
                utilities.captureException(self, utilities.logger, "Error creating zip for {0}".format(f), sys.exc_info())
                blnZipCreated = False
            finally:
                zf.close()
        except:
            utilities.captureException(self, utilities.logger, "Error creating zip for {0}".format(f), sys.exc_info())
            blnZipCreated = False
        return blnZipCreated

    def logOutput(self, logger, mess, level):
        try:
            if logger:
                if (level == 'debug'):
                    logger.debug(mess)
                elif (level == 'error'):
                    logger.error(mess)
                elif (level == 'warning'):
                    logger.warning(mess)
                else:
                    logger.info(mess)
            else:
                print(mess)
        except:
            print("Dispaly Output error:\n{0}".format( sys.exc_info()[0] ) )

	def getLogging(self):
		return utilities.logger

	def setLogger(self, sFile, sLevel):
		try:
			print("File: {0}".format(sFile))
			utilities.logger = logging.getLogger('Logging')
			handler = logging.FileHandler(sFile)
			formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
			handler.setFormatter(formatter)
			utilities.logger.addHandler(handler)
			if (sLevel.lower() == 'debug' ):
				utilities.logger.setLevel(logging.DEBUG)
			else:
				utilities.logger.setLevel(logging.INFO)
		except IOError as ioe:
			print("IO Error setting logging. {0}".format(ioe))
		except:
			print("Error setting logging\n{0}".format(sys.exc_info()[0]))
