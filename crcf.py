'''
Copyright (C) 2020 Sam He(HeGuanglin)

Discription:
    Implementation of the system task here.

History:
    Date        Author          Notes
 2020/02/05     Sam He          The first version
'''
import os
import sys

import time
import datetime
import timer

# Implementation of goto statement package
from goto import with_goto
# Implementation of timer/schedule package
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

import wexpect as expect

DefautlIP       = "127.0.0.1"
DefaultPort     = "21"
DefaultUserName = "huaawei"
DefaultPassword = "Huawei123!"
DefaultLoginWay = "ftp"


DefaultValues = [DefautlIP, DefaultPort, DefaultUserName, DefaultPassword, \
                 DefaultLoginWay, "", "", ""]

exe = expect.spawn("cmd.exe")
exe.expect(">")
exe.sendline("dir")
exe.expect(">")
exe.sendline("exit")
print("-------------------------------------------------")
print(" Welcome to GL world, Thank you again anyway.")
print("-------------------------------------------------")
print("")

ft = open("test_doc.txt", mode="r")


class RouterLoginInfo():
    def __init__(self):
        self.ip = None
        self.port = None
        self.userName = None
        self.passWord = None
        self.loginWay = None
        self.args = None
        self.remoteFiles = None
        self.localFiles = None

class ConfigurationFileParser():
    def __init__(self):
        self.lineNumber = 0
        self.blockCommentStartFlag = 0
        self.blockCommentEndStartFlag = 0

    def setBlockCommentStartFlag(self):
        self.blockCommentStartFlag = 1

    def clrBlockCommentStartFlag(self):
        self.blockCommentStartFlag = 0

    def isExistBlockCommentStartFlag(self):
        return self.blockCommentStartFlag

    def setBlockCommentEndFlag(self):
        self.blockCommentEndStartFlag = 1

    def clrBlockCommentEndFlag(self):
        self.blockCommentEndStartFlag = 0

    def isExistBlockCommentEndFlag(self):
        return self.blockCommentEndStartFlag

    def setCurrLineNuber(self, _lineNum):
        self.lineNumber = _lineNum

    def resetCurrLineNumber(self):
        self.lineNumber = 0

    def addCurrLineNunber(self):
        self.lineNumber += 1

    def getCurrLineNumber(self):
        return self.lineNumber

def BlockCommentEndFlagExisted(_commentIdx):
    '''

    :param _commentIdx:
    :return:
    '''
    if (-1 == _commentIdx):
        return 0  # return false here with 0/zero
    else:
        return 1  # return true here with 1/one


def findSingleCommentFlag(_line):
    pass


def findBlockCommentStartFlag(_line):
    pass


def findBlockCommentEndFlag(_line):
    pass

def List2RouterLoginInfo(_list):
    rli = RouterLoginInfo()
    rli.ip = _list[0]
    rli.port = _list[1]
    '''
    rli.userName = _list[2]
    rli.passWord = _list[3]
    rli.loginWay = _list[4]
    rli.args = _list[5]
    rli.remoteFiles = _list[6]
    rli.localFiles = _list[7]
    '''
    return rli

def RouterLogin(_args):
    '''
    :param _args:
    :return:

    1. Router device login server(FTP/SFTP/Telnet/SSH...) IP address
    2. Router device login server service application port
    3. Login user name
    4. Login password for user name
    5. Login way/method(telnet/ftp/sftp/ssh)
    6. Parameters/Arguments
    7. Configuration file name on remote server file system
    8. Configuration file name specified local device directory
    '''
    cmdline = ""
    # Set login way/program
    try:
        cmdline += _args[4]
    except IndexError:
        cmdline += DefaultValues[4]
    # Set server IP address
    try:
        cmdline += " " + _args[0]
    except IndexError:
        cmdline += " " + DefaultValues[0]

    # Set server application port
    try:
        cmdline += " " + _args[1]
    except IndexError:
        cmdline += " " + DefaultValues[1]

    print(cmdline)
    print("System is logging, Please wait a moment")

    try:
        return expect.spawn(cmdline, logfile=sys.stdout)
    except expect.legacy_wexpect.ExceptionPexpect:
        return None





