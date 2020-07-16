#!/usr/bin/python
#
# Copyright 2008-2014 Jeffrey B. Layton
#


import sys
try:
   import shlex              # Needed for splitting input lines
except ImportError:
   print "Cannot import shlex module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import pickle               # Needed for mkdir
   pickle_success = 1;
except ImportError:
   print "Cannot import pickle module - this is not needed for this application.";
   print "Continuing to process";
   pickle_success = 0;






# Import strace_analyzer submodules
from strace_processing import *

from strace_func import *

from strace_output import *




# Import class definitions:
from generalioclass import *

from writeclass import *

from readclass import *

from lseekclass import *

from closeclass import *

from openclass import *

from iopsclass import *

from filepointerclass import *

from resultsclass import *

from commandclass import * 




################################################################################################
################################################################################################




if __name__ == '__main__':
    
    
    Open_Filename = [];         # Open_Filename list (of dictionary) of CURRENTLY opened files
                                #    Open_Filename[iloop]["unit"] = unit
                                #    Open_Filename[iloop]["filename"] = filename
    
    # stdin
    temp_dict = {};
    temp_dict["unit"] = 0;
    temp_dict["filename"] = "stdin";
    Open_Filename.append(temp_dict);
    
    # stdout
    temp_dict = {};
    temp_dict["unit"] = 1;
    temp_dict["filename"] = "stdout";
    Open_Filename.append(temp_dict);
    
    # stderr
    temp_dict = {};
    temp_dict["unit"] = 2;
    temp_dict["filename"] = "stderr";
    Open_Filename.append(temp_dict);
    
    
    # Data structure initialization:
    # =============================
    
    CmdCounter = {};            # Command counter dictionary
    Command_List = [];
    
    # Initialization
    # ==============
    OPEN     = "open";         # done
    READ     = "read";         # done
    WRITE    = "write";        # done
    CLOSE    = "close";        # done
    LSEEK    = "lseek";        # done
    LLSEEK   = "llseek";       # done
    LLSEEKU  = "_llseek";      # done
    LSEEK64  = "lseek64";      # done
    STAT     = "stat";         # counter only done
    FSTAT    = "fstat";        # counter only done
    STAT64   = "stat64";       # counter only done
    CHMOD    = "chmod";        # counter only done
    FCHMOD   = "fchmod";       # counter only done
    ACCESS   = "access";       # counter only done
    RENAME   = "rename";       # counter only done
    MKDIR    = "mkdir";        # counter only done
    GETDENTS = "getdents";     # counter only done
    FCNTL    = "fcntl";        # counter only done
    UNLINK   = "unlink";       # counter only done
    FSEEK    = "fseek";        # counter only done
    REWIND   = "rewind";       # counter only done
    FTELL    = "ftell";        # counter only done
    FGETPOS  = "fgetpos";      # counter only done
    FSETPOS  = "fsetpos";      # counter only done
    FCLOSE   = "fclose";       # counter only done
    FSYNC    = "fsync";        # counter only done
    CREAT    = "creat";        # metadata - counter
    READDIR  = "readdir";      # counter only done
    OPENDIR  = "opendir";      # counter only done
    FOPENDIR = "fopendir";     # counter only
    REWINDDIR = "rewinddir";   # counter only done
    SCANDIR  = "scandir";      # counter only done
    SEEKDIR  = "seekdir";      # counter only done
    TELLDIR  = "telldir";      # counter only done
    FLOCK    = "flock";        # counter only done
    LOCKF    = "lockf";        # counter only done
    LSEEK_MASTER = "lseekm";   # done
    LSTAT    = "lstat";        # metadata - counter only
    FSTATAT  = "fstatat";      # metadata - counter only
    FOPEN    = "fopen";        # metadata - counter only
    FDOPEN   = "fdopen";       # metadata - counter only
    FREOPEN  = "freopen";      # metadata - counter only
    REMOVE   = "remove";       # metadata - counter only
    CHOWN    = "chown";        # metadata - counter only
    FCHOWN   = "fchown";       # metadata - counter only
    FCHMODAT = "fchmodat";     # metadata - counter only
    FCHOWNAT = "fchownat";     # metadata - counter only
    FACCESSAT = "faccessat";   # metadata - counter only
    UTIME    = "utime";        # metadata - counter only
    FUTIMES  = "futimes";      # metadata - counter only
    LUTIMES  = "lutimes";      # metadata - counter only
    FUTIMESAT = "futimesat";   # metadata - counter only
    LINK     = "link";         # metadata - counter only
    LINKAT   = "linkat";       # metadata - counter only
    UNLINKAT = "unlinkat";     # metadata - counter only
    SYMLINK  = "symlink";      # metadata - counter only
    SYMLINKAT = "symlinkat";   # metadata - counter only
    RMDIR    = "rmdir";        # metadata - counter only
    MKDIRAT  = "mkdirat";      # metadata - counter only
    GETXATTR = "getxattr";     # metadata - counter only
    LGETXATTR = "lgetxattr";   # metadata - counter only
    FGETXATTR = "fgetxattr";   # metadata - counter only
    SETXATTR = "xetxattr";     # metadata - counter only
    LSETXATTR = "lsetxattr";   # metadata - counter only
    FSETXATTR = "fsetxattr";   # metadata - counter only
    LISTXATTR = "listxattr";   # metadata - counter only
    LLISTXATTR = "llistxattr";  # metadata - counter only
    FLISTXATTR = "flistxattr";  # metadata - counter only
    REMOVEXATTR = "removexattr";  # metadata - counter only
    LREMOVEXATTR = "lremovexattr";  # metadata - counter only
    FREMOVEXATTR = "fremovexattr";  # metadata - counter only
    
    
    # Initialize Command_List:
    Command_List.append(OPEN);
    Command_List.append(READ);
    Command_List.append(WRITE);
    Command_List.append(CLOSE);
    Command_List.append(LSEEK);
    Command_List.append(LLSEEK);
    Command_List.append(LLSEEKU);
    Command_List.append(LSEEK64);
    Command_List.append(STAT);
    Command_List.append(FSTAT);
    Command_List.append(STAT64);
    Command_List.append(CHMOD);
    Command_List.append(FCHMOD);
    Command_List.append(ACCESS);
    Command_List.append(RENAME);
    Command_List.append(MKDIR);
    Command_List.append(GETDENTS);
    Command_List.append(FCNTL);
    Command_List.append(UNLINK);
    Command_List.append(FSEEK);
    Command_List.append(REWIND);
    Command_List.append(FTELL);
    Command_List.append(FGETPOS);
    Command_List.append(FSETPOS);
    Command_List.append(FCLOSE);
    Command_List.append(FSYNC);
    Command_List.append(CREAT);
    Command_List.append(READDIR);
    Command_List.append(OPENDIR);
    Command_List.append(FOPENDIR);
    Command_List.append(REWINDDIR);
    Command_List.append(SCANDIR);
    Command_List.append(SEEKDIR);
    Command_List.append(SEEKDIR);
    Command_List.append(TELLDIR);
    Command_List.append(FLOCK);
    Command_List.append(LOCKF);
    Command_List.append(LSEEK_MASTER);
    Command_List.append(LSTAT);
    Command_List.append(FSTATAT);
    Command_List.append(FOPEN);
    Command_List.append(FDOPEN);
    Command_List.append(FREOPEN);
    Command_List.append(REMOVE);
    Command_List.append(CHOWN);
    Command_List.append(FCHOWN);
    Command_List.append(FCHMODAT);
    Command_List.append(FCHOWNAT);
    Command_List.append(FACCESSAT);
    Command_List.append(UTIME);
    Command_List.append(FUTIMES);
    Command_List.append(LUTIMES);
    Command_List.append(FUTIMESAT);
    Command_List.append(LINK);
    Command_List.append(LINKAT);
    Command_List.append(UNLINKAT);
    Command_List.append(SYMLINK);
    Command_List.append(SYMLINKAT);
    Command_List.append(RMDIR);
    Command_List.append(MKDIRAT);
    Command_List.append(GETXATTR);
    Command_List.append(LGETXATTR);
    Command_List.append(FGETXATTR);
    Command_List.append(SETXATTR);
    Command_List.append(LSETXATTR);
    Command_List.append(FSETXATTR);
    Command_List.append(LISTXATTR);
    Command_List.append(LLISTXATTR);
    Command_List.append(FLISTXATTR);
    Command_List.append(REMOVEXATTR);
    Command_List.append(LREMOVEXATTR);
    Command_List.append(FREMOVEXATTR);
    
    
    
    # Initialize command counters dictionary
    CmdCounter[OPEN] = 0;
    CmdCounter[READ] = 0;
    CmdCounter[WRITE] = 0;
    CmdCounter[CLOSE] = 0;
    CmdCounter[LSEEK] = 0;
    CmdCounter[LLSEEK] = 0;
    CmdCounter[LSEEK64] = 0;
    CmdCounter[LLSEEKU] = 0;
    CmdCounter[LSEEK64] = 0;
    CmdCounter[STAT] = 0;
    CmdCounter[FSTAT] = 0;
    CmdCounter[STAT64] = 0;
    CmdCounter[CHMOD] = 0;
    CmdCounter[FCHMOD] = 0;
    CmdCounter[ACCESS] = 0;
    CmdCounter[RENAME] = 0;
    CmdCounter[MKDIR] = 0;
    CmdCounter[GETDENTS] = 0;
    CmdCounter[FCNTL] = 0;
    CmdCounter[UNLINK] = 0;
    CmdCounter[FSEEK] = 0;
    CmdCounter[REWIND] = 0;
    CmdCounter[FTELL] = 0;
    CmdCounter[FGETPOS] = 0;
    CmdCounter[FSETPOS] = 0;
    CmdCounter[FCLOSE] = 0;
    CmdCounter[FSYNC] = 0;
    CmdCounter[CREAT] = 0
    CmdCounter[READDIR] = 0;
    CmdCounter[OPENDIR] = 0;
    CmdCounter[FOPENDIR] = 0;
    CmdCounter[REWINDDIR] = 0;
    CmdCounter[SCANDIR] = 0;
    CmdCounter[SEEKDIR] = 0;
    CmdCounter[TELLDIR] = 0;
    CmdCounter[FLOCK] = 0;
    CmdCounter[LOCKF] = 0;
    CmdCounter[LSEEK_MASTER] = 0;
    CmdCounter[LSTAT] = 0;
    CmdCounter[FSTATAT] = 0;
    CmdCounter[FOPEN] = 0;
    CmdCounter[FDOPEN] = 0;
    CmdCounter[FREOPEN] = 0;
    CmdCounter[REMOVE] = 0;
    CmdCounter[CHOWN] = 0;
    CmdCounter[FCHOWN] = 0;
    CmdCounter[FCHMODAT] = 0;
    CmdCounter[FCHOWNAT] = 0;
    CmdCounter[FACCESSAT] = 0;
    CmdCounter[UTIME] = 0
    CmdCounter[FUTIMES] = 0;
    CmdCounter[LUTIMES] = 0;
    CmdCounter[FUTIMESAT] = 0;
    CmdCounter[LINK] = 0;
    CmdCounter[LINKAT] = 0;
    CmdCounter[UNLINKAT] = 0;
    CmdCounter[SYMLINK] = 0;
    CmdCounter[SYMLINKAT] = 0;
    CmdCounter[RMDIR] = 0;
    CmdCounter[MKDIRAT] = 0;
    CmdCounter[GETXATTR] = 0;
    CmdCounter[LGETXATTR] = 0;
    CmdCounter[FGETXATTR] = 0;
    CmdCounter[SETXATTR] = 0;
    CmdCounter[LSETXATTR] = 0;
    CmdCounter[FSETXATTR] = 0;
    CmdCounter[LISTXATTR] = 0;
    CmdCounter[LLISTXATTR] = 0;
    CmdCounter[FLISTXATTR] = 0;
    CmdCounter[REMOVEXATTR] = 0;
    CmdCounter[LREMOVEXATTR] = 0;
    CmdCounter[FREMOVEXATTR] = 0;
    

    # Instanitate objects
    Open_obj = openclass();
    IOPS_obj = iopsclass();
    Close_obj = closeclass();
    Write_obj = writeclass();
    Read_obj = readclass();
    Lseek_obj = lseekclass();
    FSTAT_obj = fstatclass();
    STAT_obj = statclass();
    FSYNC_obj = fsyncclass();
    UNLINK_obj = unlinkclass();
    FCNTL_obj = fcntlclass();
    ACCESS_obj = accessclass();
    GETDENTS_obj = getdentsclass();
    Filepointer_obj = Filepointerclass();
    Results_obj = resultsclass();
    Command_obj = commandclass();
    
    
    # Scalar variable initialization
    IOTimeSum = 0.0;          # Summation of all IO time (all syscalls covered)
    IOTimeSum_Write = 0.0;    # Summation of time spend in write();
    IOTimeSum_Read = 0.0;     # Summation of time spent in read()
    IOTime_count = 0;         # Number of IO functions contributing to total IO time
    shortflag = 1;
    datflag = 1;
    
    LineNum = 0;
    NumLines = 0;
    
    # Initialization for forked strace output
    FORKFLAG = 0;
    threadline = [];    # Array to store "forked output"
    
    # ======================
    # Start real processing:
    # ======================
    num_args = len(sys.argv);
    option_flags = sys.argv[1:num_args-1];   # list of command line flags
    
    # "detail" level for output (verbosity)
    VFLAGS = 4;                  # Default to the most verbose
    for arg in option_flags:
        if (arg == "-v"):
            VFLAGS = 1;
        elif (arg == "-vv"):
            VFLAGS = 2;
        elif (arg == "-vvv"):
            VFLAGS = 3;
        elif (arg == "-vvvv"):
            VFLAGS = 4;
        # endif
    # end for
    
    # input file is always last input argument
    input_filename = sys.argv[num_args -1];
    
    # Defaults (for now)
    debug = 0;
    # Open log file:
    STRACE_LOG = open("strace_analyzer.log",'w');
    STRACE_LOG.write("Diagnostic Output: \n");
    STRACE_LOG.write("================== \n");
    STRACE_LOG.write(" \n");
    
    for line in open(input_filename,'r').readlines():
        currentline = shlex.split(line);    # Use shlex to split line based on commas
        
        # search currentline for "<unfinished" - indicates a thread interuption
        if (FORKFLAG == 1):
            icount = 0;
            iunfinish = 0;
            for tmp in currentline:
                if (tmp == "<unfinished"):
                    iunfinish = icount;
                    #print "** Thread interuption: ",currentline;
                # end if
                icount = icount + 1;
            # end for
      
            # search currentline for "resumed>" - indicates completion of strace line after thread interruption
            icount = 0;
            iresume = 0;
            for tmp in currentline:
                if (tmp == "resumed>"):
                    iresume = icount;
                    tmp_cmd = currentline[(iresume-1)];
                    #print "*** Thread resume: ",currentline;
                # end if
                icount = icount + 1;
            # end for
            if (iresume > 0):
                resumeline = currentline[(iresume+1):]
                # search threadline for matching strace function
            # end if
         
            ithread = currentline[0];
            currentline = currentline[1:];
      
            # Search for matching unfinished strace line and reconstruct it
            icount = 0;
            for tmp in threadline:
                if (tmp[0] == ithread):
                    # Get syscall
                    junk1 = tmp[1:];
                    tmp2_cmd = junk1[1].split('(')[0];
                    if (tmp_cmd == tmp2_cmd):
                        # Reconstruct currentline from "unfinished" and "resumed" pieces
                        if (resumeline[0] == ")" ):
                            junk2 = junk1[-1] + resumeline[0];
                            currentline = junk1[0:-1] + [junk2] + resumeline[1:];
                        else:
                            currentline = junk1 + resumeline;
                        # end if
                        del threadline[icount];
                        break;
                    # end if
                #end if
                icount = icount+1
            #end for
        else:
            iunfinish = 0;
        #end if
        
        # Exection time
        sec = currentline[0];
        LineNum=LineNum+1;   # Increment number of lines counter
        
        # Get syscall
        cmd = currentline[1].split('(')[0]
        if (debug > 0):
            junk2 = "   cmd: " + cmd + "   LineNum: " + str(LineNum) + "\n";
            STRACE_LOG.write(junk2);
            junk2 = "   sec = " + str(sec) + "\n";
            STRACE_LOG.write(junk2);
        # end if
        
        # Get elapsed time
        junk1 = currentline[len(currentline)-1];
        junk2 = junk1[1:(len(junk1)-1)];
        elapsed_time = is_number(junk2);
        if (debug > 0):
            junk2 = "   real elapsed time: " + str(elapsed_time) + "\n";
            STRACE_LOG.write(junk2);
        # end if
        
        # Store beginning time
        if (LineNum == 1):
            BeginTime = sec;
            sec_begin = sec;
        # endif
        NumLines = NumLines + 1;   # Counter for number of lines in file
        
        # 
        junk1 = "";
        for item in currentline:
            if (item != ","):
                if (str(item[-1]) == ","):
                    junk1 = junk1 + str(item) + ",";
                else:
                    junk1 = junk1 + str(item) + ",,";
                # end if
            # end if
        # end if
        
        # =========================
        # If ladder to process data
        # =========================
        if (iunfinish > 0):
            # store currentline and move on
            junk1 = [ithread] + currentline[0:(iunfinish-1)];
            
            threadline.append(junk1);
        elif (cmp(cmd, OPEN) == 0):
            if (debug > 0):
                STRACE_LOG.write("   Found an OPEN function call \n");
            # end if
            
            # Increment total IO time and syscall counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # OPEN Processing (put data in OPEN object)
            Open_Processing(currentline,Open_obj,IOPS_obj,Filepointer_obj,Open_Filename,
                            OPEN,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                            CmdCounter);
        elif (cmp(cmd,READ) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a READ function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[READ] = CmdCounter[READ] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            IOTimeSum_Read = IOTimeSum_Read + float(elapsed_time);
            
            # READ Processing (put data in READ object)
            Read_Processing(currentline,Read_obj,IOPS_obj,Filepointer_obj,Open_Filename,
                            READ,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                            CmdCounter);
            
        elif (cmp(cmd,WRITE) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a WRITE function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[WRITE] = CmdCounter[WRITE] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            IOTimeSum_Write = IOTimeSum_Write + float(elapsed_time);
            
            # WRITE Processing (put data in WRITE object)
            Write_Processing(currentline,Write_obj,IOPS_obj,Filepointer_obj,Open_Filename,
                             WRITE,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                             CmdCounter);
            
        elif (cmp(cmd,CLOSE) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a CLOSE function call \n");
                STRACE_LOG.write("      Calling Close_Processing \n");
            # end if
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
             
            # CLOSE Processing (put data in CLOSE object)
            Close_Processing(currentline,Close_obj,IOPS_obj,Filepointer_obj,Open_Filename,
                             CLOSE,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                             CmdCounter);
            
        elif (cmp(cmd,LSEEK) == 0):
            if (debug > 0):
                STRACE_LOG.write("FOUND AN LSEEK!!!\n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LSEEK] += 1;
            CmdCounter[LSEEK_MASTER] = CmdCounter[LSEEK_MASTER] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # LSEEK Processing (put data in LSEEK object)
            Lseek_Processing(currentline, Lseek_obj, IOPS_obj, Filepointer_obj, Open_Filename,
                             LSEEK, elapsed_time, LineNum, sec, BeginTime, debug, STRACE_LOG,
                             CmdCounter);
            
        elif (cmp(cmd,LLSEEK) == 0):
            if (debug > 0):
                STRACE_LOG.write("FOUND AN LLSEEK!!!\n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LLSEEK] = CmdCounter[LLSEEK] + 1;
            CmdCounter[LSEEK_MASTER] = CmdCounter[LSEEK_MASTER] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, LLSEEK);
            filename = result["filename"];
            
            # Update IOPS_Obj (need to grab fd and corresponding filename)
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LLSEEK);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,LLSEEKU) == 0):
            if (debug > 0):
                STRACE_LOG.write("FOUND AN LLSEEKU!!!\n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LLSEEKU] = CmdCounter[LLSEEKU] + 1;
            CmdCounter[LSEEK_MASTER] = CmdCounter[LSEEK_MASTER] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, LLSEEKU);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LLSEEKU);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,LSEEK64) == 0):
            if (debug > 0):
                STRACE_LOG.write("FOUND AN LSEEK64!!!\n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LSEEK64] = CmdCounter[LSEEK64] + 1;
            CmdCounter[LSEEK_MASTER] = CmdCounter[LSEEK_MASTER] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, LSEEK64);
            filename = result["filename"];
            
            # LSEEK Processing (put data in LSEEK object)
            Lseek_Processing(currentline, Lseek_obj, IOPS_obj, Filepointer_obj, Open_Filename,
                             LSEEK64, elapsed_time, LineNum, sec, BeginTime, debug, STRACE_LOG,
                             CmdCounter);
            
        elif (cmp(cmd,STAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("FOUND A STAT!!!\n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[STAT] = CmdCounter[STAT] + 1;
            
            # Increment total IO time and syscall counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # STAT Processing (put data in STAT object)
            STAT_Processing(currentline,STAT_obj,IOPS_obj,STAT,Open_Filename,
                            elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,FSTAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FSTAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FSTAT] = CmdCounter[FSTAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # FSTAT Processing (put data in FSTAT object)
            FSTAT_Processing(currentline,FSTAT_obj,IOPS_obj,FSTAT,Open_Filename,
                             elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,STAT64) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a STAT64 function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[STAT64] = CmdCounter[STAT64] + 1;
            
            # Increment total IO time and syscall counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, STAT64);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(STAT64);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,CHMOD) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a CHMOD function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[CHMOD] = CmdCounter[CHMOD] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(CHMOD);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FCHMOD) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FCHMOD function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FCHMOD] = CmdCounter[FCHMOD] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FCHMOD);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FCHMOD);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,ACCESS) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a ACCESS function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[ACCESS] = CmdCounter[ACCESS] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # ACCESS Processing (put data in ACCESS object)
            ACCESS_Processing(currentline,ACCESS_obj,IOPS_obj,ACCESS,Open_Filename,
                              elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,RENAME) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a RENAME function call \n");
            # endif
         
            # Increment the syscall counter
            CmdCounter[RENAME] = CmdCounter[RENAME] + 1;
             
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from rename() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(RENAME);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,MKDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a MKDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[MKDIR] = CmdCounter[MKDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from mkdir() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(MKDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,GETDENTS) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a GETDENTS function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[GETDENTS] = CmdCounter[GETDENTS] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # GETDENTS Processing (put data in GETDENTS object)
            GETDENTS_Processing(currentline,GETDENTS_obj,IOPS_obj,GETDENTS,Open_Filename,
                                elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,FCNTL) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FCNTL function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FCNTL] = CmdCounter[FCNTL] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # FSYNC Processing (put data in FSYNC object)
            FCNTL_Processing(currentline,FCNTL_obj,IOPS_obj,FCNTL,Open_Filename,
                             elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,UNLINK) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a UNLINK function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[UNLINK] = CmdCounter[UNLINK] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # UNLINK Processing (put data in UNLINK object)
            UNLINK_Processing(currentline,UNLINK_obj,IOPS_obj,UNLINK,Open_Filename,
                              elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,FSEEK) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FSEEK function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FSEEK] = CmdCounter[FSEEK] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get stream from fseek() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FSEEK);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,REWIND) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a REWIND function call \n");
            # end if
          
            # Increment the syscall counter
            CmdCounter[REWIND] = CmdCounter[REWIND] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get stream from rewind() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(REWIND);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FTELL) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FTELL function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FTELL] = CmdCounter[FTELL] + 1;
           
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get stream from ftell() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FTELL);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FGETPOS) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FGETPOS function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FGETPOS] = CmdCounter[FGETPOS] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get stream from fgetpos() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FGETPOS);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FSETPOS) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FSETPOS function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FSETPOS] = CmdCounter[FSETPOS] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get stream from fsetpos() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FSETPOS);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FCLOSE) == 0):
            if (debug > 0):
              STRACE_LOG.write("   ** Found a FCLOSE function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FCLOSE] = CmdCounter[FCLOSE] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get stream from fclose() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FGETPOS);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FSYNC) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FSYNC function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FSYNC] = CmdCounter[FSYNC] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FSYNC);
            filename = result["filename"];
            
            # FSYNC Processing (put data in FSYNC object)
            FSYNC_Processing(currentline,FSYNC_obj,IOPS_obj,FSYNC,Open_Filename,
                             elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter);
            
        elif (cmp(cmd,CREAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a CREAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[CREAT] = CmdCounter[CREAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to create processing function for creat()
            #   Similiar to open()
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(CREAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,READDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a READDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[READDIR] = CmdCounter[READDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, READDIR);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(READDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,OPENDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a OPENDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[OPENDIR] = CmdCounter[OPENDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(READDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FOPENDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FOPENDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FOPENDIR] = CmdCounter[FOPENDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FOPENDIR);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(READDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,REWINDDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a REWINDDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[REWINDDIR] = CmdCounter[REWINDDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(REWINDDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,SCANDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a SCANDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[SCANDIR] = CmdCounter[SCANDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(REWINDDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,SEEKDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a SEEKDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[SEEKDIR] = CmdCounter[SEEKDIR] + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(SEEKDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,TELLDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a TELLDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[TELLDIR] = CmdCounter[TELLDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(TELLDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmd,FLOCK) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FLOCK function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FLOCK] = CmdCounter[FLOCK] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FLOCK);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FLOCK);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LOCKF) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LOCKF function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LOCKF] = CmdCounter[LOCKF] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, LOCKF);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LOCKF);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LSTAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LSTAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LSTAT] = CmdCounter[LSTAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LSTAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FSTATAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FSTATAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FSTATAT] = CmdCounter[FSTATAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FSTATAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FOPEN) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FOPEN function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FOPEN] = CmdCounter[FOPEN] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now (may need a function for this)
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FOPEN);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FDOPEN) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FDOPEN function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FDOPEN] = CmdCounter[FDOPEN] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FDOPEN);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FDOPEN);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FREOPEN) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FREOPEN function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FREOPEN] = CmdCounter[FREOPEN] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now (may need a function for this)
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FREOPEN);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,REMOVE) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a REMOVE function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[REMOVE] = CmdCounter[REMOVE] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(REMOVE);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,CHOWN) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a CHOWN function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[CHOWN] = CmdCounter[CHOWN] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(CHOWN);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FCHOWN) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FCHOWN function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FCHOWN] = CmdCounter[FCHOWN] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FCHOWN);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FCHOWN);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LSTAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LSTAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LSTAT] = CmdCounter[LSTAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now (may need path)
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LSTAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FCHMODAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FCHMODAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FCHMODAT] = CmdCounter[FCHMODAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now (may need path)
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FCHMODAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LSTAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LSTAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LSTAT] = CmdCounter[LSTAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from lstat() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LSTAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FCHOWNAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FCHOWNAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FCHOWNAT] = CmdCounter[FCHOWNAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from fchownat() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FCHOWNAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FACCESSAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FACCESSAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FACCESSAT] = CmdCounter[FACCESSAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from faccessat() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FACCESSAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,UTIME) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a UTIME function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[UTIME] = CmdCounter[UTIME] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get filename from utime() function call
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(UTIME);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FUTIMES) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FUTIMES function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FUTIMES] = CmdCounter[FUTIMES] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FUTIMES);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FUTIMES);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LUTIMES) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LUTIMES function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LUTIMES] = CmdCounter[LUTIMES] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from lutimes() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LUTIMES);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FUTIMESAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FUTIMESAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FUTIMESAT] = CmdCounter[FUTIMESAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from futimesat() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FUTIMESAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LINK) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LSTAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LINK] = CmdCounter[LINK] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LINK);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LINKAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LINKAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LINKAT] = CmdCounter[LINKAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LINKAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,UNLINKAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a UNLINKAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[UNLINKAT] = CmdCounter[UNLINKAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(UNLINKAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,SYMLINK) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a SYMLINK function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[SYMLINK] = CmdCounter[SYMLINK] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(SYMLINK);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,SYMLINKAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a SYMLINKAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[SYMLINKAT] = CmdCounter[SYMLINKAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(SYMLINKAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,RMDIR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a RMDIR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[RMDIR] = CmdCounter[RMDIR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(RMDIR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,MKDIRAT) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a MKDIRAT function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[MKDIRAT] = CmdCounter[MKDIRAT] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(MKDIRAT);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,GETXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a GETXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[GETXATTR] = CmdCounter[GETXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from getxattr() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(GETXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LGETXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LGETXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LGETXATTR] = CmdCounter[LGETXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from getxattr() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LGETXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FGETXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FGETXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FGETXATTR] = CmdCounter[FGETXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FGETXATTR);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FGETXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,SETXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a SETXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[SETXATTR] = CmdCounter[SETXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(SETXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LSETXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LSETXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LSETXATTR] = CmdCounter[LSETXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LSETXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FSETXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FSETXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FSETXATTR] = CmdCounter[FSETXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FSETXATTR);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FSETXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LISTXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LISTXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LISTXATTR] = CmdCounter[LISTXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LISTXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LLISTXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LLISTXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LLISTXATTR] = CmdCounter[LLISTXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from chmod() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LLISTXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FLISTXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FLISTXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FLISTXATTR] = CmdCounter[FLISTXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, LLSEEKU);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FLISTXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,REMOVEXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a REMOVEXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[REMOVEXATTR] = CmdCounter[REMOVEXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(REMOVEXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,LREMOVEXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a LREMOVEXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[LREMOVEXATTR] = CmdCounter[LREMOVEXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Use blank filename for now - need to get path from lremovexattr() syscall
            filename = "";
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(LREMOVEXATTR);
            IOPS_obj.storeiops(temp_list);
            
        elif (cmp(cmp,FREMOVEXATTR) == 0):
            if (debug > 0):
                STRACE_LOG.write("   ** Found a FREMOVEXATTR function call \n");
            # end if
            
            # Increment the syscall counter
            CmdCounter[FREMOVEXATTR] = CmdCounter[FREMOVEXATTR] + 1;
            
            # Increment total IO time and command counters
            IOTimeSum = IOTimeSum + float(elapsed_time);
            IOTime_count = IOTime_count + 1;
            
            # Get unit and filename
            result = get_fd_and_filename(currentline, Open_Filename, STRACE_LOG, LineNum, FREMOVEXATTR);
            filename = result["filename"];
            
            # Update IOPS_Obj
            filename = "";
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(FREMOVEXATTR);
            IOPS_obj.storeiops(temp_list);
            
        # end if
    # end for loop
    
    EndTime = sec;   # Time of end of run (last reported strace function call)
    
    print " ";
    print "Number of open files at end of analysis",commify3(len(Open_Filename));
    iloop = 0;
    for temp_dict in Open_Filename:
        iloop = iloop + 1;
        junk1 = temp_dict["unit"];
        if (junk1 < 10):
            junk2 = "  " + str(junk1);
        elif ((junk1 >= 10) and (junk1 < 100)):
            junk2 = " " + str(junk1);
        # end if
        if (iloop < 10):
            junk3 = "  " + str(iloop);
        elif ((iloop >= 10) and (iloop < 100)):
            junk3 = " " + str(iloop);
        # end if
        print junk3," unit: ",junk2," filename: ",temp_dict["filename"]
    # end for
    print "The application is relying on the OS to close these files when it finishes.";
    
    # ============================================================================
    # ============================================================================
    # ============================   Output Summary   ============================
    # ============================================================================
    # ============================================================================
    
    print " ";
    print " ";
    print "Analysis Output";
    print "===============";
    print " "
    print "Number of Lines in strace file: ",commify3(NumLines);
    print " ";
    
    # HTML Report initialization
    #    Write all data files to subdirectory called HTML_REPORT
    #    File is report.html
    dirname ="./HTML_REPORT";
    if not os.path.exists(dirname):
        os.makedirs(dirname);
    # end if
    html_filename = dirname + '/report.html';
    print "html_filename = ",html_filename;
    f = open(html_filename, 'w')
    
    # Print HTML Report header
    output_str = "<H2>\n";
    output_str = output_str + "Strace Report for file: " + input_filename + " \n";
    output_str = output_str + "</H2>\n";
    output_str = output_str + " \n";
    f.write(output_str);
    
    # HTML - print out header information
    output_str = "<H3>\n";
    output_str = output_str + "Introduction \n";
    output_str = output_str + "</H3> \n";
    output_str = output_str + " \n";
    output_str = output_str + "<P>\n";
    output_str = output_str + "This report summarizes the statistics in analyzing the strace results for a file\n";
    output_str = output_str + "This output allows you examine what the application is doing from an I/O perspective.\n";
    output_str = output_str + "This report is broken into several sections. In each section a summary of the \n";
    output_str = output_str + "results is presented and a statistical analysis is made. \n";
    output_str = output_str + "</P>\n";
    output_str = output_str + " \n";
    f.write(output_str);
   
    output_str = "<P> \n";
    output_str = output_str + "Below are hyperlinks to various sections within the report. \n";
    output_str = output_str + "<BR> \n";
    output_str = output_str + "<OL> \n";
    output_str = output_str + "   <LI><a href=\"#time_stats\">Time Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#IO_func_count\">IO Function Count</a> \n";
    output_str = output_str + "   <LI><a href=\"#write_stat\">Write Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#read_stat\">Read Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#close_stat\">Close Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#open_stat\">Open Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#lseek_stat\">Lseek Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#iops_stat\">IOPS Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#per_file_stat\">Per File Statistics</a> \n";
    output_str = output_str + "   <LI><a href=\"#perf_section\">Performance Summary</a> \n";
    if (VFLAGS > 2):
        output_str = output_str + "   <LI><a href=\"#plots_section\">Aggregate Plots</a> \n";
        output_str = output_str + "   <LI><a href=\"#individual_file_perf\">Individual File Performance</a> \n";
        output_str = output_str + "   <LI><a href=\"#file_pointer\">File Pointer Plots</a> \n";
    # end if
    output_str = output_str + "</OL> \n";
    output_str = output_str + "</P> \n";
    output_str = output_str + " \n";
    f.write(output_str);
    
    # Initialize file sizes (used for summary of read/write functions)
    FileSizes = [];
    FileSizes.append(1000);            # 1KB
    FileSizes.append(4000);            # 4KB
    FileSizes.append(8000);            # 8KB
    FileSizes.append(16000);           # 16KB
    FileSizes.append(32000);           # 32KB
    FileSizes.append(64000);           # 64KB
    FileSizes.append(128000);          # 128KB
    FileSizes.append(256000);          # 256KB
    FileSizes.append(512000);          # 512KB
    FileSizes.append(1000000);         # 1MB
    FileSizes.append(10000000);        # 10MB
    FileSizes.append(100000000);       # 100MB
    FileSizes.append(1000000000);      # 1GB
    FileSizes.append(10000000000);     # 10GB
    FileSizes.append(100000000000);    # 100GB
    FileSizes.append(1000000000000);   # 1TB
    FileSizes.append(10000000000000);  # 10TB
    
    # Initialize File size counters
    FileSizeCounter = {};
    FileSizeCounter[1000] = 0;
    FileSizeCounter[4000] = 0;
    FileSizeCounter[8000] = 0;
    FileSizeCounter[16000] = 0;
    FileSizeCounter[32000] = 0;
    FileSizeCounter[64000] = 0;
    FileSizeCounter[128000] = 0;
    FileSizeCounter[256000] = 0;
    FileSizeCounter[512000] = 0;
    FileSizeCounter[1000000] = 0;
    FileSizeCounter[10000000] = 0;
    FileSizeCounter[100000000] = 0;
    FileSizeCounter[1000000000] = 0;
    FileSizeCounter[10000000000] = 0;
    FileSizeCounter[100000000000] = 0;
    FileSizeCounter[1000000000000] = 0;
    FileSizeCounter[10000000000000] = 0;
    
    # currentfigure initialization
    currentfigure = 0;
    
    # ==================
    # ==================
    # 1. Time statistics
    # ==================
    # ==================
    
    # Elapsed Time for run length
    print " ";
    print "----------------";
    print "-- Time Stats --";
    print "----------------";
    
    TimeDelta = (float(EndTime) - float(BeginTime));
    junk1 = "%.4f" % TimeDelta;
    print "Elapsed Time for run: ",commify3(junk1)," (secs)";
    junk2 = "%.4f" % IOTimeSum;
    print "Total IO Time: ",commify3(junk2)," (secs) ";
    
    junk1 = "%.6f" % float((IOTimeSum/TimeDelta)*100.0);
    print "   Percentage of Total Time = ",junk1,"%" ;
    junk3 = "%.4f" % IOTimeSum_Read;
    print "   Total IO Time for read(): ",commify3(junk3)," (secs)";
    junk4 = "%.4f" % IOTimeSum_Write;
    print "   Total IO TIme for write(): ",commify3(junk4)," (secs)";
    junk1 = (float(IOTime_count)/float(NumLines))*100.0;
    junk2 = "%.4f" % junk1;
    print "Total number of IO Functions: ",commify3(IOTime_count)," (",commify3(junk2)," % of total) ";
    
    # HTML output
    output_str = " \n";
    output_str = output_str + "<hr /> \n";
    output_str = output_str + "<H3>\n";
    output_str = output_str + "1. <a id=\"time_stats\">Time Statistics</a> \n";
    output_str = output_str + "</H3 \n";
    output_str = output_str + " \n";
    f.write(output_str);
    
    output_str = "<P> \n";
    output_str = output_str + "The following results are the overall time statistics for all of the files. <BR><BR>\n";
    junk1 = "%.4f" % TimeDelta;
    output_str = output_str + "<strong>Elapsed Time for run</strong>: " + commify3(junk1) + " seconds &nbsp \n";
    output_str = output_str + "<BR> \n";
    junk2 = "%.4f" % IOTimeSum;
    output_str = output_str + "<strong>Total IO Time:</strong> " + commify3(junk2) + " seconds &nbsp \n";
    output_str = output_str + "<BR> \n";
    junk1 = "%.6f" % float((IOTimeSum/TimeDelta)*100.0);
    output_str = output_str + "<strong>&nbsp Percentage of Total Run Time </strong> = " + junk1 + " % \n";
    output_str = output_str + "<BR> \n";
    junk2 = commify3(IOTime_count);
    output_str = output_str + "<strong>Total number of IO Functions:</strong> " + junk2 + " &nbsp \n";
    output_str = output_str + "<BR> \n";
    junk3 = "%.4f" % IOTimeSum_Read;
    output_str = output_str + "<Strong>Total IO Time for read():</strong> " + commify3(junk3) + " seconds &nbsp \n";
    output_str = output_str + "<BR> \n";
    junk4 = "%.4f" % IOTimeSum_Write;
    junk4a = commify3(junk4);
    output_str = output_str + "<Strong>Total IO Time for write():</strong> " + junk4a + " seconds &nbsp \n";

    output_str = output_str + "<BR> \n";
    output_str = output_str + "</P> \n";
    output_str = output_str + "<BR>";
    f.write(output_str);
    
    # ========================
    # ========================
    # 2. IO Command statistics
    # ========================
    # ========================
    print " ";
    print " ";
    print "---------------------- ";
    print "-- IO Command Count -- ";
    print "---------------------- ";
    print " ";
    print "Command                   Count";
    print "===============================";
    
    # HTML report output (opt of section)
    output_str = " \n";
    output_str = output_str + "<hr /> \n";
    output_str = output_str + "<H3> \n"
    output_str = output_str + "2. <a id=\"IO_func_count\">I/O Function Count</a> \n";
    output_str = output_str + "</H3> \n";
    output_str = output_str + " \n";
    output_str = output_str + "<P> \n";
    output_str = output_str + "This section lists the I/O function command count (how many times a particular \n";
    output_str = output_str + "I/O function is called). Table 1 below contains this information \n";
    output_str = output_str + "<BR><BR><center><strong>Table 1 - I/O Function Command Count</strong><BR><BR> \n";
    output_str = output_str + "<table border =" + "\"1\" " + "> \n";
    output_str = output_str + "   <tr> \n";
    output_str = output_str + "      <th><font size=\"-2\">&nbsp Command &nbsp </font></th> \n";
    output_str = output_str + "      <th><font size=\"-2\">&nbsp Count &nbsp </font></th> \n";
    f.write(output_str);
    
    for item in CmdCounter:
        junk1 = str(CmdCounter[item]);
        junk1a = commify3(junk1);
        junk2 = len(item);
        junk3 = junk1a.rjust((30-junk2)," ");
        # print "CmdCounter[item]: ",CmdCounter[item];
        if (CmdCounter[item] > 0):
            print item,junk3;
            # HTML:
            junk0 = "   <tr> \n";
            f.write(junk0);
            junk0 = "      <td><font size=\"-2\"><strong>" + str(item) + "</strong></font></td> \n";
            f.write(junk0);
            junk1 = commify3(CmdCounter[item]);
            junk0 = "      <td align=\"right\"><font size=\"-2\"><strong>" + junk1 + "</strong></font></td> \n";
            f.write(junk0);
            junk0 = "   </tr> \n";
            f.write(junk0);
        # end if
    # end for loop   
    print " ";
    print " ";
   
    # HTML:
    output_str = "</table></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    # ===================
    # ===================
    # 3. Write statistics
    # ===================
    # ===================
    
    if (CmdCounter[WRITE] > 0):
        currentfigure2 = Write_obj.write_statistics(f, dirname, FileSizes, FileSizeCounter, BeginTime,
                                                    EndTime, currentfigure, VFLAGS, matplotlib_var, numpy_var,
                                                   CmdCounter, WRITE);
        currentfigure = currentfigure2;
    # end if
    
    # ==================
    # ==================
    # 4. Read statistics
    # ==================
    # ==================
    
    if (CmdCounter[READ] > 0):
        FileSizeCounter = {};
        FileSizeCounter[1000] = 0;
        FileSizeCounter[4000] = 0;
        FileSizeCounter[8000] = 0;
        FileSizeCounter[16000] = 0;
        FileSizeCounter[32000] = 0;
        FileSizeCounter[64000] = 0;
        FileSizeCounter[128000] = 0;
        FileSizeCounter[256000] = 0;
        FileSizeCounter[512000] = 0;
        FileSizeCounter[1000000] = 0;
        FileSizeCounter[10000000] = 0;
        FileSizeCounter[100000000] = 0;
        FileSizeCounter[1000000000] = 0;
        FileSizeCounter[10000000000] = 0;
        FileSizeCounter[100000000000] = 0;
        FileSizeCounter[1000000000000] = 0;
        FileSizeCounter[10000000000000] = 0;
        currentfigure2 = Read_obj.read_statistics(f, dirname, FileSizes, FileSizeCounter, BeginTime,
                                                  EndTime, currentfigure, VFLAGS, matplotlib_var, numpy_var,
                                                  CmdCounter, READ);
        currentfigure = currentfigure2;
    # end if
    
    # ===================
    # ===================
    # 5. Close statistics
    # ===================
    # ===================
    if (CmdCounter[CLOSE] > 0):
        currentfigure2 = Close_obj.close_statistics(f, dirname, FileSizes, FileSizeCounter, BeginTime,
                                                    EndTime, currentfigure, VFLAGS, matplotlib_var, numpy_var,
                                                    CmdCounter, CLOSE);
        currentfigure = currentfigure2;
    # end if
    
    # ==================
    # ==================
    # 6. Open statistics
    # ==================
    # ==================
    if (CmdCounter[OPEN] > 0):
        currentfigure2 = Open_obj.open_statistics(f, dirname, FileSizes, FileSizeCounter, BeginTime,
                                                  EndTime, currentfigure, VFLAGS, matplotlib_var, numpy_var,
                                                  CmdCounter, OPEN);
        currentfigure = currentfigure2;
    # end if
    
    # =================================
    # =================================
    # 7. lseek unit activity statistics
    # =================================
    # =================================
    if (CmdCounter[LSEEK_MASTER] > 0):
        Lseek_obj.lseek_statistics(f, CmdCounter, LSEEK, VFLAGS, BeginTime, EndTime);
    # end if
    
    # ==================
    # ==================
    # 8. IOPS statistics
    # ==================
    # ==================
    currentfigure2 = IOPS_obj.iops_output_stats(f, CmdCounter, BeginTime, EndTime, WRITE, READ,
                                                VFLAGS, dirname, currentfigure);
    currentfigure = currentfigure2;
    
    # ======================
    # ======================
    # 9. Per File Statistics
    # ======================
    # ======================
    # Write Summary on a per unit basis
    if ( CmdCounter[OPEN] > 0):
        Per_File_Stats(f, Write_obj, Read_obj, IOPS_obj, CmdCounter, WRITE, READ, dirname);
    # end if
    
    # =======================
    # =======================
    # 10. Performance Section 
    # =======================
    # =======================
    currentfigure2 = Performance_Output(f, currentfigure, VFLAGS, Write_obj, Read_obj, IOPS_obj, BeginTime, EndTime,
                                       input_filename);
    currentfigure = currentfigure2;
    
    #
    # ===================
    # ===================
    # 11. Aggregate Plots
    # ===================
    # ===================
    #  
    if (VFLAGS > 2):
        currentfigure2 = Aggregate_Plots(f, currentfigure, input_filename, BeginTime, EndTime, 
                                         Write_obj, Read_obj, IOPS_obj);
        currentfigure = currentfigure2;
    # end if
    
    #
    # =========================
    # =========================
    # 12. Individual file plots
    # =========================
    # =========================
    #
    if (VFLAGS > 2):
       currentfigure2 = Individual_plots(f, VFLAGS, currentfigure, BeginTime, EndTime, 
                                         input_filename, Write_obj, Read_obj, Open_obj, IOPS_obj,
                                         READ, WRITE);
       currentfigure = currentfigure2;
    # end if
    
    #
    # ======================
    # ======================
    # 13. File Pointer Plots
    # ======================
    # ======================
    #
    # output_str = output_str + "   <LI><a href=\"#file_pointer\">File Pointer Plots</a> \n";
    if (VFLAGS > 2):
        Filepointer_obj.filepointer_output(Open_obj, f, dirname, BeginTime, EndTime, currentfigure,
                                           VFLAGS, matplotlib_var, numpy_var);
    # end if
    
    
    #
    # Put Results summary in object
    #
    Results_obj.resultsdata["IOTimeSum"] = IOTimeSum;
    Results_obj.resultsdata["IOTime_count"] = IOTime_count;
    Results_obj.resultsdata["NumLines"] = NumLines;
    Results_obj.resultsdata["IOPS_Total_Final"] = IOPS_obj.IOPS_Total_Final;
    Results_obj.resultsdata["IOPS_Read_Final"] = IOPS_obj.IOPS_Total_Final;
    Results_obj.resultsdata["IOPS_Write_Final"] = IOPS_obj.IOPS_Total_Final;
    
    Results_obj.resultsdata["IOPS_Write_peak"] = IOPS_obj.IOPS_Write_peak;
    Results_obj.resultsdata["IOPS_Write_peak_time"] = IOPS_obj.IOPS_Write_peak_time;
    Results_obj.resultsdata["IOPS_Read_peak"] = IOPS_obj.IOPS_Read_peak;
    Results_obj.resultsdata["IOPS_Read_peak_time"] = IOPS_obj.IOPS_Read_peak_time;
    Results_obj.resultsdata["IOPS_Total_peak"] = IOPS_obj.IOPS_Total_peak;
    Results_obj.resultsdata["IOPS_Total_peak_time"] = IOPS_obj.IOPS_Total_peak_time;
    
    Results_obj.resultsdata["BeginTime"] = BeginTime;
    Results_obj.resultsdata["EndTime"] = EndTime;
    Results_obj.resultsdata["WriteSmall"] = Write_obj.WriteSmall;
    Results_obj.resultsdata["WriteLarge"] = Write_obj.WriteLarge;
    Results_obj.resultsdata["ReadSmall"] = Read_obj.ReadSmall;
    Results_obj.resultsdata["ReadLarge"] = Read_obj.ReadLarge;
    
    #
    # Put command list into command class for pickling
    #
    Command_obj.commanddata["Command_List"] = Command_List;
    Command_obj.commanddata["CmdCounter"] = CmdCounter;
    
    # ================================================================
    # Take the data structures and pickle them so they can be used in
    #   in other applications and in the MPI IO strace analyzer
    # ================================================================
    #
    # Start of Pickling
    #
    if (pickle_success > 0):
        
        pickle_file = open('file.pickle', 'w');
        
        pickle.dump(Results_obj, pickle_file);
        pickle.dump(Command_obj, pickle_file);
        pickle.dump(Open_obj, pickle_file);
        pickle.dump(IOPS_obj, pickle_file);
        pickle.dump(Close_obj, pickle_file);
        pickle.dump(Write_obj, pickle_file);
        pickle.dump(Read_obj, pickle_file);
        pickle.dump(Lseek_obj, pickle_file);
        pickle.dump(FSTAT_obj, pickle_file);
        pickle.dump(STAT_obj, pickle_file);
        pickle.dump(FSYNC_obj, pickle_file);
        pickle.dump(UNLINK_obj, pickle_file);
        pickle.dump(FCNTL_obj, pickle_file);
        pickle.dump(ACCESS_obj, pickle_file);
        pickle.dump(GETDENTS_obj, pickle_file);
        pickle.dump(Filepointer_obj, pickle_file);
        
    # end if

    print " ";
    print " ";




# End of main
