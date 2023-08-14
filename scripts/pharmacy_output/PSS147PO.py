# PSS147PO ;BIR/RTR-Post Install routine for patch PSS*1*147 ;07/17/09
# 1.0;PHARMACY DATA MAMAGEMENT;**147**;9/30/97;Build 16

import os
import sys
import datetime
import fileinput
import subprocess

def PSS147PO():
    PSSKDACT = ''
    PSSMRMPF = ''
    os.system('rm -rf /tmp/$J/PSS147TX')
    os.system('touch /tmp/$J/PSS147TX')
    os.system('echo "Installation of patch PSS*1.0*147 has been successfully completed!" >> /tmp/$J/PSS147TX')
    os.system('echo " " >> /tmp/$J/PSS147TX')
    if XPDGREF["PSS147IN"]["INSTALL"]:
        PSSKDACT = '3'
        SUBS()
    os.system('echo "Please use the IV Additive Report to review the auto-populated data in the" >> /tmp/$J/PSS147TX')
    os.system('echo "new ADDITIVE FREQUENCY (#18) Field of the IV ADDITIVES (#52.6) File and" >> /tmp/$J/PSS147TX')
    os.system('echo "edit as necessary." >> /tmp/$J/PSS147TX')
    os.system('echo " " >> /tmp/$J/PSS147TX')
    PSSKDACT = '7'
    if not XPDGREF["PSS147IN"]["INSTALL"]:
        os.system('echo "Populating new Additive Frequency field..."')
        IV()
        os.system('echo "Finished populating new Additive Frequency field..."')
    os.system('echo "Rebuilding PSS MGR Menu..."')
    MENU()
    os.system('echo "Finished rebuilding PSS MGR Menu..."')
    PROT()
    PRMAIL()
    os.system('echo "Generating Mail message...."')
    MAIL()
    os.system('echo "Mail message sent..."')

def IV():
    PSSADPN = ''
    PSSADPRC = ''
    PSSADPDR = ''
    PSSADPN1 = ''
    PSSADPN3 = ''
    PSSADPCL = ''
    X = ''
    for PSSADPN in range(len(PS(52.6)["B"])):
        for PSSADPRC in range(len(PS(52.6)["B"][PSSADPN])):
            PSSADPCL = ''
            if PS(52.6)[PSSADPRC][0][14] != '':
                continue
            PSSADPDR = PS(52.6)[PSSADPRC][0][2]
            if not PSSADPDR:
                continue
            PSSADPN1 = PS(52.6)[PSSADPRC][0]["ND"][0]
            PSSADPN3 = PS(52.6)[PSSADPRC][0]["ND"][2]
            if PSSADPN1 and PSSADPN3:
                X = subprocess.Popen(['python', 'PSNAPIS.py', PSSADPN1, PSSADPN3], stdout=subprocess.PIPE)
                PSSADPCL = X.stdout.read()
                X.wait()
            if not PSSADPCL:
                PSSADPCL = PS(52.6)[PSSADPRC][0][0][2]
            if "VT" in PSSADPCL:
                PS(52.6)[PSSADPRC][0][14] = '1'
            elif PSSADPCL:
                PS(52.6)[PSSADPRC][0][14] = 'A'

def MENU():
    PSSKDARS = ''
    PSSKDARM = ''
    PSSKDARM = subprocess.Popen(['python', 'XPDMENU.py', 'PSS MGR'], stdout=subprocess.PIPE)
    if not PSSKDARM:
        os.system('echo "Unable to find PSS MGR Menu Option...."')
        os.system('echo "Unable to find PSS MGR menu option.." >> /tmp/$J/PSS147TX')
        os.system('echo "Please Log a Remedy Ticket and refer to this message." >> /tmp/$J/PSS147TX')
        os.system('echo " " >> /tmp/$J/PSS147TX')
        return
    if subprocess.Popen(['python', 'XPDMENU.py', 'PSS MGR', 'PSS IV SOLUTION REPORT', 'B']):
        KTM()
        PSSKDARS = subprocess.Popen(['python', 'XPDMENU.py', 'PSS MGR', 'PSS IV SOLUTION REPORT', 'D'])
        if not PSSKDARS:
            os.system('echo "Unable to unlink PSS IV SOLUTION REPORT from PSS MGR Menu Option...."')
            os.system('echo "Unable to unlink PSS IV SOLUTION REPORT from PSS MGR Menu Option" >> /tmp/$J/PSS147TX')
            os.system('echo "Please Log a Remedy Ticket and refer to this message." >> /tmp/$J/PSS147TX')
            os.system('echo " " >> /tmp/$J/PSS147TX')
        return
    KTM()
    PSSKDARS = subprocess.Popen(['python', 'XPDMENU.py', 'PSS ADDITIVE/SOLUTION REPORTS', 'PSS IV ADDITIVE REPORT', '', '1'])
    if not PSSKDARS:
        os.system('echo "Unable to attach PSS IV ADDITIVE REPORT to PSS ADDITIVE/SOLUTION REPORTS Menu."')
        os.system('echo "Unable to attach PSS IV ADDITIVE REPORT to PSS ADDITIVE/SOLUTION REPORTS Menu" >> /tmp/$J/PSS147TX')
        os.system('echo "Please Log a Remedy Ticket and refer to this message." >> /tmp/$J/PSS147TX')
        os.system('echo " " >> /tmp/$J/PSS147TX')
    PSSKDARS = subprocess.Popen(['python', 'XPDMENU.py', 'PSS ADDITIVE/SOLUTION REPORTS', 'PSS IV SOLUTION REPORT', '', '2'])
    if not PSSKDARS:
        os.system('echo "Unable to attach PSS IV SOLUTION REPORT to PSS ADDITIVE/SOLUTION REPORTS Menu."')
        os.system('echo "Unable to attach PSS IV SOLUTION REPORT to PSS ADDITIVE/SOLUTION REPORTS Menu" >> /tmp/$J/PSS147TX')
        os.system('echo "Please Log a Remedy Ticket and refer to this message." >> /tmp/$J/PSS147TX')
        os.system('echo " " >> /tmp/$J/PSS147TX')
    PSSKDARS = subprocess.Popen(['python', 'XPDMENU.py', 'PSS MGR', 'PSS ADDITIVE/SOLUTION REPORTS', '', '18'])
    if not PSSKDARS:
        os.system('echo "Unable to attach PSS ADDITIVE/SOLUTION REPORTS to PSS MGR Menu Option...."')
        os.system('echo "Unable to attach PSS ADDITIVE/SOLUTION REPORTS to PSS MGR Menu Option" >> /tmp/$J/PSS147TX')
        os.system('echo "Please Log a Remedy Ticket and refer to this message." >> /tmp/$J/PSS147TX')
        os.system('echo " " >> /tmp/$J/PSS147TX')