# Translate alias/define variable
def UnfoldMacro(_list, _dict):
    for idx in range(0, _list.__len__(), 1):
        if _list[idx] in _dict:
            _list[idx] = _dict[_list[idx]]

# Define global configuration file parser
CFP = ConfigurationFileParser()

# Define or Alias dictionary
DefineAliasDictionary = dict()

while 1:
    # Read one line content from configuration file of tool.
    line = ft.readline()
    CFP.addCurrLineNunber()

    # If read line is end of file, just break out this while loop handle/process.
    if line == "":
        break

    # If read line is space, read next line right now.
    if line.isspace():
        continue

    # delete begin and tail space or end line char.
    line = line.strip()

    # Check if found comment block start flag
    if CFP.isExistBlockCommentStartFlag():
        blkIdx1 = line.find("*/", 0, len(line))
        if -1 == blkIdx1: # Block comment flag is not found
            continue
        else:
            line = line[blkIdx1+2:]
            #print("after */: "+line)
            CFP.clrBlockCommentStartFlag()
    #else:
    # Find single line comment content
    singleCommentIndex = line.find("//", 0, len(line))
    if 0 == singleCommentIndex: # All line is comment content
        continue
    if -1 != singleCommentIndex: # // found
        blockCommentIndex = line.find("/*", 0, len(line))
        if -1 == blockCommentIndex:
            line = line[:singleCommentIndex]
            # should goto parser line here.
        else:
            if singleCommentIndex < blockCommentIndex:
                line = line[:singleCommentIndex]
                # should goto below while loop here.
    # Check if multiple comment block in this line?
    while 1:
        blkIdx0 = line.find("/*", 0, len(line))
        if -1 != blkIdx0: # Block comment start flag found
            blkIdx1 = line.find("*/", blkIdx0+2, len(line))
            if -1 != blkIdx1: # Block comment end flag found
                line = line[:blkIdx0] + line[blkIdx1+2:]
                #print("Combine line: "+line)
            else: # Not found block comment end flag here and get out this while loop
                CFP.setBlockCommentStartFlag()
                break
        else: # Not found any block comment flag
            break

    if CFP.isExistBlockCommentStartFlag():
        continue

    # Valid line handle/process follow/below
    # If system run to here, that mean that: content of line is valid content.
    if line == "":
        continue

    # Check statement is if define or alias instance.
    list = line.split()
    if list[0] == "#define" or list[0] == "#alias":
        tmpDict = {list[1]: list[2]}
        # Update dictionary here right now.
        DefineAliasDictionary.update(tmpDict)
        #print(DefineAliasDictionary[list[1]])
        continue

    # Check if line content is IP group?
    # If yes, divide it to two part of about begin and end part content.
    list = line.split("-")
    if list.__len__() == 1:
        list = line.split(" to ")

    if list.__len__() > 2:
        print("ERROR: " + str(CFP.getCurrLineNumber()) + \
              "--Please check carefully again, thank you!")

    #print("Before handle define or alias: ", end="")
    #print(list)
    #print("List length is: "+ str(list.__len__()))
    if list.__len__() != 1 and list.__len__() != 2:
        print("ERROR: " + str(CFP.getCurrLineNumber()) + \
              "--Please check carefully again, thank you!")
        continue
    for i in range(0, list.__len__(), 1):
        list[i] = list[i].strip()
        list[i] = list[i].split()
        UnfoldMacro(list[i], DefineAliasDictionary)

    if list.__len__() == 1:
        print(list[0])
        print(list[0][0])
        RouterLogin(list[0])
    elif list.__len__() == 2:
        print(list[0], end=" to ")
        print(list[1])
        ipStartValueList = list[0][0].split(".")
        ipEndValueList = list[1][0].split(".")
        ipStartValue = (int(ipStartValueList[0]) << 24) | \
                       (int(ipStartValueList[1]) << 16) | \
                       (int(ipStartValueList[2]) << 8)  | \
                       (int(ipStartValueList[3]) << 0)
        ipEndValue   = (int(ipEndValueList[0]) << 24) | \
                       (int(ipEndValueList[1]) << 16) | \
                       (int(ipEndValueList[2]) << 8)  | \
                       (int(ipEndValueList[3]) << 0)

        ipMin = min(ipStartValue, ipEndValue)
        ipMax = max(ipStartValue, ipEndValue)

        for ipValue in range(ipMin, ipMax+1, 1):
            ipString = str((ipValue >> 24) & 0xFF) + "." + \
                       str((ipValue >> 16) & 0xFF) + "." + \
                       str((ipValue >>  8) & 0xFF) + "." + \
                       str((ipValue >>  0) & 0xFF)
            #print(ipString)
            list[0][0] = ipString
            RouterLogin(list[0])
    #list = list[0].split()
    # Check IP is if legal
    # three point(".")
    # digital number maximum is 3 * 4
    # Check IP length is legal?
    ipString = list[0][0] #.split(".")
    #print(str(ipTmp) + "length is: " + str(ipTmp.__len__()))
    if 7 <= ipString.__len__() and ipString.__len__() <= 15:
        pass
    else:
        print("ERROR: " + str(CFP.getCurrLineNumber()) + \
              "--IP address length is incorrect")
        print(ipString)
        break

    # Check digital number if legal
    '''
    ipList = list[0].split(".")
    for tmp in ipList:
        if tmp.__len__() < 1 or tmp.__len__() > 3:
            print("ERROR: " + str(CFP.getCurrLineNumber()) + \
                  "--Legal IP address digital length, Please check carefully again, thank you!")
        if not tmp.isdigit():
            print("ERROR: "+str(CFP.getCurrLineNumber()) + \
                  "--Legal IP address, Please check carefully again, thank you!")
    print(ipList)
    '''
    #print(ipValue)
    #print(0xFFFFFFF)
    ##### end of configuration file parser.


