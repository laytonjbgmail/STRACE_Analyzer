

try:
   from math import floor    # Needed for floor function
except ImportError:
   print "Cannot import math module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

from strace_func import *



# =========
# =========
# Functions
# =========
# =========



#
# Process Open() syscalls filling data structures
# 
def Open_Processing(currentline,Open_obj,IOPS_obj,Filepointer_obj,Open_Filename,
                    OPEN,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                    CmdCounter):
   # Syscall:
   #   int open(const char *path, int oflag, ...  );
   # Sample input line:
   #   1252621029.776202 open("/etc/ld.so.cache", O_RDONLY) = 3 <0.000017>
   #   1252621029.815635 open("junk.out", O_RDWR|O_CREAT|O_LARGEFILE, 0666) = 6 <0.000042>
   # Sample split line:
   #   currentline:  ['1252621029.776202', 'open(/etc/ld.so.cache,', 'O_RDONLY)', '=', '3', '<0.000017>']
   #   currentline:  ['1252621029.815635', 'open(junk.out,', 'O_RDWR|O_CREAT|O_LARGEFILE,', '0666)', '=', '6', '<0.000042>']
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # Open_obj             # Open class object
   # IOPS_obj             # IOPS class object
   # OPEN                 # Keyword for open syscall
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # Local temporary variables 
   temp_dict = {};             # local temporary dictionary
   temp_list = [];             # local temporary list
   
   # Get file name   [ Note: currentline[1] containst the filename after "(" ]
   junk1 = currentline[1].split('(')[1];
   filename = junk1[0:len(junk1)-1];

   # Get file descriptor (unit)  [ it is after "=" in split line ]
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # end try
   unit = int(currentline[i+1]);    # file descriptor
   
   # If unit is positive (i.e. it was successfully opened) then start processing
   #   information about open function and populate data structures
   if (unit > 0):
      if (debug > 0):
         junk1 = "      filename: " + filename.lower() + "  file descriptor: " + str(unit) + " \n";
         STRACE_LOG.write(junk1);
      #end if
      
      # Get File open options (oflags and omode) from split input string
      ibegin = 2;
      #    Find index that has an '=' then grab the options after the "=" sign
      try:
         ifinal = currentline.index("=");
         islice = range(ibegin,ifinal);
         ilength = ifinal - ibegin;
         if (ilength > 1):
            omode = currentline[ifinal-1];
            oflags = currentline[ibegin];
            # remove last character of each:
            omode = omode[0:len(omode)-1];
            oflags = oflags[0:len(oflags)-1];
         else:
            omode = "";
            oflags = currentline[ibegin];
            oflags = oflags[0:len(oflags)-1];
         # end "if (ilength > 1):"
      except ValueError:
         ifinal = -1;   # no match
         STRACE_LOG.write("*** Problem with indexing for open mode flags \n");
         junk1 = "    Current Line in strace file: "+str(LineNum)+" \n";
         STRACE_LOG.write(junk1);
      # end "try"
      
      # Write omode and oflags to log file if debugging
      if (debug > 0):
         junk1 = "      oflags: " + omode + "\n";
         STRACE_LOG.write(junk1);
         junk1 = "      mode: " + oflags + "\n";
         STRACE_LOG.write(junk1);
      # end if

      # Increment command counter for OPEN command
      CmdCounter[OPEN] = CmdCounter[OPEN] + 1;
      
      # Find if file is already open
      i = -1;
      for item in Open_Filename:
         junk1 = item["filename"];
         if (junk1.lower() == filename.lower() ):
            record = item;
            i = 1;
            break
         # end if
      # end for loop
      
      if (i > 0):
         # File already exists in data structures - throw a message to the log and continue
         junk1 = "*** Warning: Filename " + filename.lower() + " for fd " + str(unit) + " already exists \n";
         STRACE_LOG.write(junk1);
         junk1 = "    filename: " + str( record["filename"] ) + "\n";
         STRACE_LOG.write(junk1);
      else:
         # File is not currently open - write a message to the log and continue
         junk1 = "*** Filename " + filename.lower() + " for fd " + str(unit) + " does not exist in Open_Filename \n";
         STRACE_LOG.write(junk1);
         
         # Update data structure for currently opened files
         temp_dict = {};
         temp_dict["unit"] = int(unit);
         temp_dict["filename"] = filename.lower();
         Open_Filename.append(temp_dict);
         junk1 = "*** Filename " + filename.lower() + " for unit " + str(unit) + " added to Open_Filename dictionary \n";
         STRACE_LOG.write(junk1);
         
         # Add data to Open Object
         temp_list = [];
         temp_list.append(LineNum);
         temp_list.append(sec);
         temp_list.append(filename.lower());
         temp_list.append(int(unit));
         temp_list.append(elapsed_time);
         Open_obj.storeopen(temp_list);
         
         # Update IOPS Object
         temp_list = [];
         temp = int(floor(float(sec) - float(BeginTime)) + 1);
         temp_list.append(LineNum);
         temp_list.append(filename.lower());
         temp_list.append(sec);
         temp_list.append(temp);
         temp_list.append(OPEN);
         IOPS_obj.storeiops(temp_list);
         
         # Add data to File Pointer object (filepointer)
         #  Filepointer = [];           # File pointer for a specific file (list of dictionaries)
         #                              #    Filepointer[iloop]["sec"] = sec
         #                              #    Filepointer[iloop]["unit"] = file descriptor
         #                              #    Filepointer[iloop]["filename"] = filename
         #                              #    Filepointer[iloop]["pointer"] = pointer value
         #                              #    Filepointer[iloop]["type"] = type of call
         temp_dict = {};
         temp_dict["sec"] = sec;
         temp_dict["unit"] = int(unit);
         temp_dict["filename"] = filename.lower();
         temp_dict["pointer"] = 0;
         temp_dict["type"] = OPEN;
         Filepointer_obj.storefilepointer(temp_dict);
      # end if
   else:
      if (debug > 0):
         junk1 = "      Open did not succeed on fd: " + str(unit) + " \n";
         junk1 = junk1 + "         filename = ",filename.lower() + " \n";
         junk1 = junk1 + "         Not adding file descriptor and filename to statistics \n";
         STRACE_LOG.write(junk1);
      # end if
   # End of if
   
