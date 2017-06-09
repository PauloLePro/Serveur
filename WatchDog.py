import logging
import logging.handlers
import Sysinfo
import re
import time
import sys
from daemon import Daemon
from logging.handlers import TimedRotatingFileHandler

class MyDaemon(Daemon):
    def run(self):
        init()

#Création de la classe WatchDog
class WatchDog:
    def __init__(self):

        self.logger = self._initlog()

    # Création du fichier de log
    def _initlog(self):

        """"""
        logger = logging.getLogger("Rotating Log")
        logger.setLevel(logging.INFO)

        date = time.strftime("%d:%m:%Y")

        nomFichierLog = str(Sysinfo.getMacAddress()+'.log') #time.strftime("%d/%m/%Y") +
        file = open(nomFichierLog, "a")
        file.close()

        path = "/var/www/{}".format(nomFichierLog)

        handler = TimedRotatingFileHandler(path, when="M", interval=1, backupCount=7) # D pour day // M pour minutes
        logger.addHandler(handler)

        format = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(format)

        return logger

    # Vérification pour la Wifi
    def infoWifi(self):
        if (Sysinfo.getInfoWifi() == True):
            return (True)
        else:
            return (False)

    def infoEth(self):
        if (Sysinfo.getInfoEth() == True):
            return (True)
        else:
            return (False)

    # Gère l'affichage pour l'info disque (liste 3)
    def infoDisk(self):
        regexpDisk = re.compile('(\d{1,3})+%', re.I)

        match = regexpDisk.search(Sysinfo.getDiskSpace()[3])
        disk = int(match.group(1))

        return disk


##########################################################################################################

    # On gère l'écriture dans le fichier de log des différentes informations
    def write(self):

        if self.infoWifi() != True:
            self.logger.info("wifi = False")
        else:
            self.logger.info("wifi = True")

        if self.infoEth() != True:
            self.logger.info("eth = False")
        else:
            self.logger.info("eth = True")

        self.logger.info('temperature CPU = '+Sysinfo.getCPUtemperature())

        self.logger.info('Utilisation du disque en % ='+str(self.infoDisk()))

        self.logger.info('Ram utiliser = '+Sysinfo.getRAMinfo()[1])

        self.logger.info('Utilisation du CPU en % ='+str(Sysinfo.getCPUuse()))

        #self.logger.info(Sysinfo.getCPUloadPerProc())

def init():
    wd = WatchDog()

    while True:
        wd.write()
        time.sleep(5)  # log toute les 30 secs

#Lance le script
if __name__ == '__main__':

    daemon = MyDaemon('/tmp/watchdog_daemon.pid')
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            print("unknow command")
            sys.exit(2)
        print("exit 0")
        sys.exit(0)
    else:
        print("usage %s start|stop|restart" % sys.argv[0])
        sys.exit(2)