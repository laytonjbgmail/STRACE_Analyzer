

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
def Open_Processing(currentline,Open,Open_Filename,Lseek_info,IOPS_info,IOPS,File_Stats,
                    Offset_info,Offset,OPEN,OpenMax,OpenMin,elapsed_time,
                    LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
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
   # Open                 # Open function call list dictionaries
                          #   Open[iloop]["line_number"] = LineNum;
                          #   Open[iloop]["sec"] = sec;
                          #   Open[iloop]["file"] = filename;
                          #   Open[iloop]["unit"] = unit;
                          #   Open[iloopOpen_Filename]["elapsed_time"] = elapsed_time;
   # Lseek_info;          # Lseek file information
   # Lseek_info           # List of dictionaires of lseek information
                          #   Lseek_info[iloop]["filename"] = filename
                          #   Lseek_info[iloop]["unit"] = unit
                          #   Lseek_info[iloop]["pointer"] = pointer to Lseek-info array
                          #                                 (used to get file name for this offset)
   # IOPS_info            # List of dictionaries of IOPS information
                          #   IOPS_info[iloop]["filename"] = filename
                          #   IOPS_info[iloop]["unit"] = unit
                          #   IOPS_info[iloop]["pointer"] = pointer to Offset array
   # IOPS                 # Total IOPS information (list of dictionaries)
                          #   IOPS[iloop]["time"] = time interval (in seconds)
                          #   IOPS[iloop]["pointer"] = pointer to IOPS_info array
                          #   IOPS[iloop]["type"] = (IOPS Function list)
   # IOPS;                # Main IOPS data structure
   # File_Stats           # File Statistics
                          #   File_stats[iloop]["unit"] = unit
                          #   File_Stats[iloop]["file"] = $filename; 
                          #   File_Stats[iloop]["read_bytes"] += $byte;
                          #   File_Stats[iloop]["write_bytes"] += $byte; 
                          #   File_Stats[iloop]["read_rate_count"]
                          #   File_Stats[iloop]["read_rate_sum"]
                          #   File_Stats[iloop]["write_rate_sum"]
                          #   File_Stats[iloop]["write_rate_count"]
   # Offset_info          # List of dictionaries of offset infomroation
                          #   Offset_info[iloop]["filename"] = filename
                          #   Offset_info[iloop]["unit"] = unit
                          #   Offset_info[iloop]["pointer"] = pointer to Offset_info array
                          #   Offset_info[iloop]["offset_cur"] = Current offset in bytes
   # Offset               # Offset information (list of dictionaries)
                          #   It contains the offset information for all file. They
                          #   distinguished by "pointer" which points to the partifular
                          #   file in Offset_info
                          #   Offset[iloop]["pointer"] = pointer to filename in Offset_info
                          #   Offset[iloop]["time"] = time;
                          #   Offset[iloop]["offset"] = offset (in bytes)
   # OPEN;                # Keyword for open syscall
   # OpenMax              # OpenMax dictionary
                          #    OpenMax["MaxTime"] = maximum time
   # OpenMin              # OpenMin dictionary
                          #    OpenMin["MinTime"] = minimum time
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # Local temporary variables 
   temp_dict = {};             # local temporary dictionary
   
   # Get file name
   #    currentline[1] containst the filename after "("
   junk1 = currentline[1].split('(')[1];
   filename = junk1[0:len(junk1)-1];

   # Get file descriptor (unit)
   #   (it is after "=" in split line)
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   # end try
   unit = int(currentline[i+1]);    # file descriptor
   if (debug > 0):
      if (unit < 0):
         junk1 = "      Open did not succeed on fd: " + str(unit) + "  So not adding fd to statistics \n";
         STRACE_LOG.write(junk1);
      else:
         junk1 = "      unit: " + str(unit) + " \n";
         STRACE_LOG.write(junk1);
      # end "if (unit < 0):"
   # end "if (debug > 0):"
   
   # If unit is positive (i.e. it was successfully opened) then start processing
   #   information about open function and populate data structures
   if (unit > 0):
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
      
      # Update Maxmimum open time (if necessary)
      if (elapsed_time > OpenMax["MaxTime"] ):
         OpenMax["MaxTime"] = elapsed_time;
         OpenMax["line"] = LineNum - 1; 
      elif ( float(elapsed_time) < float(OpenMin["MinTime"]) ):
         OpenMin["MinTime"] = elapsed_time;
         OpenMin["line"] = LineNum - 1;
      # end if statement
      
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
         junk1 = "*** Warning: Filename " + filename + " for unit " + str(unit) + " already exists \n";
         STRACE_LOG.write(junk1);
         junk1 = "    filename: " + str( record["filename"] ) + "\n";
         STRACE_LOG.write(junk1);
      else:
         # File does not exists in data structures - throw a message to the log and continue
         junk1 = "*** Filename " + filename + " for unit " + str(unit) + " does not exist in Open_Filename \n";
         STRACE_LOG.write(junk1);
         
         temp_dict = {};
         temp_dict["unit"] = int(unit);
         temp_dict["filename"] = filename;
         Open_Filename.append(temp_dict);
         junk1 = "*** Filename " + filename + " for unit " + str(unit) + " added to Open_Filename dictionary \n";
         STRACE_LOG.write(junk1);
         
         # Add data to Open data structure
         temp_dict = {};
         temp_dict["line_number"] = LineNum;
         temp_dict["sec"] = sec;
         temp_dict["file"] = filename;
         temp_dict["unit"] = int(unit);
         temp_dict["elapsed_time"] = elapsed_time;
         Open.append(temp_dict);
         
         # Add file data to Offset_info by using local dictionary
         #   and appending it to Offset_info
         temp_dict = {};
         temp_dict["filename"] = filename;
         temp_dict["unit"] = int(unit);
         if (len(Offset_info) <= 0):
            temp_dict["pointer"] = 1;
         else:
            temp_dict["pointer"] = len(Offset_info) + 1;\
         #
         temp_dict["offset_cur"] = 0;
         Offset_info.append(temp_dict);
         
         # Initialize actual offset data 
         temp_dict = {};
         temp_dict["pointer"] = junk1;
         temp_dict["time"] = float(sec)-float(BeginTime);
         temp_dict["offset"] = 0;
         Offset.append(temp_dict);
         
         # Add file data to lseek_info by using local dictionary (Lseek_local)
         #   and appending it to Lseek_info
         temp_dict = {};
         temp_dict["filename"] = filename;
         temp_dict["unit"] = int(unit);
         if (len(Lseek_info) <= 0):
            temp_dict["pointer"] = 1;
         else:
            temp_dict["pointer"] = len(Lseek_info)+1;
         # end if
         Lseek_info.append(temp_dict);
         
         # Add file data to IOPS_info by using local dictionary (IOPS_local)
         #    and appending it to IOPS_info
         temp_dict = {};
         temp_dict["filename"] = filename;
         temp_dict["unit"] = int(unit);
         if (len(IOPS_info) <= 0):
            local_pointer = 1;
            temp_dict["pointer"] = local_pointer;
         else:
            local_pointer = len(IOPS_info)+1;
            temp_dict["pointer"] = local_pointer;
         # end if
         IOPS_info.append(temp_dict);
         
         # Update IOPS data structure by using local dictionary (IOPS_local)
         #   and appending it to IOPS
         temp_dict = {};
         # Compute time interval (in seconds) relative to start 
         temp = int(floor(float(sec) - float(BeginTime)) + 1);
         temp_dict["time"] = temp;
         temp_dict["pointer"] = local_pointer;
         temp_dict["type"] = OPEN;
         IOPS.append(temp_dict);
         
         # Update file stats data structure (actually this will initialize it)
         #    Search if filename already exists in File_Stats array
         #       if k is negative then the file does not exist in File_Stats - so add it
         #       Also if File_Stats is empty (length of array is zero) then add file to array
         #
         # Also use this check to add the file information to Offset_info and IOPS_info
         
         k = -1;
         for item in File_Stats:
            junk1 = item["filename"];
            if (junk1.lower() == filename.lower() ):
               k = 1;
               break;
            # end if
         # end for loop
         if (len(File_Stats) == 0):
            k = -1;
         # endif
         
         if (k < 0):
            # Add file information to File_Stats data structure by first creating
            #   local dictionary (File_Stats_Dict) and then appending it to the array
            temp_dict = {};
            temp_dict["unit"] = int(unit);
            temp_dict["filename"] = filename;
            temp_dict["read_bytes"] = 0;
            temp_dict["write_bytes"] = 0;
            temp_dict["read_rate_count"] = 0;
            temp_dict["read_rate_sum"] = 0;
            temp_dict["write_rate_sum"] = 0;
            temp_dict["write_rate_count"] = 0;
            File_Stats.append(temp_dict);
         #endif
      # end "if (i > 0):"
      if (debug > 0):
         junk1 = "      filename: " + filename + " \n";
         STRACE_LOG.write(junk1);
      # end if
   # End of if
# End of Open_Processing



#
# Process Read() syscalls filling data structures
#
def Read_Processing(currentline,Read,Open_Filename,IOPS_info,IOPS,File_Stats,Offset_info,
                    Offset,READ,ReadMax,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                    CmdCounter,ReadBytesTotal,lineOutput):
   # Syscall:
   #   ssize_t read(int fildes, void *buf, size_t nbyte);
   # Sample strace line:
   #   1252621029.776685 read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0\200\343"..., 512) = 512 <0.000013>
   # Sample split line:
   #   ['1252621029.776685', 'read(3,', '\\177ELF\\1\\1\\1\\0\\0\\0\\0\\0\\0\\0\\0\\0\\3\\0\\3\\0\\1\\0\\0\\0\\200\\343...,', '512)', '=', '512', '<0.000013>']
   #
   # currentline          # Current split line from strace file
   # Read                 # Read list - actually it's a list of dictionaries
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
   # IOPS_info            # List of dictionaries of IOPS information
                          #   IOPS_info[iloop]["filename"] = filename
                          #   IOPS_info[iloop]["unit"] = unit
                          #   IOPS_info[iloop]["pointer"] = pointer to Offset array
   # IOPS                 # Total IOPS information (list of dictionaries)
                          #   IOPS[iloop]["time"] = time interval (in seconds)
                          #   IOPS[iloop]["pointer"] = pointer to IOPS_info array
                          #   IOPS[iloop]["type"] = (IOPS Function list)
   # IOPS;                # Main IOPS data structure
   # File_Stats           # File Statistics
                          #   File_stats[iloop]["unit"] = unit
                          #   File_Stats[iloop]["file"] = $filename; 
                          #   File_Stats[iloop]["read_bytes"] += $byte;
                          #   File_Stats[iloop]["write_bytes"] += $byte; 
                          #   File_Stats[iloop]["read_rate_count"]
                          #   File_Stats[iloop]["read_rate_sum"]
                          #   File_Stats[iloop]["write_rate_sum"]
                          #   File_Stats[iloop]["write_rate_count"]
   # Offset_info          # List of dictionaries of offset infomroation
                          #   Offset_info[iloop]["filename"] = filename
                          #   Offset_info[iloop]["unit"] = unit
                          #   Offset_info[iloop]["pointer"] = pointer to Offset_info array
                          #   Offset_info[iloop]["offset_cur"] = Current offset in bytes
   # Offset               # Offset information (list of dictionaries)
                          #   It contains the offset information for all file. They
                          #   distinguished by "pointer" which points to the partifular
                          #   file in Offset_info
                          #   Offset[iloop]["pointer"] = pointer to filename in Offset_info
                          #   Offset[iloop]["time"] = time;
                          #   Offset[iloop]["offset"] = offset (in bytes)
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
   # ReadBytesTotal       # Toal bytes read
   # lineOutput           # Complete strace line (not split) - used for debugging



   # local temporary variables:
   temp_dict = {};
   
   if (debug > 0):
      STRACE_LOG.write("   *** In read_processing routine\n");
   # end if
   
   # Find number of bytes read by looking for "=" sign (index) and using the previous index
   # Get index for "="
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   junk1 = currentline[i+1];
   bytes = int(junk1);
   
   # Find unit
   junk1 = currentline[1];
   junk2 = junk1.index("(");
   unit = int(junk1[junk2+1:len(junk1)-1]); 
   
   # Update maximum read time (if necessary)
   if (float(elapsed_time) > float(ReadMax["MaxTime"]) ):
      ReadMax["MaxTime"] = elapsed_time;
      ReadMax["line"] = LineNum - 1;
   # end if
   
   #
   # Note: Socket functions and other functions will perform IO to an fd
   #       Need to check if the unit is connected to a file - if so, then
   #       store data - otherwise, ignore the read line because it's a socket
   #
   # Step 1: Find if unit is in use by searching Open_Filename list of
   #    dictionaries for "unit" match
   i = -1;
   for item in Open_Filename:
      if item["unit"] == unit:
         i = 1;
         break
      # end if
   # end for
   
   if (i > 0):
      # File exists (it is open)
      
      # Add data to Read data structure
      #   Create temporary (local) dictionary to hold data structure and
      #   then use append method to add it to Read data structure
      temp_dict = {};
      temp_dict["line"] = LineNum;
      temp_dict["sec"] = sec;
      if (int(bytes) >= 0):
         temp_dict["bytes"] = bytes;
      else:
         temp_dict["bytes"] = -1;
      # end if
      temp_dict["byte_sec"] = float(bytes)/float(elapsed_time);
      temp_dict["elapsed_time"] = elapsed_time;
      temp_dict["unit"] = unit;
      
      k = -1;
      for item in Open_Filename:
         if (item["unit"] == unit):
            k = 1;
            junk1 = item["filename"];
            break;
         #end if
      # end for loop
      if (k > 0):
         temp_dict["filename"] = junk1;
      else:
         print "Error in read_processing routine. Cannot find filename \n";
         print "    associated with unit:",unit;
         temp_dict["filename"] = " ";
      #end if
      if (debug > 0):
         junk1 = "   *** Filename: " + item["filename"] + "  Number of Bytes: " + str(temp_dict["bytes"]);
         junk1 = junk1 + " Elapsed Time: " + str(temp_dict["elapsed_time"]) + " Throughput: ";
         junk1 = junk1 + str(temp_dict["byte_sec"]) + " byte/sec  ( ";
         junk1 = junk1 + str( (temp_dict["byte_sec"]/1000000) ) + " MB/s) \n";
         STRACE_LOG.write(junk1);
      # end if
      Read.append(temp_dict);
      
      # Add number of bytes to total bytes read
      ReadBytesTotal["sum"] = ReadBytesTotal["sum"] + int(bytes);
      
      # Find File_Stats dictionary corresponding to the current unit
      #
      # Step 1 - find if unit is on Open_Filename list - if so, find associated file name
      k = -1;
      for item in Open_Filename:
         if (item["unit"] == unit):
            k = 1;
            junk1 = item["filename"];
            break;
         #end if
      # end for loop
      
      # Step 2 - Use file name to find dictionary in File_Stats list corresponding to file
      if (k > 0):       # file exists in Open_Filenam (it meanst the file is open)
         l = -1;
         File_Stats_pointer = -1;
         for item in File_Stats:
            l = l+1;
            junk2 = item["filename"]
            if ( junk2.lower() == junk1.lower() ):
               File_Stats_pointer = l;
               break;
            # end of
         # end for loop
         if (File_Stats_pointer >= 0):
            File_Stats[File_Stats_pointer]["read_bytes"] = File_Stats[File_Stats_pointer]["read_bytes"] + int(bytes);
            File_Stats[File_Stats_pointer]["read_rate_sum"] = File_Stats[File_Stats_pointer]["read_rate_sum"] + (float(bytes)/float(elapsed_time));
            File_Stats[File_Stats_pointer]["read_rate_count"] = File_Stats[File_Stats_pointer]["read_rate_count"] + 1;
         else:
            print "In Read processing. File_Stats_pointer is negative - problem";
         # end if
         
         # Update IOPS array
         IOPS_insert(IOPS_info,IOPS,READ,sec,BeginTime,unit,debug,STRACE_LOG);
         
         # Update File offset tracking
         Offset_insert(Offset_info,Offset,sec,BeginTime,bytes,LineNum,unit);
         
         # end if
      else:
         print "In Read Processing. Cannot find unit listed in Open_Filename array - problem";
      # end if
   else:
      #print "   File is not open";
      junk1 = "Read: No file attached to unit " + str(unit) + " - could be a socket\n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line Number: " + str(LineNum) + "\n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line: " + lineOutput + "\n";
      STRACE_LOG.write(junk1);
   # end if
# end "def Read_Processing(currentline):"



#
# Process Write() syscalls filling data structures
#                    
def Write_Processing(currentline,Write,Open_Filename,IOPS_info,IOPS,File_Stats,Offset_info,
                     Offset,WRITE,WriteMax,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,
                     CmdCounter,WriteBytesTotal):
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
   # Write                # Write list - actually it's a list of dictionaries
                          #    Write[iloop]["line"] = LineNum
                          #    Write[iloop]["sec"] = sec
                          #    Write[iloop]["elapsed_time"] = elapsed_time;
                          #    Write[iloop]["unit"] = unit;
                          #    Write[iloop]["byte_sec"] = bytes per sec
                          #    Write[iloop]["bytes"] = bytes;
                          #    Write[iloop]["filename"] = filename (from Open_filename)
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
   # IOPS;                # Main IOPS data structure
   # File_Stats           # File Statistics
                          #   File_stats[iloop]["unit"] = unit
                          #   File_Stats[iloop]["file"] = $filename; 
                          #   File_Stats[iloop]["read_bytes"] += $byte;
                          #   File_Stats[iloop]["write_bytes"] += $byte; 
                          #   File_Stats[iloop]["read_rate_count"]
                          #   File_Stats[iloop]["read_rate_sum"]
                          #   File_Stats[iloop]["write_rate_sum"]
                          #   File_Stats[iloop]["write_rate_count"]
   # Offset_info          # List of dictionaries of offset infomroation
                          #   Offset_info[iloop]["filename"] = filename
                          #   Offset_info[iloop]["unit"] = unit
                          #   Offset_info[iloop]["pointer"] = pointer to Offset_info array
                          #   Offset_info[iloop]["offset_cur"] = Current offset in bytes
   # Offset               # Offset information (list of dictionaries)
                          #   It contains the offset information for all file. They
                          #   distinguished by "pointer" which points to the partifular
                          #   file in Offset_info
                          #   Offset[iloop]["pointer"] = pointer to filename in Offset_info
                          #   Offset[iloop]["time"] = time;
                          #   Offset[iloop]["offset"] = offset (in bytes)
   # WRITE                # Write function keyword
   # WriteMax             # Write maximum time dictionary
                          #   WriteMax["MaxTime"] = maximum time
                          #   WriteMax["line"] = line in strace file
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   # WriteBytesTotal      # Toal bytes written
   
   
   
   # local (temporary) variables
   temp_dict = {};
   
   if (debug > 0):
      STRACE_LOG.write("   *** In write_processing routine\n");
   # end if
   
   # Find number of bytes in split string (it's after the = sign)
   #    Find number of bytes written by looking for "=" sign
   #    (index) and using the next index
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   junk1 = currentline[i+1];
   bytes = int(junk1);

   # Find unit
   junk1 = currentline[1];
   junk2 = junk1.index("(");
   unit = int(junk1[junk2+1:len(junk1)-1]);
   
   if (debug > 0):
      junk1 = "      unit = " + str(unit) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "      Number of bytes: " + str(bytes) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "      Elapsed time: " + str(elapsed_time) + " \n";
      STRACE_LOG.write(junk1);
      junk1 = "      Throughput (byte/s): " + str(float(bytes)/float(elapsed_time)) + " \n";
      STRACE_LOG.write(junk1);
   # end debug

   # Update Maximum write time (if necceasry)
   if (float(elapsed_time) > float(WriteMax["MaxTime"]) ):
       WriteMax["MaxTime"]= elapsed_time;
       WriteMax["line"] = LineNum - 1;
   # end if

   #
   # If unit is > 0 then put write information into data structures
   #   Note: stdin is usually 0 but since we shouldn't be writing to
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
            junk1 = item["filename"];
            break
         # end if
      # end for loop
      
      if (i > 0):
         #
         # Add write data to local dictionary and then use
         #   append function to add to Write data structure
         #
         # Find filename associated with unit
         temp_dict = {};
         temp_dict["line_number"] = int(LineNum);
         temp_dict["sec"] = sec;
         if (int(bytes) >= 0):
            temp_dict["bytes"] = int(bytes);
         else:
            temp_dict["bytes"] = -1;
         # end if
         temp_dict["byte_sec"] = float(bytes)/float(elapsed_time);
         temp_dict["elapsed_time"] = elapsed_time;
         temp_dict["unit"] = unit;
         temp_dict["filename"] = junk1;
         Write.append(temp_dict);
         
         # Increment total bytes written (for all files)
         WriteBytesTotal["sum"] = WriteBytesTotal["sum"] + int(bytes);
         
         # Find File_Stats dictionary corresponding to the current unit
         #
         
         # "unit" is open - now find if the file name is in File_Stats_Pointer
         l = -1;
         File_Stats_pointer = -1;
         for item in File_Stats:
            l = l+1;
            junk2 = item["filename"]
            if ( junk2.lower() == junk1.lower() ):
               File_Stats_pointer = l;
               break;
            # end of
         # end for loop
         if (File_Stats_pointer >= 0):  
            File_Stats[File_Stats_pointer]["write_bytes"] = File_Stats[File_Stats_pointer]["write_bytes"] + int(bytes);
            File_Stats[File_Stats_pointer]["write_rate_sum"] = File_Stats[File_Stats_pointer]["write_rate_sum"] + (float(bytes)/float(elapsed_time));
            File_Stats[File_Stats_pointer]["write_rate_count"] = File_Stats[File_Stats_pointer]["write_rate_count"] + 1;
         else:
            print "In Write processing. File_Stats_pointer is negative - problem";
         # end if
         
         # Update IOPS array
         IOPS_insert(IOPS_info,IOPS,WRITE,sec,BeginTime,unit,debug,STRACE_LOG);
         
         # Update Offset tracking information
         Offset_insert(Offset_info,Offset,sec,BeginTime,bytes,LineNum,unit);
      else:
         junk2 = "In write_processing: Cannot find filename in Open_filename data structure\n";
         STRACE_LOG.write(junk2);
         junk2 = "   unit: " + str(unit) + " \n";
         STRACE_LOG.write(junk2);
         junk1 = "   Line Number = "+str(LineNum)+" \n";
         STRACE_LOG.write(junk1);
         lineOutput = "";
         for tmp in currentline:
            lineOutput = lineOutput + " " + tmp;
         lineOutput = lineOutput + "\n";
         junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
         STRACE_LOG.write(junk2);         
         for item in Open_Filename:
            junk1 = "      "+str(item) + "\n";
            STRACE_LOG.write(junk1);
         # end for
      # End if
   else:
      STRACE_LOG.write("In write_processing: file descriptor on current write call \n");
      STRACE_LOG.write("   is zero or negative \n");
      junk2 = "   unit: " + str(unit) + "\n";
      STRACE_LOG.write(junk2);
      junk2 = "   Line in strace file: " + str(LineNum) + "\n";
      STRACE_LOG.write(junk2);
   # end of "if (unit > 0):"
# end of Write_Processing



       
#
# Process Lseek() syscalls filling data structures
#                    
def Lseek_Processing(currentline, Lseek_obj, IOPS_obj, Open_Filename, LSEEK, elapsed_time,
                     LineNum, sec, BeginTime, debug, STRACE_LOG, CmdCounter):
    # Syscall:
    #    off_t lseek(int fd, off_t offset, int whence);
    # Sample input line:
    #    1252621029.816022 lseek(3, 0, SEEK_SET)   = 0 <0.000005>
    # Sample split line:
    # ['1252621029.816022', 'lseek(3,', '0,', 'SEEK_SET)', '=', '0', '<0.000005>']
    #
    # currentline          # Current split line from strace file
    # Lseek_obj            # Instantiation of Lseek object
                           #    Each line in the object looks like the following:
                           #       LineNum        (line number of strace output file)
                           #       sec            (seconds since epoch when function was called)
                           #       elapsed_time   (elapsed time for open)
                           #       filename       (filename for file being opened)
                           #       unit           (file descriptor associated with file)
                           #       whence         (whence for lseek)
                           #       offset         (offset argument from lseek)
                           #       off_t_result   (final file offset)   
    # Open_Filename;       # List of currently opened files
                           #   Open_Filename[iloop]["unit"] = unit
                           #   Open_Filename[iloop]["filename"] = filename
    # LSEEK                # lseek function keyword
    # elapsed_time         # elapsed time of syscall
    # LineNum              # Current line number
    # sec                  # sec of syscall
    # BeginTime            # Begin time of run
    # debug                # debug flag
    # STRACE_LOG           # Log file (also for debug information)
    # CmdCounter           # Command counter dictionary
   
   
    # Local temporary variables 
    temp_dict = {};              # local temporary dictionary
    print "   in lseek_processing"

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
   
    # Find file name associated with unit
    i = -1;
    for item in Open_Filename:
        if item["unit"] == unit:
            i = 1;
            break
        # end if
    # end for

    if (i > 0):
        k = -1;
        for item in Open_Filename:
            if (item["unit"] == unit):
                k = 1;
                junk1 = item["filename"];
                break;
            # end if
        # end for loop

        if (k > 0):
            # Update Lseek information
            #    Local dictionary
            temp_dict = {};
            junk3 = float(sec) - float(BeginTime);
            temp_dict = {};
            temp_dict["line_number"] = int(LineNum);
            temp_dict["sec"] = sec;
            temp_dict["elapsed_time"] = int(elapsed_time);
            temp_dict["filename"] = filename;
            temp_dict["unit"] = int(unit);
            temp_dict["whence"] = whence;
            temp_dict["offset"] = int(offset);
            temp_dict["off_t_result"] = int(off_t_result);
        else:
            junk2 = "In lseek_processing, cannot find filename in Open_Filename data structure \n";
            STRACE_LOG.write(junk2);
            junk2 = "   unit: " + str(unit) + "\n";
            STRACE_LOG.write(junk2);
            junk2 = "   line number: " + str(currentline) + "\n";
            STRACE_LOG.write(junk2);
            for item in Open_Filename:
                junk1 = "      item:"+str(item)+" \n";
                STRACE_LOG.write(junk1);
            # end for
        # end if
       
        # Append local dictionary to list of dictionaries
        Lseek_ob.storeleek(temp_dict);
    else:
        junk2 = "In lseek_processing, cannot find unit in Open_Filename data structure \n";
        STRACE_LOG.write(junk2);
        junk2 = "   unit: " + str(unit) + "\n";
        STRACE_LOG.write(junk2);
        junk2 = "   line number: " + str(currentline) + "\n";
        STRACE_LOG.write(junk2);
        for item in Open_Filename:
            junk1 = "      item:"+str(item)+" \n";
            STRACE_LOG.write(junk1);
        # end for loop
    # end if
   
    # Insert IOPS into IOPS data structures
    #IOPS_insert(IOPS_info,IOPS,LSEEK,sec,BeginTime,unit,debug,STRACE_LOG);
   
# End of Lseek_Processing






#
# Process LLseek() syscalls filling data structures
#
def LLseek_Processing(currentline,Lseek,Lseek_info,Open_Filename,IOPS_info,IOPS,File_Stats,
                      Offset_info,Offset,LLSEEK,LseekMax,elapsed_time,LineNum,sec,BeginTime,
                      debug,STRACE_LOG,CmdCounter):
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
   # currentline          # Current split line from strace file
   # Lseek                # Lseek information (list of dictionaries
                          #   Lseek[iloop]["pointer"] = pointer to filename in Lseek_info
                          #   Lseek[iloop]["time"] = time
                          #   Lseek[iloop]["counter"] = counter?
   # Lseek_info           # List of dictionaires of lseek information
                          #   Lseek_info[iloop]["filename"] = filename
                          #   Lseek_info[iloop]["unit"] = unit
                          #   Lseek_info[iloop]["pointer"] = pointer to Lseek-info array
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
   # IOPS;                # Main IOPS data structure
   # File_Stats           # File Statistics
                          #   File_stats[iloop]["unit"] = unit
                          #   File_Stats[iloop]["file"] = $filename; 
                          #   File_Stats[iloop]["read_bytes"] += $byte;
                          #   File_Stats[iloop]["write_bytes"] += $byte; 
                          #   File_Stats[iloop]["read_rate_count"]
                          #   File_Stats[iloop]["read_rate_sum"]
                          #   File_Stats[iloop]["write_rate_sum"]
                          #   File_Stats[iloop]["write_rate_count"]
   # Offset_info          # List of dictionaries of offset infomroation
                          #   Offset_info[iloop]["filename"] = filename
                          #   Offset_info[iloop]["unit"] = unit
                          #   Offset_info[iloop]["pointer"] = pointer to Offset_info array
                          #   Offset_info[iloop]["offset_cur"] = Current offset in bytes
   # Offset               # Offset information (list of dictionaries)
                          #   It contains the offset information for all file. They
                          #   distinguished by "pointer" which points to the partifular
                          #   file in Offset_info
                          #   Offset[iloop]["pointer"] = pointer to filename in Offset_info
                          #   Offset[iloop]["time"] = time;
                          #   Offset[iloop]["offset"] = offset (in bytes)
   # LLSEEK               # lseek function keyword
   # LseekMax             # Lseek maximum time dictionary
                          #   LseekMax["MaxTime"] = maximum time
                          #   LseekMax["line"] = line in strace file
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary

   


   # Local temporary variables 
   temp_dict = {};              # local temporary dictionay

   # Find _whence_ by looking for "=" sign (index) and using the previous index
   # Get index for "="
   try:
      i = currentline.index("=");
   except ValueError:
      i = -1 # no match
   #
   junk1 = currentline[i-1];
   whence = junk1[0:len(junk1)-1];

   # Get result of llseek
   junk1 = currentline[i-2];
   j = len(junk1);
   offset = junk1[1:j-2];
   
   # Get success:
   #   Look for "Illegal" in currentline
   k = -1;
   for item in currentline:
      if item == "(Illegal":
         k = 1;
         break
   # end for loop
   
   if (k < 0):
      i = len(currentline);
      success = int(currentline[i-2]);
   
      # Determine unit (file descriptor) - second element of currentline
      junk1 = currentline[1];
      junk2 = junk1.index("(");
      unit = int(junk1[junk2+1:len(junk1)-1]);
   
      # Search Lseek_info for "unit" - if found, pull out filename and pointer
      local_pointer = -2;
      for item in Lseek_info:
         if ( int(item["unit"]) == int(unit) ):
            local_pointer = item["pointer"];
            junk1 = item["offset_cur"];
            break
         # end if
      # end for loop
      if (local_pointer > -2):   
         # Update Lseek information
         #    Local dictionary
         temp_dict = {};
         junk3 = float(sec) - float(BeginTime);
         temp_dict = {};
         temp_dict["unit"] = int(unit);
         temp_dict["pointer"] = local_pointer;
         temp_dict["time"] = junk3;
         temp_dict["counter"] = 1;
         # Append local dictionary to list of dictionaries
         Lseek.append(temp_dict);
      # end if

      if (debug > 0):
         junk1 = "      * llseek_activity: time: "+str(temp)+"  unit: "+str(unit)+"\n";
         STRACE_LOG.write(junk1);
      # end if
      
      #
      # Update Offset tracking information
      #
      #   Step 1 - find "pointer" in Offset_info corresponding to current "unit"
      #            Start by finding "unit" in Open_Filename and the corresponding file
      l = -1;
      for item in Open_Filename:
         if ( int(item["unit"]) == int(unit) ):
            l = 1;
            junk1 = item["filename"];
            #print "   found unit: filename = ",junk1;
            break;
         #end if
      # end for loop
   
      # if l > o then unit was found to be opened - now find filename in Offset_info
      #    and obtain pointer
      if (l > 0):
         m = -1;
         local_pointer = -1;
         local_offset_cur = -1;
         for item in Offset_info:
            m = m + 1;
            if (item["filename"] == junk1):
               local_pointer = item["pointer"];
               local_offset_cur = item["offset_cur"];
               break;
            # end if
         # end for loop
      
         #   Step 2 - insert data into Offset list using "pointer" if it is positive
         if (local_pointer > -2):
            temp_dict = {};
            temp_dict["pointer"] = local_pointer;
            temp_dict["time"] = float(sec) - float(BeginTime);
            temp_dict["offset"] = off_t_result;
            # Append local dictionary to list of dictionaries
            Offset.append(temp_dict);
         
            Offset_info[m]["offset_cur"] = off_t_result;
         else:
            junk2 = "In llseek_processing, cannot find pointer in Offset_info \n";
            STRACE_LOG.write(junk2);
            junk2 = "   Searching for filename:" + str(junk1) + " in Offset_info \n";
            STRACE_LOG.write(junk2);
            junk2 = "   unit:" + str(unit) + " \n";
            STRACE_LOG.write(junk2);
         #end if
         
         # Insert IOPS into IOPS data structures
         IOPS_insert(IOPS_info,IOPS,LLSEEK,sec,BeginTime,unit,debug,STRACE_LOG);
      else:
         junk2 = "In llseek_processing, cannot find unit in Open_Filename data structure \n";
         STRACE_LOG.write(junk2);
         junk2 = "   unit: " + str(unit) + "\n";
         STRACE_LOG.write(junk2);
         junk2 = "   line number: " + str(currentline) + "\n";
         STRACE_LOG.write(junk2);
         for item in Open_Filename:
            junk1 = "      item:"+str(item)+" \n";
            STRACE_LOG.write(junk1);
         # end for loop
         print "In llseek_processing, cannot find unit in Open_Filename data structure ";
         print "   unit: ",unit;
         for item in Open_Filename:
            print "      item: ",item
         # end for
      # end if
      
      # Update lseek maximums
      if (elapsed_time > LseekMax["MaxTime"]):
         LseekMax["MaxTime"] = elapsed_time;
         LseekMax["line"] = LineNum - 1;
      # end if
      
   # end if (k > 0):
# End of LLseek_Processing






#
# Process Close() syscalls filling data structures
#
def Close_Processing(currentline,Close_obj,Open,Open_Filename,IOPS_info,IOPS,CLOSE,CloseMax,
                     CloseMin,elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
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
   # Close                # Close list - actually it's a list of dictionaries
                          #    Close[iloop]["line"] = LineNum
                          #    Close[iloop]["sec"] = sec
                          #    Close[iloop]["elapsed_time"] = elapsed_time;
                          #    Close[iloop]["unit"] = unit;
   # Open                 # Open function call list dictionaries
                          #   Open[iloop]["line_number"] = LineNum;
                          #   Open[iloop]["sec"] = sec;
                          #   Open[iloop]["file"] = filename;
                          #   Open[iloop]["unit"] = unit;
                          #   Open[iloop]["elapsed_time"] = elapsed_time;
   # Open_Filename;       # List of currently opened files
                          #   Open_Filename[iloop]["unit"] = unit
                          #   Open_Filename[iloop]["filename"] = filename
   # Lseek_info;          # Lseek file information
   # Lseek_info           # List of dictionaires of lseek information
                          #   Lseek_info[iloop]["filename"] = filename
                          #   Lseek_info[iloop]["unit"] = unit
                          #   Lseek_info[iloop]["pointer"] = pointer to Lseek-info array
                          #                                 (used to get file name for this offset)
   # IOPS_info            # List of dictionaries of IOPS information
                          #   IOPS_info[iloop]["filename"] = filename
                          #   IOPS_info[iloop]["unit"] = unit
                          #   IOPS_info[iloop]["pointer"] = pointer to Offset array
   # IOPS                 # Total IOPS information (list of dictionaries)
                          #   IOPS[iloop]["time"] = time interval (in seconds)
                          #   IOPS[iloop]["pointer"] = pointer to IOPS_info array
                          #   IOPS[iloop]["type"] = (IOPS Function list)
   # IOPS;                # Main IOPS data structure
   # CLOSE;               # Keyword for close syscall
   # CloseMax             # Close maximum time dictionary
                          #   CloseMax["MaxTime"] = maximum time
                          #   CloseMax["line"] = line in strace file
   # CloseMin             # Close minimum time dictionary
                          #   CloseMin["MinTime"] = minimum time
                          #   CloseMin["line"] = line in strace file
   # elapsed_time         # elapsed time of syscall
   # LineNum              # Current line number
   # sec                  # sec of syscall
   # BeginTime            # Begin time of run
   # debug                # debug flag
   # STRACE_LOG           # Log file (also for debug information)
   # CmdCounter           # Command counter dictionary
   
   
   # temporary variables
   temp_dict = {};
   
   if (debug > 0):
       STRACE_LOG.write("   *** In close_processing routine\n");
   # end if
   
   # Check if close() function was successful
   #    Find success by looking for "=" sign (index) and using the next index
   try:
       i = currentline.index("=");
   except ValueError:
       i = -1 # no match
   junk1 = currentline[i+1];
   success = int(junk1);
   
   if (success == 0):
      # Find unit
      junk1 = currentline[1];
      junk2 = junk1.index("(");
      try:
         junk3 = junk1.index(")");
      except ValueError:
         junk3 = len(junk1);
      #end try
      unit = int(junk1[junk2+1:junk3]);
   
      if (debug > 0):
         STRACE_LOG.write("      In Close_Processing routine \n");
      # end if statement
      
      # Find corresponding file in Open_Filename data structure and erase it
      # because the file is closed
      #    Check if filename exists in Open_Filename
      if (unit > 0):
         # Search Open_Filename list of dictionaries for open file match
         i = -1;
         j = -1;
         for item in Open_Filename:
            j = j+1;
            if int(item["unit"]) == int(unit):
               i = 1;
               break
            # end if
         # end for loop
         
         # Note: We only look for positive units since the program shouldn't try
         #   to close stdin or stdout (or stderr).
         if (i > 0):
             k = -1;
             for item in Open_Filename:
                 if (item["unit"] == unit):
                     k = 1;
                     junk1 = item["filename"];
                     break;
                 #end if
             # end for loop
             if (k < 0):
                 temp_dict["filename"] = junk1;
             else:
                 print "Error in close_processing routine. Cannot find filename \n";
                 print "    associated with unit:",unit;
                 temp_dict["filename"] = " ";
             #end if

             # File exists (it is open)
             #    Update local Close data structure
             temp_dict = {};
             temp_dict["line_number"] = LineNum;
             temp_dict["sec"] = sec;
             temp_dict["unit"] = unit;
             temp_dict["elapsed_time"] = elapsed_time;
             Close_obj.storeclose(self,temp_dict);
            
             if (debug > 0):
                 junk1 = "         unit = " + str(unit) + " \n"
                 STRACE_LOG.write(junk1);
                 junk1 = "         Elapsed time: " + str(elapsed_time) + " \n";
                 STRACE_LOG.write(junk1);
             # end if (debug > 0)
            
             # Remove element corresponding to close unit in Open_Filename data structure
             #   This means that the file is closed
             del Open_Filename[j];
            
             # Insert IOPS into IOPS data structures
             IOPS_insert(IOPS_info,IOPS,CLOSE,sec,BeginTime,unit,debug,STRACE_LOG);
         else:
            junk1 = "In close_processing: cannot find unit in Open_Filename data structure \n";
            STRACE_LOG.write(junk1);
            junk1 = "   Line Number = "+str(LineNum)+" \n";
            lineOutput = "";
            for tmp in currentline:
               lineOutput = lineOutput + " " + tmp;
            lineOutput = lineOutput + "\n";
            if (debug > 0):
               junk2 = "   (" + str(LineNum) + ")   " + lineOutput ;
               STRACE_LOG.write(junk2);
            # end of if
            STRACE_LOG.write(junk1);
            junk1 = "   unit: "+str(unit)+" \n";
            STRACE_LOG.write(junk1);
            lineOutput = "";
            for tmp in currentline:
               lineOutput = lineOutput + " " + tmp;
            lineOutput = lineOutput + "\n";
            junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
            STRACE_LOG.write(junk2);
            for item in Open_Filename:
               junk1 = "      "+str(item) + "\n";
               STRACE_LOG.write(junk1);
            # end for
         # end if (i > 0):
      # end if (unit > 0):
   # end if (success == 0):
# End Close_processing


#
# Process IO functions() syscalls that use a unit and fill data structures
#
def Unit_IO_Processing(currentline,COMMAND,Open_Filename,IOPS_info,IOPS,
                       elapsed_time,LineNum,sec,BeginTime,debug,STRACE_LOG,CmdCounter):
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
   
   # Get unit
   junk1 = currentline[1].split('(')[1];
   junk2 = junk1[0:len(junk1)-1];
   unit = int(junk2);
   
   # See if "unit" is in Open_Filename - if so, store COMMAND information
   i = -1;
   for item in Open_Filename:
      if item["unit"] == unit:
         i = 1;
         break
      # end if
   # end for
   
   if (i > 0):
      # insert data into IOPS data structures
      IOPS_insert(IOPS_info,IOPS,COMMAND,sec,BeginTime,unit,debug,STRACE_LOG);
   else:
      junk1 = "In Unit_IO_Processing for Command: "+COMMAND+" - cannot find unit in Open_File \n";
      STRACE_LOG.write(junk1);
      junk1 = "   unit = "+str(unit)+" \n";
      STRACE_LOG.write(junk1);
      junk1 = "   Line Number = "+str(LineNum)+" \n";
      STRACE_LOG.write(junk1);
      lineOutput = "   Line:: ";
      for tmp in currentline:
         lineOutput = lineOutput + " " + tmp;
      lineOutput = lineOutput + "\n";
      junk2 = "(" + str(LineNum) + ")   " + lineOutput ;
      STRACE_LOG.write(junk2);
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