# End of Open_Processing





#
# Process Close() syscalls filling data structures
#
def Close_Processing(currentline,Close_obj,IOPS_obj,Filepointer_obj,Open_Filename,
                     CLOSE,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                     CmdCounter):
   
   # Syscall:
   #    int close(int fd);
   # Sample strace line:
   #    1252621030.301696 close(0)              = 0 <0.000011>
   # Sample split line:
   #     ['1252621030.301696', 'close(3)', '=', '0', '<0.000011>']
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # Close_obj            # Close object
   # IOPS_obj             # IOPS Object
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # CLOSE;               # Keyword for close syscall
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # temporary variables
   temp_dict = {};
   temp_list = [];
   
   if (debug > 0):
      STRACE_LOG.write("   *** In close_processing routine\n");
   # end if
   
   # Check if close() function was successful
   #    Find success by looking for "=" sign (index) and using the next index
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # end try
   junk1 = currentline[i+1];
   success = int(junk1);
   
   if (success == 0):
      # Close was successful
      
      # Increment the syscall counter
      CmdCounter[CLOSE] = CmdCounter[CLOSE] + 1;
      
      # Find unit (file descriptor)
      junk1 = currentline[1];
      junk2 = junk1.index("(");
      try:
         junk3 = junk1.index(")");
      except ValueError:
         junk3 = len(junk1);
      #end try
      unit = int(junk1[junk2+1:junk3]);    # file descriptor
      
      # Find corresponding file in Open_Filename data structure and erase it
      #    because the file is closed
      #    Check if filename exists in Open_Filename
      if (unit > 2):                 # change so that we can't close stdin, stdout, stderr
         
         # Search Open_Filename list of dictionaries for open file match
         i = -1;
         j = -1;
         for item in Open_Filename:
            j = j+1;
            if ( int(item["unit"]) == int(unit) ):
               i = 1;
               filename = item["filename"];
               break
            # end if
         # end for loop
         
         # Note: We only look for positive units since the program shouldn't try
         #   to close stdin or stdout (or stderr).
         if (i > 0):
            # File exists (it is open)
            
            # Add data to Close Object
            temp_list = [];
            temp_list.append(LineNum);
            temp_list.append(sec);
            temp_list.append(filename);
            temp_list.append(unit);
            temp_list.append(float(elapsed_time));
            Close_obj.storeclose(temp_list);
            
            if (debug > 0):
               junk1 = "         unit = " + str(unit) + " filename: " + filename.lower() + " \n"
               STRACE_LOG.write(junk1);
               junk1 = "         Elapsed time: " + str(elapsed_time) + " \n";
               STRACE_LOG.write(junk1);
            # end if
            
            # Remove element corresponding to close unit in Open_Filename data structure
            #   This means that the file is closed
            del Open_Filename[j];
            
            # Insert IOPS data into IOPS object
            temp_list = [];
            temp = int(floor(float(sec) - float(BeginTime)) + 1);
            temp_list.append(LineNum);
            temp_list.append(filename.lower());
            temp_list.append(sec);
            temp_list.append(temp);
            temp_list.append(CLOSE);
            IOPS_obj.storeiops(temp_list);
            
            # Add data to File Pointer object (filepointer)
            #  Filepointer = [];           # File pointer for a specific file (list of dictionaries)
            #                              #    Filepointer[iloop]["sec"] = sec
            #                              #    Filepointer[iloop]["unit"] = file descriptor
            #                              #    Filepointer[iloop]["filename"] = filename
            #                              #    Filepointer[iloop]["pointer"] = pointer value
            #                              #    Filepointer[iloop]["type"] = type of call
            temp_dict = {};
            temp_dict["sec"] = sec;
            temp_dict["unit"] = int(unit);
            temp_dict["filename"] = filename.lower();
            temp_dict["pointer"] = 0;
            temp_dict["type"] = CLOSE;
            Filepointer_obj.storefilepointer(temp_dict);
         else:
            # File does not exist in Open_Filename list - write out data to log and continue
            
            junk1 = "In close_processing: cannot find unit in Open_Filename data structure \n";
            STRACE_LOG.write(junk1);
            junk1 = "   Line Number of strace file = "+str(LineNum)+" \n";
            STRACE_LOG.write(junk1);
            
            # Reconstruct actual line in strace output and print it to log
            lineOutput = "";
            for tmp in currentline:
               lineOutput = lineOutput + " " + tmp;
            # end for
            lineOutput = lineOutput + "\n";
            junk2 = "   (" + str(LineNum) + ")   " + lineOutput ;
            STRACE_LOG.write(junk2);
            
            # print out file descriptor (unit) to log
            junk1 = "   unit: " + str(unit) + " \n";
            STRACE_LOG.write(junk1);
            
            # print out current Open_Filename list to log
            junk2 = "   Current Open_Filename list \n";
            STRACE_LOG.write(junk2);
            for item in Open_Filename:
               junk1 = "      " + str(item) + "\n";
               STRACE_LOG.write(junk1);
            # end for
            
         # end if (i > 0):
      # end if (unit > 0):
   # end if (success == 0):
# End Close_processing




