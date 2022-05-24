#!/usr/bin/python3
from fabric.api import *
import getpass
#import MySQLdb
import re
import subprocess
import requests

env.user = "ghamontree"
env.password = ""
env.hosts = ['']
#env.password = getpass.getpass(prompt='Password: ', stream=None)

#env.roledefs = {
#        'Debian' : ['10.0.0.162'],
#        'CentOS7' : ['10.0.0.163'],
#        'FreeBSD' : ['10.0.0.119'],
#        'Database' : ['10.0.0.162']
#        }

def insert_spacing(mystr):
    #print('NEWLINECOUNT: '+ str(newstr.count("\n")))
    newstr = re.split(r"[~\r\n]+", mystr)
    newstr = ' '+'\n '.join(newstr)
    return newstr

def wiki_gen():
    #Get first block of general information.
    hostname = run("hostname")
    run('touch /tmp/'+str(hostname))
    outF = open('/tmp/' + str(hostname), "a")
    outF.write("==Specs==\n\n")
    outF.write(insert_spacing("Hostname: "+hostname+"\n"))
    os = run("hostnamectl | grep Oper")
    outF.write(insert_spacing(os + "\n"))
    mem = run("awk '/MemTotal/ {print $2}' /proc/meminfo")
    outF.write(insert_spacing("Total Memory: "+mem+"\n"))
    disk = sudo("fdisk -l | grep Disk | grep G")
    outF.write(insert_spacing("Disk Space: "+disk+"\n\t"))

    #Check if it's hardware or virtio
    input_string = run("lspci -v | grep 'Kernel modules:'")
    pattern = "virtio_pci"
    match = re.findall("%s" % pattern, input_string)
    print(match)
    new_match = str(match)
    if (new_match) == "['virtio_pci', 'virtio_pci', 'virtio_pci', 'virtio_pci', 'virtio_pci']":
        server_type = "Virtualized by Ovirt"
    else:
        server_type = "Hardware"
    outF.write(insert_spacing("This server is: "+server_type+"\n"))

    #IP Info
    outF.write("\n\n==IP Addresses==\n\n")
    ip_info = run("ip addr")
    outF.write(insert_spacing(ip_info))

    #Routing Table
    outF.write("\n\n==Routing Table==\n\n")
    route_info = run("ip route list")
    outF.write(insert_spacing(route_info))

    #Partitions
    outF.write("\n\n==Partitions==\n\n")
    partition_info = run("lsblk")
    outF.write(insert_spacing(partition_info))

    #FSTAB
    outF.write("\n\n==FSTAB==\n\n")
    fstab_info = run("cat /etc/fstab")
    outF.write(insert_spacing(fstab_info))

    #CRONTAB --Need to get the daily/weekly stuff added / Not working on Debian
    outF.write("\n\n==Crontab==\n\n")
    cron_info = sudo("tail -n 1000 /var/spool/cron/*")
    outF.write(insert_spacing(cron_info))

    #Running Proccesses
    outF.write("\n\n==Running Processes==\n\n")
    process_info = run("ps auxfwww")
    outF.write(insert_spacing(process_info))

    #SystemD Units
    outF.write("\n\n==SystemD Units==\n\n")
    systemd_info = run("systemctl list-units | grep ''")
    outF.write(insert_spacing(systemd_info))

    #Services
    wordSearch = (process_info)
    str(wordSearch.find('crypto'))
    str(wordSearch.find('sshd'))
    str(wordSearch.find('httpd'))
    outF.write("\n\n==Services==\n\n")
    if wordSearch.find('sshd') >= 0:
        outF.write("[[sshd]]\n")
    if wordSearch.find('httpd') >= 0:
        outF.write("[[httpd]]\n")
    if wordSearch.find('monit') >= 0:
        outF.write("[[monit]]\n")
    if wordSearch.find('wazuh') >= 0:
        outF.write("[[wazuh]]\n")
    if wordSearch.find('cacti') >= 0:
        outF.write("[[cacti]]\n")
    if wordSearch.find('icinga') >= 0:
        outF.write("[[icinga]]\n")
    #if wordSearch.find('') >= 0:
    #    outF.write("[[]]\n")
    outF.write("\n\n[[Category:Data Centers]]")









def uphost():
    run("hostname")
    run("uptime")

def uptime():
	local("uptime")

def hostname():
	run("hostname")

#---------------------Testing DB
def dbtest():
    myDB = MySQLdb.connect(host="",port=3306,user="root",passwd="",db="test")
    cHandler = myDB.cursor()
    cHandler.execute("SHOW DATABASES;")
    cHandler.execute("SELECT CURDATE();")

    results = cHandler.fetchall()
    for items in results:
        print (items[0])

#---------------------Testing Groups
@roles('FreeBSD')
def updateBSD():
    env.shell = '/usr/local/bin/bash -c'
    run("pkg upgrade -y")

@roles('CentOS7')
def updateSUSE():
    env.shell = '/bin/bash -l -c'
    run("transactional-update -n")

@roles('Debian')
def updateDebian():
    env.shell = '/bin/bash -l -c'
    run("apt-get update -y")

def updateAll():
    execute(updateBSD)
    execute(updateSUSE)
    execute(updateDebian)
