import zipfile
import logging
import os
import sys
import tarfile
import traceback


class Utilities:
    logger = None

    def __init__(self):
        pass

    def capture_exception(self, logger, mess, ex):
        err = ''
        tblst = None
        lineno = None
        details = None
        try:
            err = ex[1]
            tblst = traceback.extract_tb(ex[2])[0]
            lineno = tblst[1]
            details = tblst[3]
        except:
            err = sys.exc_info()[1]
            tblst = traceback.extract_tb(sys.exc_info()[2])[0]
            lineno = tblst[1]
            details = tblst[3]
        finally:
            self.log_output(logger, "{0}.\nType: {1}\nLine number: {2}\nDetails: {3}".format(mess, str(err), str(lineno), str(details)), 'error')

    @staticmethod
    def create_tarfile(output_file, source_dir):
        created = False
        try:
            tar = tarfile.open(output_file, "w:gz")
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            tar.close()
            created = True
        except:
            Utilities.capture_exception(Utilities.logger, "Error creating tar file{0}".format(sys.exc_info()))
            created = False
        finally:
            return created

    def create_zipfile(self, filename):
        blnzipcreated = False
        zip_file = None
        try:
            zip_file = "{0}.gz".format(filename)
            zf = zipfile.ZipFile(zip_file, mode='w')
            try:
                zf.write(filename)
                blnzipcreated = True
                self.log_output(self, "{0} was successfully compressed.".format(filename), 'info')
            except:
                Utilities.capture_exception(self, Utilities.logger, "Error creating zip for {0}".format(filename), sys.exc_info())
                blnzipcreated = False
            finally:
                zf.close()
        except:
            Utilities.capture_exception(self, Utilities.logger, "Error creating zip for {0}".format(filename), sys.exc_info())
            blnzipcreated = False
        return blnzipcreated

    @staticmethod
    def log_output(logger, mess, level):
        try:
            if logger:
                if level == 'debug':
                    logger.debug(mess)
                elif level == 'error':
                    logger.error(mess)
                elif level == 'warning':
                    logger.warning(mess)
                else:
                    logger.info(mess)
            else:
                print(mess)
        except:
            print("Display output error:\n{0}".format(sys.exc_info()[0]))

    @staticmethod
    def get_logging():
        return Utilities.logger

    @staticmethod
    def set_logger(filename, level):
        try:
            print("File: {0}".format(filename))
            Utilities.logger = logging.getLogger('Logging')
            handler = logging.FileHandler(filename)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            Utilities.logger.addHandler(handler)
            if level.lower() == 'debug':
                Utilities.logger.setLevel(logging.DEBUG)
            else:
                Utilities.logger.setLevel(logging.INFO)
        except IOError as ioe:
                print("IO Error setting logging. {0}".format(ioe))
        except:
                print("Error setting logging\n{0}".format(sys.exc_info()[0]))