#
# Process Write() syscalls filling data structures
#                    
def Write_Processing(currentline, Write_obj, IOPS_obj, Filepointer_obj, Open_Filename,
                     WRITE, elapsed_time, LineNum, sec, BeginTime, debug, STRACE_LOG,
                     CmdCounter):
   # Syscall:
   #    ssize_t write(int fildes, const void *buf, size_t nbyte);
   #       where:  In the absence of errors, or if error detection is not performed,
   #               the write() function shall return zero and have no other results. 
   # Sample strace line:
   #   1252621029.820728 write(3, "@\37\0\0\0\0\0\0\0\0\364?\0\0\0\0\0\0\4@\0\0\0\0\0\0\16"..., 8008) = 8008 <0.000058>
   # Sample split line:
   #   ['1252621029.820728', 'write(3,', '@\\37\\0\\0\\0\\0\\0\\0\\0\\0\\364?\\0\\0\\0\\0\\0\\0\\4@\\0\\0\\0\\0\\0\\0\\16...,', '8008)', '=', '8008', '<0.000058>']
   #
   # currentline          # Current split line from strace file
   # Write_obj            # Write object
   # IOPS_obj             # IOPS Ibject
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # WRITE                # Write function keyword
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   
   # local (temporary) variables
   temp_dict = {};
   temp_list = [];
   
   if (debug > 0):
      STRACE_LOG.write("   *** In write_processing routine\n");
   # end if
   
   # Find number of bytes actually written in split string (it's after the = sign)
   #    Find number of bytes written by looking for "=" sign
   #    (index) and using the next index
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # end try
   junk1 = currentline[i+1];
   bytes = int(junk1);            # number of bytes actually written

   # Find unit (file descriptor) for write
   junk1 = currentline[1];
   junk2 = junk1.index("(");
   unit = int(junk1[junk2+1:len(junk1)-1]);
   
   if (debug > 0):
      junk1 = "      unit = " + str(unit) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "      Number of bytes written: " + str(bytes) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "      Elapsed time: " + str(elapsed_time) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "      Throughput (byte/s): " + str(float(bytes)/float(elapsed_time)) + " \n";
      STRACE_LOG.write(junk1);
   # end debug
   
   #
   # If unit is > 0 then put write information into data structures
   #   and object (Note: unit=0 is stdin, unit=1 is stdout, 2=stderr)
   # 
   #   Note: stdin is usually unit=0 but since we shouldn't be writing to
   #         stdin, we can ignore it and start with stdout (unit=1)
   #
   if (unit > 0):
      # Search Open_Filename list of dictionaries for open file match
      i = -1;
      j = -1;
      for item in Open_Filename:
         j = j+1;
         if ( int(item["unit"]) == int(unit) ):
            i = 1;
            filename = item["filename"];
            break
         # end if
      # end for loop
      
      if (i > 0):
         #
         # Add write data to Write_Obj
         #
         temp_list = [];
         temp_list.append(int(LineNum));
         temp_list.append(float(sec));
         temp_list.append(float(elapsed_time));
         temp_list.append(filename.lower());
         temp_list.append(unit);
         if (int(bytes) >= 0):
            temp_list.append(int(bytes));
         else:
            temp_list.append(-1);
         # end if
         junk1 = float(bytes)/float(elapsed_time);
         temp_list.append(junk1)
         Write_obj.storewrite(temp_list);
         
         # Update IOPS_Obj
         temp_list = [];
         temp = int(floor(float(sec) - float(BeginTime)) + 1);
         temp_list.append(LineNum);
         temp_list.append(filename.lower());
         temp_list.append(sec);
         temp_list.append(temp);
         temp_list.append(WRITE);
         IOPS_obj.storeiops(temp_list);
         
         # Add data to File Pointer object (filepointer)
         #  Filepointer = [];           # File pointer for a specific file (list of dictionaries)
         #                              #    Filepointer[iloop]["sec"] = sec
         #                              #    Filepointer[iloop]["unit"] = file descriptor
         #                              #    Filepointer[iloop]["filename"] = filename
         #                              #    Filepointer[iloop]["pointer"] = pointer value
         #                              #    Filepointer[iloop]["type"] = type of call
         temp_dict = {};
         temp_dict["sec"] = sec;
         temp_dict["unit"] = int(unit);
         temp_dict["filename"] = filename.lower();
         if (int(bytes) >= 0):
            temp_dict["pointer"] = int(bytes);
         else:
            temp_dict["pointer"] = -1;
         # end if
         temp_dict["type"] = WRITE;
         Filepointer_obj.storefilepointer(temp_dict);
      else:
         junk2 = "In write_processing: Cannot find filename in Open_filename data structure\n";
         STRACE_LOG.write(junk2);
         junk2 = "   unit: " + str(unit) + " \n";
         STRACE_LOG.write(junk2);
         junk1 = "   Line Number in strace output file = "+str(LineNum)+" \n";
         STRACE_LOG.write(junk1);

         # Rebuild actual line in strace output before writing to logs
         lineOutput = "";
         for tmp in currentline:
            lineOutput = lineOutput + " " + tmp;
         # end for
         lineOutput = lineOutput + "\n";
         junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
         STRACE_LOG.write(junk2);
         
         # Write currently open files to strace logs
         junk2 = "   Currently open files in Open_Filename list: \n";
         STRACE_LOG.write(junk2);     
         for item in Open_Filename:
            junk1 = "      "+str(item) + "\n";
            STRACE_LOG.write(junk1);
         # end for
      # End if
   else:
      STRACE_LOG.write("In write_processing: file descriptor on current write call \n");
      STRACE_LOG.write("   is zero or negative. This should not happen. \n");
      junk2 = "   unit: " + str(unit) + "\n";
      STRACE_LOG.write(junk2);
      junk2 = "   Line number in strace file: " + str(LineNum) + "\n";
      STRACE_LOG.write(junk2);
   # end of "if (unit > 0):"
# end of Write_Processing