def PROT():
    PSSMRMPF = ''
    os.system('echo "Attaching PSS MED ROUTE RECEIVE protocol to XUMF MFS EVENTS protocol..."')
    PSSMRMPR = subprocess.Popen(['python', 'XPDMENU.py', 'XUMF MFS EVENTS'], stdout=subprocess.PIPE)
    if not PSSMRMPR:
        PASE()
        PSSMRMPF = '1'
        KTM()
        return
    PSSMRMDJ = subprocess.Popen(['python', 'XPDMENU.py', 'PSS MED ROUTE RECEIVE'], stdout=subprocess.PIPE)
    if not PSSMRMDJ:
        PASEX()
        PSSMRMPF = '2'
        KTM()
        return
    if subprocess.Popen(['python', 'XPDMENU.py', 'XUMF MFS EVENTS', 'PSS MED ROUTE RECEIVE', 'B']):
        ADDPRX()
        return
    KTM()
    PSSMRMAT = {'data': [{'file': '101.01', 'fields': {'+2,': PSSMRMRDJ}}, {'file': '101', 'fields': {'+1,': PSSMRMRPR}}]}
    subprocess.Popen(['python', 'UPDATE^DIE.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if subprocess.Popen(['python', 'XPDMENU.py', 'XUMF MFS EVENTS', 'PSS MED ROUTE RECEIVE', 'B']):
        PSSMRMPF = '3'
        PACEZ()
        KTM()

def PASE():
    os.system('echo " "')
    os.system('echo "Cannot find XUMF MFS EVENTS protocol on system, installation will continue,"')
    os.system('echo "please see post installation mail message for further instructions."')
    os.system('echo " "')

def PASEX():
    os.system('echo " "')
    os.system('echo "Cannot find PSS MED ROUTE RECEIVE protocol on system, installation will"')
    os.system('echo "continue, please see post installation mail message for further instructions."')
    os.system('echo " "')

def PACEZ():
    os.system('echo " "')
    os.system('echo "Unable to attach PSS MED ROUTE RECEIVE protocol to XUMF MFS EVENTS"')
    os.system('echo "protocol. These protocols must be attached in order to process any Standard"')
    os.system('echo "Medication Route updates. Please log a Remedy Ticket and refer to this message."')
    os.system('echo " "')

def PRMAIL():
    if not PSSMRMPF:
        return
    if PSSMRMPF == '1':
        os.system('echo "Unable to find the XUMF MFS EVENTS protocol. This protocol was exported in"')
        os.system('echo "patch XU*8.0*474. You must have this protocol so the PSS MED ROUTE RECEIVE"')
        os.system('echo "protocol can be attached to it, in order to process any Standard Medication"')
        os.system('echo "Route updates. Please log a Remedy Ticket and refer to this message."')
    elif PSSMRMPF == '2':
        os.system('echo "Unable to find the PSS MED ROUTE RECEIVE protocol. This protocol is exported"')
        os.system('echo "in patch PSS*1.0*147. You must have this protocol so it can be attached to the"')
        os.system('echo "XUMF MFS EVENTS protocol, in order to process any Standard Medication Route"')
        os.system('echo "updates. Please log a Remedy Ticket and refer to this message."')
    elif PSSMRMPF == '3':
        os.system('echo "Unable to attach the PSS MED ROUTE RECEIVE protocol to the XUMF MFS EVENTS"')
        os.system('echo "protocol. These protocols must be attached in order to process any Standard"')
        os.system('echo "Medication Route updates. Please log a Remedy Ticket and refer to this message."')

def MAIL():
    PSS147RC = ''
    XMTEXT = ''
    XMY = ''
    XMSUB = ''
    XMDUZ = ''
    XMMG = ''
    XMSTRIP = ''
    XMROU = ''
    XMYBLOB = ''
    XMZ = ''
    XMDUN = ''
    XMSUB = "PSS*1*147 Installation Complete"
    XMDUZ = "PSS*1*147 Install"
    XMTEXT = "^TMP($J,""PSS147TX"","
    PSS147RC = subprocess.Popen(['python', 'XMD.py', '-s', XMSUB, '-u', XMDUZ, '-t', XMTEXT], stdout=subprocess.PIPE)
    for line in PSS147RC.stdout:
        line = line.rstrip()
        XMY.append(line)
    XMY = list(set(XMY))
    subprocess.Popen(['python', 'XMD.py', '-s', XMSUB, '-u', XMDUZ, '-t', XMTEXT, '-r', ','.join(XMY)])

PSS147PO()