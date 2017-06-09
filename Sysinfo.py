import os
import psutil

#Donne la température du CPU (retourne un string)
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=", "").replace("'C\n", ""))


# Donne des informations relative à la RAM (en octets)
# Index 0: RAM totale
# Index 1: RAM utilisé
# Index 2: RAM non utilisé
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])


# Donne le % de CPU utilisé (retourne un string)
def getCPUuse():
    return psutil.cpu_percent(0.5)


# Renvoie des informations sur l'espace disque (liste)
# Index 0: Espace disque total
# Index 1: Espace disque utilisé
# Index 2: Espace disque restant
# Index 3: Pourcentage de disque utilisé
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])

#Renvoie d'état de la wifi actif ou non
def getInfoWifi(wifiname = 'wlan0'):
    p = psutil.net_if_stats()

    try:
        wifi = p[wifiname]
    except Exception as error:
        print(error)

    return (wifi[0])

def getInfoEth(ethname = 'eth0'):
    p = psutil.net_if_stats()

    try:
        eth = p[ethname]
    except Exception as error:
        print(error)

    return (eth[0])

#Retourne le % d'utilisation du CPU en fonction PID
def getCPUloadPerPID(pid=0):
    if not pid<0:
        try:
            current_process = psutil.Process(pid=pid)
        except psutil.NoSuchProcess:
            return
        current_process_load = current_process.cpu_percent(interval=0.5)
        return current_process_load
    else:
        return

#Retourne le % CPU
def getCPUloadPerProc():
    i = 0
    processes_info = []
    while i < 2:
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'cpu_percent', 'name'])
                if pinfo['cpu_percent'] > 0.0:
                    processes_info.append(pinfo)
            except psutil.NoSuchProcess:
                pass
        i += 1
    return processes_info


#Retourne l'adresse MAC du composant
def getMacAddress(wifi='wlan0'):
    adressemac = str(os.popen('ifconfig ' + wifi + ' | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'').readline())
    if len(adressemac) == 17:#La taille de la mac address est déjà bonne
        return adressemac
    else:
        if len(adressemac) > 17:#On rabote la macaddress pour qu'elle fasse la bonne taille
            return adressemac[:-(len(adressemac)-17)]
        if len(adressemac) < 17: #Erreur macaddress trop petite
            raise ValueError('MacAddress trop petite')