#
# Process Read() syscalls filling data structures
#
def Read_Processing(currentline,Read_obj,IOPS_obj,Filepointer_obj,Open_Filename,READ,
                    elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   # Syscall:
   #   ssize_t read(int fildes, void *buf, size_t nbyte);
   # Sample strace line:
   #   1252621029.776685 read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0\200\343"..., 512) = 512 <0.000013>
   # Sample split line:
   #   ['1252621029.776685', 'read(3,', '\\177ELF\\1\\1\\1\\0\\0\\0\\0\\0\\0\\0\\0\\0\\3\\0\\3\\0\\1\\0\\0\\0\\200\\343...,', '512)', '=', '512', '<0.000013>']
   #
   # currentline          # Current split line from strace file
   # Read_obj             # Read object
   # IOPS_obj	          # IOPS object
                          #    Read[iloop]["line"] = LineNum
                          #    Read[iloop]["sec"] = sec
                          #    Read[iloop]["bytes"] = bytes
                          #    Read[iloop]["byte_sec"] = throughput (bytes/time)
                          #    Read[iloop]["elapsed_time"] = elapsed_time;
                          #    Read[iloop]["unit"] = unit;
                          #    Read[iloop]["filename"] = filename;
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # READ                 # Read function keyword
   # ReadMax              # Read maximum time dictionary
                          #   ReadMax["MaxTime"] = maximum time
                          #   ReadMax["line"] = line in strace file
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary



   # local temporary variables:
   temp_dict = {};
   temp_list = [];
   
   if (debug > 0):
      STRACE_LOG.write("   *** In read_processing routine\n");
   # end if
   
   # Find number of bytes read by looking for "=" sign (index) and using the previous index
   #    Get index for "="
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # edn try
   junk1 = currentline[i+1];
   bytes = int(junk1);
   
   # Find unit (file descriptor)
   junk1 = currentline[1];
   junk2 = junk1.index("(");
   unit = int(junk1[junk2+1:len(junk1)-1]);    # file descriptor
   
   #
   # Note: Socket functions and other functions will perform IO to an fd
   #       Need to check if the unit is connected to a file - if so, then
   #       store data - otherwise, ignore the read line because it's a socket
   #
   # Step 1: Find if unit is in use by searching Open_Filename list of
   #    dictionaries for "unit" match
   i = -1;
   for item in Open_Filename:
      if (item["unit"] == unit):
         i = 1;
         filename = item["filename"];
         break
      # end if
   # end for
   
   if (i >= 0):                     # Change here to allow read to std
      # File exists (it is open)
      
      # Add data to Read object
      temp_list = [];
      temp_list.append(LineNum);
      temp_list.append(sec);
      temp_list.append(elapsed_time);
      temp_list.append(filename.lower());
      temp_list.append(unit);
      if (int(bytes) >= 0):
         temp_list.append(bytes);
      else:
         temp_list.append(-1);
      # end if
      temp = float(bytes)/float(elapsed_time);
      temp_list.append(temp);
      Read_obj.storeread(temp_list);
      
      # Update IOPS_Obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(READ);
      IOPS_obj.storeiops(temp_list);
      
      # Add data to File Pointer object (filepointer)
      #  Filepointer = [];           # File pointer for a specific file (list of dictionaries)
      #                              #    Filepointer[iloop]["sec"] = sec
      #                              #    Filepointer[iloop]["unit"] = file descriptor
      #                              #    Filepointer[iloop]["filename"] = filename
      #                              #    Filepointer[iloop]["pointer"] = pointer value
      #                              #    Filepointer[iloop]["type"] = type of call
      temp_dict = {};
      temp_dict["sec"] = sec;
      temp_dict["unit"] = int(unit);
      temp_dict["filename"] = filename.lower();
      if (int(bytes) >= 0):
         temp_dict["pointer"] = int(bytes);
      else:
         temp_dict["pointer"] = -1;
      # end if
      temp_dict["type"] = READ;
      Filepointer_obj.storefilepointer(temp_dict);
   else:
      junk1 = "Read: No file attached to unit " + str(unit) + " - could be a socket\n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line Number: " + str(LineNum) + "\n";
      STRACE_LOG.write(junk1);

      # Rebuild actual line in strace output before writing to logs
      lineOutput = "";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      # end for
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if
# end





#
# Process Lseek() syscalls filling data structures
#                    
def Lseek_Processing(currentline, Lseek_obj, IOPS_obj, Filepointer_obj, Open_Filename,
                     LSEEK, elapsed_time, LineNum, sec, BeginTime, debug, STRACE_LOG,
                     CmdCounter):
   # Syscall:
   #    off_t lseek(int fd, off_t offset, int whence);
   # Sample input line:
   #    1252621029.816022 lseek(3, 0, SEEK_SET)   = 0 <0.000005>
   # Sample split line:
   # ['1252621029.816022', 'lseek(3,', '0,', 'SEEK_SET)', '=', '0', '<0.000005>']
   #
   # 1269925346.094130 lseek(4, 1939, SEEK_SET) = 1939 <0.000004>
   #
   # currentline          # Current split line from strace file
   # Lseek_obj            # Lseek object
   # IOPS_obj             # IOPS object
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # Local temporary variables 
   temp_dict = {};              # local temporary dictionary
   temp_list = [];

   # Find _whence_ by looking for "=" sign (index) and using the previous index        
   #    If whence is SEEK_SET, the file offset shall be set to offset bytes.
   #    If whence is SEEK_CUR, the file offset shall be set to its current location plus offset.
   #    If whence is SEEK_END, the file offset shall be set to the size of the file plus offset.
   #  
   # Get index for "=" because whence is just before ")" in "split" of input line
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # end try
   junk1 = currentline[i-1];
   whence = junk1[0:len(junk1)-1];
   
   # Get offset argument:
   junk1 = currentline[i-2];
   offset = int(junk1[0:len(junk1)-1]);
   
   # Determine current offset (result of lseek)
   off_t_result = currentline[i+1];
   
   # Determine unit (file descriptor) - second element of currentline
   junk1 = currentline[1];
   junk2 = junk1.index("(");
   unit = junk1[junk2+1:len(junk1)-1];

   # find filename associated with unit
   i = -1;
   for item in Open_Filename:
      if ( int(item["unit"]) == int(unit) ):
         i = 1;
         filename = item["filename"];
         break
      # end if
   # end for
   
   
   if (i > 0):
       
       # Update Lseek information
       #    Local dictionary
       temp_dict = {};
       junk3 = float(sec) - float(BeginTime);
       temp_dict = {};
       temp_dict["line_number"] = int(LineNum);
       temp_dict["sec"] = sec;
       temp_dict["elapsed_time"] = float(elapsed_time);
       temp_dict["filename"] = filename;
       temp_dict["unit"] = int(unit);
       temp_dict["whence"] = whence;
       temp_dict["offset"] = int(offset);
       temp_dict["off_t_result"] = int(off_t_result);
       # Append local dictionary to list of dictionaries
       Lseek_obj.storelseek(temp_dict);
       
       # Update IOPS_Obj
       temp_list = [];
       temp = int(floor(float(sec) - float(BeginTime)) + 1);
       temp_list.append(LineNum);
       temp_list.append(filename.lower());
       temp_list.append(sec);
       temp_list.append(temp);
       temp_list.append(LSEEK);
       IOPS_obj.storeiops(temp_list);
       
       # Add data to File Pointer object (filepointer)
       #  Filepointer = [];           # File pointer for a specific file (list of dictionaries)
       #                              #    Filepointer[iloop]["sec"] = sec
       #                              #    Filepointer[iloop]["unit"] = file descriptor
       #                              #    Filepointer[iloop]["filename"] = filename
       #                              #    Filepointer[iloop]["pointer"] = pointer value
       #                              #    Filepointer[iloop]["type"] = type of call
       temp_dict = {};
       temp_dict["sec"] = sec;
       temp_dict["unit"] = int(unit);
       temp_dict["filename"] = filename.lower();
       temp_dict["pointer"] = off_t_result;
       temp_dict["type"] = LSEEK;
       Filepointer_obj.storefilepointer(temp_dict);
   else:
       print "cannot find file in lseek_processing";
       junk2 = "In lseek_processing, cannot find unit in Open_Filename data structure \n";
       STRACE_LOG.write(junk2);
       junk2 = "   unit: " + str(unit) + "\n";
       STRACE_LOG.write(junk2);
       junk2 = "   line number: " + str(currentline) + "\n";
       STRACE_LOG.write(junk2);

       # Print out current list Open_Filename
       for item in Open_Filename:
           junk1 = "      item:"+str(item)+" \n";
           STRACE_LOG.write(junk1);
       # end for loop
   # end if
   
# End of Lseek_Processing





#
# Process Lseek() syscalls filling data structures
#                    
def LLseek_Processing(currentline, Lseek_obj, IOPS_obj, Open_Filename, LSEEK, elapsed_time,
                     LineNum, sec, BeginTime, debug, STRACE_LOG, CmdCounter):
   # Syscall:
   #    off_t lseek(int fd, off_t offset, int whence);
   #    int _llseek(unsigned int fd, unsigned long offset_high,
   #                unsigned long offset_low, loff_t *result,
   #                unsigned int whence);
   # Sample strace line:
   #    1252621029.820685 _llseek(3, 8008, [8008], SEEK_SET) = 0 <0.000011>
   # Sample split line:
   #    ['1252621029.820685', '_llseek(3,', '8008,', '[8008],', 'SEEK_SET)', '=', '0', '<0.000011>']
   #
   #
   # currentline          # Current split line from strace file
   # Lseek_obj            # Lseek object
   # IOPS_obj             # IOPS object
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # Local temporary variables 
   temp_dict = {};              # local temporary dictionary
   temp_list = [];

   # Find _whence_ by looking for "=" sign (index) and using the previous index        
   #    If whence is SEEK_SET, the file offset shall be set to offset bytes.
   #    If whence is SEEK_CUR, the file offset shall be set to its current location plus offset.
   #    If whence is SEEK_END, the file offset shall be set to the size of the file plus offset.
   #  
   # Get index for "=" because whence is just before ")" in "split" of input line
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # end try
   junk1 = currentline[i-1];
   whence = junk1[0:len(junk1)-1];
   
   # Get offset argument:
   junk1 = currentline[i-2];
   offset = int(junk1[0:len(junk1)-1]);
   
   # Determine current offset (result of lseek)
   off_t_result = currentline[i+1];
   
   # Determine unit (file descriptor) - second element of currentline
   junk1 = currentline[1];
   junk2 = junk1.index("(");
   unit = junk1[junk2+1:len(junk1)-1];

   # find filename associated with unit
   i = -1;
   for item in Open_Filename:
      if ( int(item["unit"]) == int(unit) ):
         i = 1;
         filename = item["filename"];
         break
      # end if
   # end for
   

   if (i > 0):
       
       # Update Lseek information
       #    Local dictionary
       temp_dict = {};
       junk3 = float(sec) - float(BeginTime);
       temp_dict = {};
       temp_dict["line_number"] = int(LineNum);
       temp_dict["sec"] = sec;
       temp_dict["elapsed_time"] = float(elapsed_time);
       temp_dict["filename"] = filename;
       temp_dict["unit"] = int(unit);
       temp_dict["whence"] = whence;
       temp_dict["offset"] = int(offset);
       temp_dict["off_t_result"] = int(off_t_result);
       # Append local dictionary to list of dictionaries
       Lseek_obj.storelseek(temp_dict);
       
       # Update IOPS_Obj
       temp_list = [];
       temp = int(floor(float(sec) - float(BeginTime)) + 1);
       temp_list.append(LineNum);
       temp_list.append(filename.lower());
       temp_list.append(sec);
       temp_list.append(temp);
       temp_list.append(LSEEK);
       IOPS_obj.storeiops(temp_list);
   else:
       print "cannot find file in lseek_processing";
       junk2 = "In lseek_processing, cannot find unit in Open_Filename data structure \n";
       STRACE_LOG.write(junk2);
       junk2 = "   unit: " + str(unit) + "\n";
       STRACE_LOG.write(junk2);
       junk2 = "   line number: " + str(currentline) + "\n";
       STRACE_LOG.write(junk2);

       # Print out current list Open_Filename
       for item in Open_Filename:
           junk1 = "      item:"+str(item)+" \n";
           STRACE_LOG.write(junk1);
       # end for loop
   # end if
   
# End of LLseek_Processing






#
# Process FSTAT IO functions() syscalls that use a unit and fill data structures
#
def FSTAT_Processing(currentline,FSTAT_obj,IOPS_obj,COMMAND,Open_Filename,
                     elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # FSTAT_obj            # FSTAT object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary

   
   # Get unit
   junk1 = currentline[1].split('(')[1];
   junk2 = junk1[0:len(junk1)-1];
   unit = int(junk2);
   
   # See if "unit" is in Open_Filename - if so, store COMMAND information
   i = -1;
   for item in Open_Filename:
      if ( int(item["unit"]) == int(unit) ):
         i = 1;
         filename = item["filename"];
         break
      # end if
   # end for
   
   if (i > 0):
      # file descriptor exists

      # st_mode
      junk1 = currentline[2].split('{');
      junk2 = junk1[1];
      junk3 = junk2[0:7];
      if (junk3 == "st_mode"):
         # found st_mode
         test2 = junk2[0:len(junk2)-1].split('=');
         st_mode = test2[1];
      else:
         st_mode = " ";
      # end if
      
      # st_size
      junk1 = currentline[3];
      junk2 = junk1[0:len(junk1)-1];
      junk3 = junk2[0:7];
      if (junk3 == "st_size"):
         # found st_size
         st_size = junk2;
      else:
         st_size = " ";
      # end if
      
      # Update FSTAT_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(unit);                #   unit           (file descriptor associated with file)
      temp_list.append(st_mode);             #   st_mode        (file descriptor protection)
      temp_list.append(st_size);             #   st_size        (total size in bytes)
      FSTAT_obj.storefstat(temp_list);
      
      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);
   else:
      junk1 = "In Unit_IO_Processing for Command: " + COMMAND + " - cannot find unit in Open_File \n";
      STRACE_LOG.write(junk1);
      junk1 = "   unit = " + str(unit) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line Number = " + str(LineNum) + " \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
      
      # Print out Open_Filename data
      junk1 = "   Open_Filename: \n";
      STRACE_LOG.write(junk1);
      for item in Open_Filename:
         junk1 = "         "+str(item) + "\n";
         STRACE_LOG.write(junk1);
      # end for
   # end if
# end def





#
# Process STAT IO functions() syscalls that use a unit and fill data structures
#
def STAT_Processing(currentline,STAT_obj,IOPS_obj,COMMAND,Open_Filename,
                     elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # STAT_obj             # STAT object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # Get the filename (after "(" )
   i = -1;
   j = 0;
   for item in currentline:
      if ( item[0:4].lower() == "stat" ):
         i = 1;
         break
      # end if
      j = j + 1;
   # end for
   
   if (i > 0):
      # found stat command
      
      # find input file for stat command
      test1 = currentline[j];
      filename = test1[5:(len(test1)-1)];
      
      # check if filename is in Open_Filename:
      i = -1;
      unit = -1;
      for item in Open_Filename:
         if ( item["filename"] == filename ):
            i = 1;
            unit = item["unit"];
            break
         # end if
      # end for
      
      # search for equal sign
      i = -1;
      for item in currentline:
         if (item == "="):
            i = j;
            break
         # end if
         j = j + 1;
      # end for
      
      if (i > 0):
         test1 = currentline[i:(len(currentline)-1)];
         result = test1[0];
         message = "";
         for item in test1[1:]:
            message = message + " " + item
         # end for
      # end if
      
      # Update STAT_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(int(unit));           #   unit           (file descriptor from Open_Filename)
      temp_list.append(int(result));         #   result         (result of stat call)
      temp_list.append(message);             #   message        (message from stat call - typcially an error)
      STAT_obj.storestat(temp_list);
      
      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);

   else:
      junk1 = "In STAT_Processing for Command: " + COMMAND + " - cannot find file in stat command \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if

# end def



#
# Process FSYNC IO functions() syscalls that use a unit and fill data structures
#
def FSYNC_Processing(currentline,FSYNC_obj,IOPS_obj,COMMAND,Open_Filename,
                     elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # FSYNC_obj            # FSYNC object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   
   # Get the unit (file descriptor)
   i = -1;
   j = 0;
   for item in currentline:
      if ( item[0:5].lower() == "fsync" ):
         i = 1;
         break
      # end if
      j = j + 1;
   # end for
   
   if (i > 0):
      # Found fsync command
      
      # Get unit
      test1 = currentline[j];
      unit = int(test1[6:(len(test1)-1)]);

      # search Open_Filename for file name
      i = -1;
      unit = -1;
      filename = "";
      for item in Open_Filename:
         if ( int(item["unit"]) == unit ):
            i = 1;
            filename = item["filename"];
            break
         # end if
      # end for
      
      # Get result (after "=")
      try:
         i = currentline.index("=");
      except ValueError:
         i = -1 # no match
      # end try
      result = int(currentline[i+1]);    # file descriptor
      if (result != 0):  # successful
         test1 = currentline[(i+2):];
         test2 = test1[0:(len(test1) - 1)];
         
         message = " ";
         for tmp in test2:
            message = message + " " + tmp;
         # end for
      else:
         message="";
      # end if
      
      # Update FSYNC_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(int(unit));           #   unit           (file descriptor from Open_Filename)
      temp_list.append(int(result));         #   result         (result of stat call)
      temp_list.append(message);             #   message        (message from stat call - typcially an error)
      FSYNC_obj.storefsync(temp_list);
      
      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);
   else:
      junk1 = "In FSYNC_Processing for Command: " + COMMAND + " - cannot find file in fsync command \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if
# end def



#
# Process UNLINK IO functions() syscalls that use a unit and fill data structures
#
def UNLINK_Processing(currentline,UNLINK_obj,IOPS_obj,COMMAND,Open_Filename,
                      elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # UNLINK_obj           # FSYNC object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   
   # Get the filename (after "unlink(" )
   i = -1;
   j = 0;
   for item in currentline:
      if ( item[0:6].lower() == "unlink" ):
         i = 1;
         break
      # end if
      j = j + 1;
   # end for
   
   if (i > 0):
      # Found unlink command
      
      # Get unit
      test1 = currentline[j];
      filename = test1[7:(len(test1)-1)];
      
      # search Open_Filename for filename
      i = -1;
      unit = -1;
      for item in Open_Filename:
         if ( item["filename"] == filename.lower() ):
            i = 1;
            unit = item["unit"];
            break
         # end if
      # end for
      
      # Get result (after "=")
      try:
         i = currentline.index("=");
      except ValueError:
         i = -1 # no match
      # end try
      result = int(currentline[i+1]);    # file descriptor
      if (result != 0):  # successful
         test1 = currentline[(i+2):];
         test2 = test1[0:(len(test1) - 1)];
         
         message = " ";
         for tmp in test2:
            message = message + " " + tmp;
         # end for
      else:
         message="";
      # end if
      
      # Update UNLINK_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(int(unit));           #   unit           (file descriptor from Open_Filename)
      temp_list.append(int(result));         #   result         (result of stat call)
      temp_list.append(message);             #   message        (message from stat call - typcially an error)
      UNLINK_obj.storeunlink(temp_list);
      
      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);
   else:
      junk1 = "In UNLINK_Processing for Command: " + COMMAND + " - cannot find file in unlink command \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if
# end def





#
# Process FCNTL IO functions() syscalls that use a unit and fill data structures
#
def FCNTL_Processing(currentline,FCNTL_obj,IOPS_obj,COMMAND,Open_Filename,
                     elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # FCNTL_obj            # FSYNC object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   
   # Get the unit (file descriptor)
   i = -1;
   j = 0;
   for item in currentline:
      if ( item[0:5].lower() == "fcntl" ):
         i = 1;
         break
      # end if
      j = j + 1;
   # end for
  
   if (i > 0):
      # Found fcntl command
      
      # Get unit
      test1 = currentline[j];
      unit = int(test1[6:(len(test1)-1)]);
      
      # search Open_Filename for file name
      i = -1;
      unit = -1;
      filename = "";
      for item in Open_Filename:
         if ( int(item["unit"]) == unit ):
            i = 1;
            filename = item["filename"];
            break
         # end if
      # end for
      
      # Get bits ater file descriptor and before equals sign
      # Get result (after "=")
      try:
         k = currentline.index("=");
      except ValueError:
         k = -1 # no match
      # end try
      if (k > 0):
         test1 = currentline[(j+1):k];
         test2 = "";
         for item in test1:
            test2 = test2 + item
         # end if
         cmd = test2[0:(len(test2)-1)];
      else:
         cmd = "";
      # end if
      
      # Get result (after "=")
      result = currentline[k+1];    # result of fcntl command (this can be a non-integer 
                                    #   so make it a string)
      if (result != "0"):           # Gather any information that might be passed back
         test1 = currentline[(k+2):(len(currentline)-1)];
         
         message = " ";
         for tmp in test1:
            message = message + " " + tmp;
         # end for
      else:
         message="";
      # end if
      
      # Update FSYNC_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(int(unit));           #   unit           (file descriptor from Open_Filename)
      temp_list.append(cmd);                 #   cmd            (command for fcntl)
      temp_list.append(result);              #   result         (result of fcntl call - string)
      temp_list.append(message);             #   message        (message from fcntl call)
      FCNTL_obj.storefcntl(temp_list);

      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);
   else:
      junk1 = "In FCNTL_Processing for Command: " + COMMAND + " - cannot find file in fcntl command \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if
# end def


#
# Process ACCESS IO functions() syscalls that use a unit and fill data structures
#
def ACCESS_Processing(currentline,ACCESS_obj,IOPS_obj,COMMAND,Open_Filename,
                      elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # ACCESS_obj            # FSYNC object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   
   # Get the file descriptor
   i = -1;
   j = 0;
   for item in currentline:
      if ( item[0:6].lower() == "access" ):
         i = 1;
         break
      # end if
      j = j + 1;
   # end for
   
   if (i > 0):
      # Found access command
      
      # Get filename
      test1 = currentline[j];
      filename = test1[7:(len(test1)-1)];

      # search Open_Filename for file descriptor (unit)
      i = -1;
      unit = -1;
      filename = "";
      for item in Open_Filename:
         if ( item["filename"] == filename.lower() ):
            i = 1;
            unit = item["unit"];
            break
         # end if
      # end for
      
      # get command:
      try:
         k = currentline.index("=");
      except ValueError:
         k = -1 # no match
      # end try
      if ( (j+1) == (k-1) ):
         test1 = currentline[(j+1)];    # file descriptor
      elif ( (j+1) < (k-1) ):
         test1 = currentline[(j+1):(k-1)]; 
      else:
         print "something is jacked up"
      # end if
      mode = test1[0:(len(test1)-1)];
      
      result = int(currentline[k+1]);    # file descriptor
      if (result != 0):  # successful
         test1 = currentline[(k+2):];
         test2 = test1[0:(len(test1) - 1)];
         
         message = " ";
         for tmp in test2:
            message = message + " " + tmp;
         # end for
      else:
         message="";
      # end if
      
      # Update ACCESS_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(int(unit));           #   unit           (file descriptor from Open_Filename)
      temp_list.append(mode);                #   mode           (mode in access command)
      temp_list.append(int(result));         #   result         (result of stat call)
      temp_list.append(message);             #   message        (message from stat call - typcially an error)
      ACCESS_obj.storeaccess(temp_list);
      
      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);
   else:
      junk1 = "In ACCESS_Processing for Command: " + COMMAND + " - cannot find file in access command \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if
# end def




#
# Process GETDENTS IO functions() syscalls that use a unit and fill data structures
#
def GETDENTS_Processing(currentline,GETDENTS_obj,IOPS_obj,COMMAND,Open_Filename,
                      elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # GETDENTS_obj         # GETDENTS object
   # IOPS_obj             # IOPS Object
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   
   # Get the file descriptor (unit)
   i = -1;
   j = 0;
   for item in currentline:
      if ( item[0:8].lower() == "getdents" ):
         i = 1;
         break
      # end if
      j = j + 1;
   # end for
   
   if (i > 0):
      # Found getdents command
      
      # Get unit
      test1 = currentline[j];
      unit = test1[9:(len(test1)-1)];
      
      # Search Open_Filename for filename
      i = -1;
      unit = -1;
      filename = "";
      for item in Open_Filename:
         if ( int(item["unit"]) == unit ):
            i = 1;
            filename = item["filename"];
            break
         # end if
      # end for
      
      # Get numebr of bytes read (value after "=" sign)
      try:
         k = currentline.index("=");
      except ValueError:
         k = -1 # no match
      # end try
      if (k > 0):
         readbytes = int(currentline[k+1]);
      else:
         readbytes = -1;
      # end if
      
      # Update GETDENTS_obj
      temp_list = [];
      temp_list.append(LineNum);             #   LineNum        (line number of strace output file)
      temp_list.append(sec);                 #   sec            (seconds since epoch when function was called)
      temp_list.append(elapsed_time);        #   elapsed_time   (elapsed time for open)
      temp_list.append(filename.lower());    #   filename       (filename for file being opened)
      temp_list.append(int(unit));           #   unit           (file descriptor from Open_Filename)
      temp_list.append(readbytes);           #   readbytes      (number of bytes read)
      GETDENTS_obj.storegetdents(temp_list);
      
      # Update IOPS_obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);
   else:
      junk1 = "In GETDENTS_Processing for Command: " + COMMAND + " - cannot find file in getdents command \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
   # end if
# end def



#
# Process IO functions() syscalls that use a unit and fill data structures
#
def Unit_IO_Processing(currentline,COMMAND,Open_Filename,IOPS_obj,elapsed_time,
                       LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # IOPS_obj             # IOPS Object
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   # Get unit
   junk1 = currentline[1].split('(')[1];
   junk2 = junk1[0:len(junk1)-1];
   unit = int(junk2);
   
   # See if "unit" is in Open_Filename - if so, store COMMAND information
   i = -1;
   for item in Open_Filename:
      if ( int(item["unit"]) == int(unit) ):
         i = 1;
         filename = item["filename"];
         break
      # end if
   # end for
   
   if (i > 0):
      # Update IOPS_Obj
      temp_list = [];
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_list.append(LineNum);
      temp_list.append(filename.lower());
      temp_list.append(sec);
      temp_list.append(temp);
      temp_list.append(COMMAND);
      IOPS_obj.storeiops(temp_list);

      #IOPS_insert(IOPS_info,IOPS,COMMAND,sec,BeginTime,unit,debug,STRACE_LOG);
   else:
      junk1 = "In Unit_IO_Processing for Command: " + COMMAND + " - cannot find unit in Open_File \n";
      STRACE_LOG.write(junk1);
      junk1 = "   unit = " + str(unit) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line Number = " + str(LineNum) + " \n";
      STRACE_LOG.write(junk1);
      
      # Print out current strace output line
      lineOutput = "   Line: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
      
      # Print out Open_Filename data
      junk1 = "   Open_Filename: \n";
      STRACE_LOG.write(junk1);
      for item in Open_Filename:
         junk1 = "         "+str(item) + "\n";
         STRACE_LOG.write(junk1);
      # end for
   # end if
# end def




#
# Process IO functions() syscalls that use a filename and fill data structures
#
def File_IO_Processing(currentline, COMMAND, Open_Filename, IOPS_info, IOPS, elapsed_time, 
                       LineNum, sec, BeginTime, debug, STRACE_LOG, CmdCounter):
   #
   # Command Line arguments:
   # -----------------------
   # currentline          # Current split line from strace file
   # COMMAND              # value of COMMAND function
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # IOPS_info            # List of dictionaries of IOPS information
                          #   IOPS_info[iloop]["filename"] = filename
                          #   IOPS_info[iloop]["unit"] = unit
                          #   IOPS_info[iloop]["pointer"] = pointer to Offset array
   # IOPS                 # Total IOPS information (list of dictionaries)
                          #   IOPS[iloop]["time"] = time interval (in seconds)
                          #   IOPS[iloop]["pointer"] = pointer to IOPS_info array
                          #   IOPS[iloop]["type"] = (IOPS Function list)
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   # Get filename
   junk1 = currentline[1].split('(')[1];
   filename = junk1[0:len(junk1)-1];
   
   unit = -1;
   # insert data into IOPS data structures
   IOPS_insert(IOPS_info,IOPS,COMMAND,sec,BeginTime,unit,debug,STRACE_LOG);

   if (debug > 0):
      junk1 = "In File_IO_Processing for Command: "+COMMAND+" - After calling IOPS_insert \n";
      STRACE_LOG.write(junk1);
      junk1 = "   unit = "+str(unit)+" \n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line Number = "+str(LineNum)+" \n";
      STRACE_LOG.write(junk1);
      junk1 = "   unit: "+str(unit)+" \n";
      STRACE_LOG.write(junk1);
      junk1 = "   Open_Filename: \n";
      STRACE_LOG.write(junk1);
      for item in Open_Filename:
         junk1 = "         "+str(item) + "\n";
         STRACE_LOG.write(junk1);
      # end for
   # end debug
   
# end def




