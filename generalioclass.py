#!/usr/bin/python
#
# Copyright 2008-2014 Jeffrey B. Layton
#




class fstatclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor associated with file)
#   st_mode        (file descriptor protection)
#   st_size        (total size in bytes)
#   

    def __init__(self):
        self.fstatdata = [];
    
    def storefstat(self,data):
        self.fstatdata.append(data);
        #print "a = ",self.fstatdata;

    def getfstat(self):
        return self.fstatdata;

# end class fstat


class statclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor)
#   result         (result of stat)
#   message        (result message string)
#   

    def __init__(self):
        self.statdata = [];
    
    def storestat(self,data):
        self.statdata.append(data);
        #print "a = ",self.statdata;

    def getstat(self):
        return self.statdata;

# end class fstat


class fsyncclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor)
#   result         (result of stat)
#   message        (result message string)
#   

    def __init__(self):
        self.fsyncdata = [];
    
    def storefsync(self,data):
        self.fsyncdata.append(data);
        #print "a = ",self.fsyncdata;

    def getfsync(self):
        return self.fsyncdata;

# end class fsync


class unlinkclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor)
#   result         (result of stat)
#   message        (result message string)
#   

    def __init__(self):
        self.unlinkdata = [];
    
    def storeunlink(self,data):
        self.unlinkdata.append(data);
        #print "a = ",self.unlinkdata;

    def getunlink(self):
        return self.unlinkdata;

# end class unlink


class fcntlclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor)
#   cmd            (fcntl command)
#   result         (result of fcntl - string)
#   message        (result message string)
#   

    def __init__(self):
        self.fcntldata = [];
    
    def storefcntl(self,data):
        self.fcntldata.append(data);
        #print "a = ",self.fcntldata;

    def getfcntl(self):
        return self.fcntldata;

# end class fcntl


class accessclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor)
#   mode           (mode of access command)
#   result         (result of access)
#   message        (result message string)
#   

    def __init__(self):
        self.accessdata = [];
    
    def storeaccess(self,data):
        self.accessdata.append(data);
        #print "a = ",self.accessdata;

    def getaccess(self):
        return self.accesscdata;

# end class access




class getdentsclass:

# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor)
#   readbytes      (mode of access command)
#   

    def __init__(self):
        self.getdentsdata = [];
    
    def storegetdents(self,data):
        self.getdentsdata.append(data);
        #print "a = ",self.getdentsdata;

    def getgetdents(self):
        return self.getdentsdata;

# end class access