def Task0():
    print("Task 0: ", end="")
    print(datetime.datetime.now())

def Task1():
    print("Task 1: ",end="")
    print(datetime.datetime.now())

def TaskScheduler():
    '''

    :return:
    '''
    '''
    
    #创建调度器：BlockingScheduler
    blockScheduler = BlockingScheduler()
    #添加任务,时间间隔2S
    blockScheduler.add_job(Task0, 'interval', seconds=2, id='test_job1')
    #添加任务,时间间隔5S
    blockScheduler.add_job(Task1, 'interval', seconds=3, id='test_job2')
    blockScheduler.add_job(Task1(), )
    blockScheduler.start()
    '''

    '''
            year (int|str) – 4-digit year
            month (int|str) – month (1-12)
            day (int|str) – day of the (1-31)
            week (int|str) – ISO week (1-53)
            day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
            hour (int|str) – hour (0-23)
            minute (int|str) – minute (0-59)
            second (int|str) – second (0-59)

            start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
            end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
            timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

            *    any    Fire on every value
            */a    any    Fire every a values, starting from the minimum
            a-b    any    Fire on any value within the a-b range (a must be smaller than b)
            a-b/c    any    Fire every c values within the a-b range
            xth y    day    Fire on the x -th occurrence of weekday y within the month
            last x    day    Fire on the last occurrence of weekday x within the month
            last    day    Fire on the last day within the month
            x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
        '''
    # Create BackgroundScheduler
    backSchdeduler = BackgroundScheduler()
    backSchdeduler.add_job(Task1, 'cron', second='*',day='9')
    #backSchdeduler.add_job(Task0, 'cron', second=30)
    backSchdeduler.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2000)  # 其他任务是独立的线程执行
        print('sleep!')
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

        print('Exit The Job!')


TaskScheduler()

'''
if __name__ == '__main__':
    print("This is main file and main function")
'''