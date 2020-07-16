

try:
   from math import sqrt;    # Needed for sqrt function
except ImportError:
   print "Cannot import mat module for sqrt - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   from collections import defaultdict
except:
   print "cannot import defaultdict";
   print "exiting";
   sys.exit();

try:
   import os                 # Needed for mkdir
except ImportError:
   print "Cannot import os module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import matplotlib.pyplot as plt;
   matplotlib_var = 1
except:
   matplotlib_var = 0;
   print "Cannot find matplotlib - will proceed without plots but the data files";
   print "  will still be produced."

try:
   import numpy as np
   numpy_var = 1;
except:
   numpy_var = 0;
   print "Cannot find numpy - will proceed without plots";




from strace_func import *


# =========
# =========
# Functions
# =========
# =========






#
# This routine prints out the basic stats on a per file basis
#
def Per_File_Stats(f, Write_obj, Read_obj, IOPS_obj, CmdCounter, WRITE, READ, dirname):
    #
    #-------------------------
    #-- Per File Statistics -- 
    #-------------------------
    #

    # Table of: Total write bytes (per file), Total read bytes (per file), Peak write rate, Peak read rate, Peak IOPS?

    # First scan through write and read data and gather the list of unique file names

    Local_data = Write_obj.getwrite();
    write_filenames = list( set( [Local_data[i][3] for i in range(0,len(Local_data))] ) );
    Local_data = Read_obj.getread();
    read_filenames = list( set( [Local_data[i][3] for i in range(0,len(Local_data))] ) );
    
    all_filenames = list( set(write_filenames + read_filenames) );
   
    # At this pint, total_filename is the dedup-ed list of filenames used with writes or reads
    
    
    # HTML report output (top of section)
    output_str = " \n";
    output_str = output_str + "<hr /> \n";
    output_str = output_str + "<H3> \n"
    output_str = output_str + "9. <a id=\"per_file_stat\">Per File Statistics</a> \n";
    output_str = output_str + "</H3> \n";
    output_str = output_str + " \n";
    output_str = output_str + "<P> \n";
    f.write(output_str);
    output_str = "This section reports the per file data statistics. It reports the number of bytes \n";
    output_str = output_str + "read, written, the read and write throughput performance in Bytes/s. \n";
    output_str = output_str + "This is done for every file opened. \n";
    output_str = output_str + "</P> \n";
    #output_str = output_str + "<BR> \n";
    f.write(output_str);
   
    # HTML table header:
    output_str = "<P> \n";
    output_str = output_str + "Table 5 below contains information on the lseek function usage in\n";
    output_str = output_str + "various input and output files used by the application. \n";
    output_str = output_str + "<BR><BR><center><strong>Table 5 - Per file data statistics </strong><BR><BR> \n";
    output_str = output_str + "<table border =" + "\"1\" " + "> \n";
    output_str = output_str + "   <tr> \n";
    output_str = output_str + "      <th align=left><font size=\"-2\">File name</font></th> \n";
    output_str = output_str + "      <th align=right><font size=\"-2\">Total Read MB</font></th> \n";
    output_str = output_str + "      <th align=right><font size=\"-2\"><center>Peak Read <BR> throughput (MB/s)</center></font></th> \n";
    output_str = output_str + "      <th align=right><font size=\"-2\"><center>Peak Read IOPS</center></font></th> \n";
    output_str = output_str + "      <th align=right><font size=\"-2\"><center>Total Write MB</center></font></th> \n";
    output_str = output_str + "      <th align=right><font size=\"-2\"><center>Peak Write <BR> throughput (MB/s)</center></font></th> \n";
    output_str = output_str + "      <th align=right><font size=\"-2\"><center>Peak Write IOPS</center></font></th> \n";
    output_str = output_str + "   </tr> \n";
    f.write(output_str);
   
    # File_Stats;                # File Stats array
   
    print " ";
    print " ";
    print("-- File Statistics (per file basis) --\n\n");
    print "Filename                                                                                                Total           Peak Read           Peak Read               Total         Peak Write           Peak Write";
    print "Filename                                                                                              Read MB              MB/sec                IOPS            Write MB              MB/sec                IOPS";
    print "=================================================================================================================================================================================================================="; 
    #      1234567890123456789112345678921234567893123456789412345678951234567896123456789712345678981234567899123456789012345678911234567892123456789312345678941234567895123456789612345678971234567898123456789912345678901234567891
    #      .........0.........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1
    
    # Loop over filenames
    #
    # per_file_list[i] = points to dictionary (list of dictonary)
    #    add filename and unit to dictionary
    #
    
    per_file_highlights = [];    # list of dictionaries
    for item in all_filenames:
        temp_dict = {};
        temp_dict["filename"] = item;    # item is filename
        temp_dict["Write_peak_throughput"] = 0.0;
        temp_dict["Total_write_bytes"] = 0.0;
        temp_dict["Read_peak_throughput"] = 0.0;
        temp_dict["Total_read_bytes"] = 0.0;
        per_file_highlights.append(temp_dict);
    # end for

    # Test searching:
    per_file_highlights = [];    # list of dictionaries
    for item in all_filenames:
        temp_dict = {};
        temp_dict["filename"] = item;    # item is filename
        temp_dict["Write_peak_throughput"] = 0.0;
        temp_dict["Total_write_bytes"] = 0.0;
        temp_dict["Read_peak_throughput"] = 0.0;
        temp_dict["Total_read_bytes"] = 0.0;
        temp_dict["Write_IOPS"] = 0;
        temp_dict["Read_IOPS"] = 0;
        
        search = item;
        
        # Search Write data
        result_write = [element for element in Write_obj.getwrite() if element[3] == search]
        if (len(result_write) > 0):
            Total_write_bytes = 0;
            Write_peak_throughput = 0.0;
            for record in result_write:
                Total_write_bytes = Total_write_bytes + record[5];
                if (record[6] > Write_peak_throughput):
                    Write_peak_throughput = record[6];
                # end if
            # end if
            temp_dict["Write_peak_throughput"] = Write_peak_throughput;
            temp_dict["Total_write_bytes"] = Total_write_bytes;
        # end if
        temp_dict["Write_IOPS"] = len(result_write);
        
        # Search Read data
        result_read = [element for element in Read_obj.getread() if element[3] == search]
        if (len(result_read) > 0):
            Read_peak_throughput = 0.0;
            Total_read_bytes = 0;
            Read_IOPS = 0;
            for record in Read_obj.getread():
                if (record[3] == item):
                    Total_read_bytes = Total_read_bytes + record[5];
                    if (record[6] > Read_peak_throughput):
                        Read_peak_throughput = record[6];
                    # end if
                # end if
            # end if
            temp_dict["Read_peak_throughput"] = Read_peak_throughput;
            temp_dict["Total_read_bytes"] = Total_read_bytes;
        # end if
        temp_dict["Read_IOPS"] = len(result_read);
        
        # Per File IOPS Data:
        local_iops = [element for element in IOPS_obj.getiops() if element[1] == search];   # Get all IOPS data for file
        # Create time intervals for IOPS for this file
        Local_Array = [];
        for item2 in local_iops:
            junk1 = int(item2[3]);
            Local_Array.append(junk1);
        # end for loop
        
        # Count duplicates
        Counts = count_dups(Local_Array);
        
        # Extract the non-duplicate time intervals we need
        Local_Time_Intervals = [];
        for item2 in Counts:
            Local_Time_Intervals.append(item2[0]);
        # end for
        Local_Time_Intervals.sort();        # sort time interval array in ascending order
        
        # Search for Peak Write IOPS
        if (CmdCounter[WRITE] > 0):
            sum1_write = 0;
            itotal_write = 0;             # Total number of WRITE function
            IOPS_Write_peak = 0;          # Peak Write IOPS
            
            for item2 in Local_Time_Intervals:
                sum1_write = 0;
                for record in local_iops:
                    if ( (record[4] == WRITE) and (record[3] == item2) ):
                        sum1_write = sum1_write + 1;      # add the Write IOPS in this particular time interval
                    # end if
                # end for loop
                if (sum1_write > IOPS_Write_peak):
                    IOPS_Write_peak = sum1_write;
                # end if
            # end for loop
        # end if
        temp_dict["Peak_Write_IOPS"] = IOPS_Write_peak;
        
        # Search for Peak Read IOPS
        if (CmdCounter[READ] > 0):
            sum1_read = 0;
            itotal_read = 0;             # Total number of WRITE function
            IOPS_Read_peak = 0;          # Peak Write IOPS
            
            for item2 in Local_Time_Intervals:
                sum1_read = 0;
                for record in local_iops:
                    if ( (record[4] == READ) and (record[3] == item2) ):
                        sum1_read = sum1_read + 1;      # add the Write IOPS in this particular time interval
                    # end if
                # end for loop
                if (sum1_read > IOPS_Read_peak):
                    IOPS_Read_peak = sum1_read;
                # end if
            # end for loop
        # end if
        temp_dict["Peak_Read_IOPS"] = IOPS_Read_peak;
        per_file_highlights.append(temp_dict);
        
        # stdout:
        # file name
        junk1 = temp_dict["filename"];
        junk2 = junk1.ljust(89," ");
        # read bytes
        junk3 = temp_dict["Total_read_bytes"]/1000000.0;
        junk3a = "%.4f" % junk3;
        junk3b = commify3(junk3a);
        junk4 = junk3b.rjust(19," ");
        # Reads MB/sec
        junk5 = temp_dict["Read_peak_throughput"]/1000000.0;
        junk5a = "%.4f" % junk5;
        junk5b = commify3(junk5a);
        junk5c = junk5b.rjust(19," ");
        # Read IOPS:
        junk6 = temp_dict["Peak_Read_IOPS"];
        junk6b = commify3(junk6);
        junk6c = junk6b.rjust(19," ");
        # write bytes
        junk7 = temp_dict["Total_write_bytes"]/1000000.0;
        junk7a = "%.4f" % junk7;
        junk7b = commify3(junk7a);
        junk8 = junk7b.rjust(19," ");
        # Write MB/sec
        junk9 = temp_dict["Write_peak_throughput"]/1000000.0;
        junk9a = "%.4f" % junk9;
        junk9b = commify3(junk9a);
        junk9c = junk9b.rjust(19," ");
        # Write IOPS:
        junk10 = temp_dict["Peak_Write_IOPS"];
        junk10b = commify3(junk10);
        junk10c = junk10b.rjust(19," ");
        
        print junk2,junk4,junk5c,junk6c,junk8,junk9c,junk10c;  # stdout
        
        # HTML
        junk1 = temp_dict["filename"];
        junk2 = temp_dict["Total_read_bytes"];
        junk2a = junk2/1000000.0;    #(MB)
        junk2b = "%.4f" % junk2a;
        junk2c = commify3(junk2b);
        junk3 = temp_dict["Read_peak_throughput"];
        junk3a = junk3/1000000.0;    #(MB)
        junk3b = "%.4f" % junk3a
        junk3c = commify3(junk3b);
        junk4 = temp_dict["Total_write_bytes"];
        junk4a = junk2/1000000.0;    #(MB)
        junk4b = "%.4f" % junk4a
        junk4c = commify3(junk4b);
        junk5 = temp_dict["Write_peak_throughput"];
        junk5a = junk5/1000000.0;    #(MB)
        junk5b = "%.4f" % junk5a
        junk5c = commify3(junk5b);
        junk6 = commify3(IOPS_Read_peak);
        junk7 = commify3(IOPS_Write_peak);
        
        output_str = "   <tr> \n";
        output_str = output_str + "      <td align=left><font size=\"-2\">" + junk1 + "</font></td> \n";
        output_str = output_str + "      <td align=right><font size=\"-2\">" + junk2c + "</font></td> \n";
        output_str = output_str + "      <td align=right><font size=\"-2\">" + junk3c + "</font></td> \n";
        output_str = output_str + "      <td align=right><font size=\"-2\">" + junk6 + "</font></td> \n";
        output_str = output_str + "      <td align=right><font size=\"-2\">" + junk4c + "</font></td> \n";
        output_str = output_str + "      <td align=right><font size=\"-2\">" + junk5c + "</font></td> \n";
        output_str = output_str + "      <td align=right><font size=\"-2\">" + junk7 + "</font></td> \n";
        output_str = output_str + "   </tr> \n";
        f.write(output_str);
    # end for
     
    # Close HTML table
    # HTML - close table
    output_str = "</table></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    output_str = output_str + " \n";
    f.write(output_str);
    
# end def Per_File_Stats():




#
# Performance Output (data and plots)
#
def Performance_Output(f, currentfigure, VFLAGS, Write_obj, Read_obj, IOPS_obj, BeginTime, EndTime,
                       input_filename):
    #
    # Data needed:
    #    f             - file descriptor for output file
    #    basefigure    - Starting plot number
    #    currentfigure - currentfigure number (running total) - may need to return this value
    #    BeginTime     - Beginning time of run
    #    EndTime       - Time when run finished
    #    CmdCounter    - Command Counter dictionary
    #    WRITE         - Command Counter for Writes
    #    READ          - Command Cunter for reads
    #    Write         - List of dictionaries of write data
    #    Read          - List of dictionaries of read data
    #    IOPS          - IOPS list
   
    # Write_obj.throughtput_max        # Maximum write throughput (scalar in Bytes/s)
    # Write_obj.throughput_max_time    # When does maximum write throughput happen during run
    # Write_obj.throughput_min         # Minimum write throughput (scalar in Bytes/s)
    # Write_obj.throughput_min_time    # When does minimum write throughput happen during run
    # Write_obj.throughput_max_MB      # Maximum write throughput (scalar in MB/s)
    # Write_obj.throughput_min_MB      # Minimum write throughput (scalar in MB/s)
   
    # Read_obj.throughtput_max         # Maximum read throughput (scalar in Bytes/s)
    # Read_obj.throughput_max_time     # When does maximum read throughput happen during run
    # Read_obj.throughput_min          # Minimum read throughput (scalar in Bytes/s)
    # Read_obj.throughput_min_time     # When does minimum read throughput happen during run
    # Read_obj.throughput_max_MB       # Maximum read throughput (scalar in MB/s)
    # Read_obj.throughput_min_MB       # Minimum read throughput (scalar in MB/s)

    # IOPS_obj.IOPS_Write_peak         # Peak Write IOPS
    # IOPS_obj.IOPS_Write_peak_time    # Time interval where Peak Write IOPS occurs
    # IOPS.obj.IOPS_Read_Final         # Overall average Write IOPS
    # IOPS_obj.IOPS_Read_peak          # Peak Read IOPS
    # IOPS_obj.IOPS_Read_peak_time     # Time interval where Peak Read IOPS occurs
    # IOPS_obj.IOPS_Read_Final         # Overall average Read IOPS
    # IOPS_obj.IOPS_Total_peak         # Peak Total IOPS
    # IOPS_obj.IOPS_Total_peak_time    # Time interval where Peak Total IOPS occurs
    # IOPS_obj.IOPS_Total_Final        # Overall average Total IOPS



    # HTML: (top of section)
    output_str = " \n\n";
    output_str = output_str + "<hr /> \n";
    output_str = output_str + "<H3> \n"
    output_str = output_str + "10. <a id=\"perf_section\">Performance Summary</a> \n";
    output_str = output_str + "</H3> \n";
    output_str = output_str + " \n";
    output_str = output_str + "<P> \n";
    output_str = output_str + "This section presents the performance information from the application. \n";
    output_str = output_str + "It presents the write and read throughput (MB/s) as a function of time \n";
    output_str = output_str + "and the write and read IOPS as a function of time. \n";
    f.write(output_str);
    if (VFLAGS >= 2):
        output_str = "There is also a plot of the Total IOPS as a function of time. \n";
        f.write(output_str);
    # end if
    output_str = "</P> \n \n";
    f.write(output_str);

    # Performance summary here (text + HTML):
    # Write
    junk2 = "%.4f" % Write_obj.throughput_max_MB;
    junk2a = commify3(junk2);
    junk3 = "%.4f" % Write_obj.throughput_max_time;
    junk3a = commify3(junk3);
    junk4 = "%.4f" % Write_obj.throughput_min_MB;
    junk4a = commify3(junk4);
    junk5 = "%.4f" % Write_obj.throughput_min_time;
    junk5a = commify3(junk5);
    
    output_str = output_str + "Performance summary: \n";
    output_str = output_str + "<UL> \n";
    f.write(output_str);
    output_str = "   <LI>Write Throughput: \n";
    output_str = output_str + "   <UL> \n";
    f.write(output_str);
    output_str = "      <LI>Maximum Write Throughput: " + junk2a + " MB/s \n";
    output_str = output_str + "      <UL> \n";
    output_str = output_str + "         <LI>Occured at " + junk3a + " seconds \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "      <LI>Minimum Write Throughput = " + junk4a + " MB/s \n";
    output_str = output_str + "      <UL> \n";
    output_str = output_str + "         <LI>occurred at " + junk5a + " seconds \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "   </UL> \n";
    f.write(output_str);
    
    # Read
    junk2 = "%.4f" % Read_obj.throughput_max_MB;
    junk2a = commify3(junk2);
    junk3 = "%.4f" % Read_obj.throughput_max_time;
    junk3a = commify3(junk3);
    junk4 = "%.4f" % Read_obj.throughput_min_MB;
    junk4a = commify3(junk4);
    junk5 = "%.4f" % Read_obj.throughput_min_time;
    junk5a = commify3(junk5);
     
    output_str = "   <LI>Read Throughput: \n";
    output_str = output_str + "   <UL> \n";
    f.write(output_str);
    output_str = "      <LI>Maximum Read Throughput: " + junk2a + " MB/s \n";
    output_str = output_str + "      <UL> \n";
    output_str = output_str + "         <LI>Occured at " + junk3a + " seconds \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "      <LI>Minimum Read Throughput = " + junk4a+ " MB/s \n";
    output_str = output_str + "      <UL> \n";
    output_str = output_str + "         <LI>occurred at " + junk5a + " seconds \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "   </UL> \n";
    f.write(output_str);
    
    # IOPS
    # IOPS_obj.IOPS_Write_peak         # Peak Write IOPS
    # IOPS_obj.IOPS_Write_peak_time    # Time interval where Peak Write IOPS occurs
    # IOPS.obj.IOPS_Write_Final         # Overall average Write IOPS
    # IOPS_obj.IOPS_Read_peak          # Peak Read IOPS
    # IOPS_obj.IOPS_Read_peak_time     # Time interval where Peak Read IOPS occurs
    # IOPS_obj.IOPS_Read_Final         # Overall average Read IOPS
    # IOPS_obj.IOPS_Total_peak         # Peak Total IOPS
    # IOPS_obj.IOPS_Total_peak_time    # Time interval where Peak Total IOPS occurs
    # IOPS_obj.IOPS_Total_Final        # Overall average Total IOPS


    junk2a = commify3(IOPS_obj.IOPS_Write_peak);
    junk3 = "%.4f" % IOPS_obj.IOPS_Write_peak_time;
    junk3a = commify3(junk3);
    junk4 = "%.4f" % IOPS_obj.IOPS_Write_Final;
    junk4a = commify3(junk4);
    
    junk5a = commify3(IOPS_obj.IOPS_Read_peak);
    junk6 = "%.4f" % IOPS_obj.IOPS_Read_peak_time;
    junk6a = commify3(junk6);
    junk7 = "%.4f" % IOPS_obj.IOPS_Read_Final;
    junk7a = commify3(junk7);
    
    junk8a = commify3(IOPS_obj.IOPS_Total_peak);
    junk9 = "%.4f" % IOPS_obj.IOPS_Total_peak_time;
    junk9a = commify3(junk9);
    junk10 = "%.4f" % IOPS_obj.IOPS_Total_Final;
    junk10a = commify3(junk10);

    output_str = "   <LI>IOPS: \n";
    f.write(output_str);
    output_str = "   <UL> \n";
    output_str = output_str + "      <LI>Write: \n";
    output_str = output_str + "      <UL> \n";
    output_str = output_str + "         <LI>Peak Write IOPS: " + junk2a + " \n";
    output_str = output_str + "         <UL> \n";
    output_str = output_str + "            <LI>Occured at " + junk3a + " seconds \n";
    output_str = output_str + "         </UL> \n";
    output_str = output_str + "         <LI>Average Write IOPS: " + junk4a+ " \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "      <LI>Read: \n";
    output_str = output_str + "      <UL> \n";
    output_str = output_str + "         <LI>Peak Read IOPS: " + junk5a+ " \n";
    output_str = output_str + "         <UL> \n";
    output_str = output_str + "            <LI>Occured at " + junk6a + " seconds \n";
    output_str = output_str + "         </UL> \n";
    output_str = output_str + "         <LI>Average Read IOPS: " + junk7a + " \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "      <LI>Total: \n";
    output_str = output_str + "         <LI>Peak Total IOPS: " + junk8a + " \n";
    output_str = output_str + "         <UL> \n";
    output_str = output_str + "            <LI>Occured at " + junk9a + " seconds \n";
    output_str = output_str + "         </UL> \n";
    output_str = output_str + "         <LI>Average Total IOPS: " + junk10a + " \n";
    output_str = output_str + "      </UL> \n";
    output_str = output_str + "   </UL> \n";
    f.write(output_str);
    output_str = "</UL> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    
    if (VFLAGS >= 2):
        # ==========
        # Two plots: Top plot is write throughput (MB/s) versus time
        #            Bottom plot is Write IOPS versus time
        #
        # Figure +1: (x = time, y = write_syscall_throughput_all -> upper plot
        #             x = time, y = iops_write  -> lower plot
        # ==========
        write_syscall_throughput_all_MB = [(x / 1000000.0) for x in Write_obj.write_syscall_throughput_all ];   # Convert throughput to MB/s

        
        title = input_filename;    # name of input file
        xaxis_title_1 = "Time (secs)";
        yaxis_title_1 = "Write Throughput (MB/s)";
        xaxis_title_2 = "Time (secs)";
        yaxis_title_2 = "Write IOPS";
        output_file_name = "./HTML_REPORT/write_throughput_iops.png";
        # Plot1: X = Write_obj.time, y = Write_obj.write_syscall_throughput_all
        # Plot2: X = IOPS_obj.Time_Intervals  y = IOPS_Obj.IOPS_Write_Plot
        Plot_2_1(Write_obj.time, write_syscall_throughput_all_MB,
                 IOPS_obj.Time_Intervals_Write, IOPS_obj.IOPS_Write_Plot, title, xaxis_title_1, yaxis_title_1, 
                 xaxis_title_2, yaxis_title_2, output_file_name);
        
        # HTML:
        currentfigure = currentfigure + 1;
        output_str = "<P> \n";
        output_str = output_str + "Figure " + str(currentfigure) + " below has two plots. The \n";
        output_str = output_str + "upper plot is of the write \n";
        output_str = output_str + "throughput in MB/s versus application run time. The \n";
        output_str = output_str + "lower plot is of the Write IOPS versus application run time. \n";
        output_str = output_str + "Note that application run time means that the time is normalized \n";
        output_str = output_str + "to the application start time. So when the application starts \n";
        output_str = output_str + "the time is zero. \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "<center> \n";
        output_str = output_str + "<img src=\"write_throughput_iops.png\"> \n";
        output_str = output_str + "<BR><strong>Figure " + str(currentfigure) + " - Upper Plot: \n";
        output_str = output_str + "Write Throughput (MB/s) \n";
        output_str = output_str + "versus time (seconds). Lower Plot: Write IOPS versus time \n";
        output_str = output_str + "(seconds)</strong></center><BR><BR> \n";
        output_str = output_str + "</P> \n";
        f.write(output_str);
        
        #
        # ==========
        # Two plots: Top plot is read throughput (MB/s) versus time
        #            Bottom plot is Read IOPS versus time
        #
        # Figure +1: (x = time, y = write_syscall_throughput_all -> upper plot
        #             x = time, y = iops_write  -> lower plot
        # ==========
        #
        read_syscall_throughput_all_MB = [(x / 1000000.0) for x in Read_obj.read_syscall_throughput_all ];   # Convert throughput to MB/s
        
        title = input_filename;    # name of input file
        xaxis_title_1 = "Time (secs)";
        yaxis_title_1 = "Read Throughput (MB/s)";
        xaxis_title_2 = "Time (secs)";
        yaxis_title_2 = "Read IOPS";
        output_file_name = "./HTML_REPORT/read_throughput_iops.png";
        Plot_2_1(Read_obj.time, read_syscall_throughput_all_MB,
                 IOPS_obj.Time_Intervals_Read, IOPS_obj.IOPS_Read_Plot, title, xaxis_title_1, yaxis_title_1, 
                 xaxis_title_2, yaxis_title_2, output_file_name);
        
        # HTML:
        currentfigure = currentfigure + 1;
        output_str = "<P> \n";
        output_str = output_str + "Figure " + str(currentfigure) + " below has two plots. The \n";
        output_str = output_str + "upper plot is of the read \n";
        output_str = output_str + "throughput in MB/s versus application run time. The \n";
        output_str = output_str + "lower plot is of the Read IOPS versus application run time. \n";
        output_str = output_str + "Note that application run time means that the time is normalized \n";
        output_str = output_str + "to the application start time. So when the application starts \n";
        output_str = output_str + "the time is zero. \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "<center> \n";
        output_str = output_str + "<img src=\"read_throughput_iops.png\"> \n";
        output_str = output_str + "<BR><strong>Figure " + str(currentfigure) + " - Upper \n";
        output_str = output_str + "Plot: Read Throughput (MB/s) \n";
        output_str = output_str + "versus time (seconds). Lower Plot: Read IOPS versus time \n";
        output_str = output_str + "(seconds)</strong></center><BR><BR> \n";
        output_str = output_str + "</P> \n";
        f.write(output_str);
        
        # Write IOPS - single plot
        currentfigure = currentfigure + 1;
        output_str = "<P> \n";
        output_str = output_str + "Figure " + str(currentfigure) + " below is a time history of the Write IOPS in one \n";
        output_str = output_str + "second intervals. <BR>\n";
        f.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"write_iops_time_history.png\"> \n";
        output_str = output_str + "<BR><strong>Figure " + str(currentfigure) + " - Write IOPS Time ";
        output_str = output_str + "history</strong></center><BR><BR> \n";
        output_str = output_str + "</P> <BR> \n";
        f.write(output_str);
        
        # Read IOPS
        currentfigure = currentfigure + 1;
        output_str = "<BR> <BR> \n";
        f.write(output_str);
        output_str = "<P> \n";
        output_str = output_str + "Figure " + str(currentfigure) + " below is a time history of the Read IOPS in one \n";
        output_str = output_str + "second intervals. <BR>\n";
        f.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"read_iops_time_history.png\"> \n";
        output_str = output_str + "<BR><strong>Figure " + str(currentfigure) + " - Read IOPS Time ";
        output_str = output_str + "history</strong></center><BR><BR> \n";
        output_str = output_str + "</P> <BR> \n";
        f.write(output_str);
        
        # Total IOPS
        currentfigure = currentfigure + 1;
        output_str = "<BR> <BR> \n";
        f.write(output_str);
        output_str = "<P> \n";
        output_str = output_str + "Figure " + str(currentfigure) + " below is a time history of the Total IOPS in one \n";
        output_str = output_str + "second intervals. <BR>\n";
        f.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"total_iops_time_history.png\"> \n";
        output_str = output_str + "<BR><strong>Figure " + str(currentfigure) + " - Total IOPS Time ";
        output_str = output_str + "history</strong></center><BR><BR> \n";
        output_str = output_str + "</P> <BR> \n \n";
        f.write(output_str);
    # end if
     
    return currentfigure;

# end def



#
# Aggregate Plots
#
def Aggregate_Plots(f, currentfigure, input_filename, BeginTime, EndTime, Write_obj, Read_obj, IOPS_obj):
    
    # HTML: (top of section)
    output_str = " \n\n";
    output_str = output_str + "<hr /> \n";
    output_str = output_str + "<H3> \n"
    output_str = output_str + "11. <a id=\"plots_section\">Aggregate Plots</a> \n";
    output_str = output_str + "</H3> \n";
    output_str = output_str + " \n";
    output_str = output_str + "<P> \n";
    output_str = output_str + "This section presents some plots of various parameters to help \n";
    output_str = output_str + "with interpreting the results. There may be quite a few plots. \n";
    output_str = output_str + "</P> \n ";
    f.write(output_str);
    
    # ==========
    # Figure +1: (x = time, y = write_syscall_size_all_MB -> upper plot
    #             x = time, y = iops_write  -> lower plot
    # ==========
    #Write_obj.getbytes(BeginTime);   # write_syscall_size_all
    write_syscall_throughput_all_MB = [(x / 1000000.0) for x in Write_obj.write_syscall_throughput_all ];   # Convert throughput to MB/s
    write_syscall_size_all_MB = [(x / 1000000.0) for x in Write_obj.write_syscall_size_all ];   # Convert syscall size to MB
    
    title = str(input_filename);
    xaxis_title_1 = "Time (secs)";
    yaxis_title_1 = "Write syscall (MB)";
    xaxis_title_2 = "Time (secs)";
    yaxis_title_2 = "Write IOPS";
    output_file_name = "./HTML_REPORT/write_syscall_iops.png";
    
    Plot_2_1(Write_obj.time, write_syscall_size_all_MB,
             IOPS_obj.Time_Intervals_Write, IOPS_obj.IOPS_Write_Plot,
             title, xaxis_title_1, yaxis_title_1, 
             xaxis_title_2, yaxis_title_2, output_file_name);
    #Plot_2_1(time, write_syscall_size_all, xdata2, write_iops, title, xaxis_title_1, yaxis_title_1, 
    #        xaxis_title_2, yaxis_title_2, output_file_name);
     
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below has two plots. The \n";
    output_str = output_str + "upper plot is of the write \n";
    output_str = output_str + "system call size in bytes versus application run time. The \n";
    output_str = output_str + "lower plot is of the Write IOPS versus application run time. \n";
    output_str = output_str + "Note that application run time means that the time is normalized \n";
    output_str = output_str + "to the application start time. So when the application starts \n";
    output_str = output_str + "the time is zero. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"write_syscall_iops.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Upper Plot: \n";
    output_str = output_str + "Write Syscall Size (Bytes) \n";
    output_str = output_str + "versus time (seconds). Lower Plot: Write IOPS versus time \n";
    output_str = output_str + "(seconds)</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);

    # ==========
    # Figure +2: (x = time, y = write_syscall_throughput_all_MB -> upper plot
    #             x = time, y = iops_write  -> lower plot
    # ==========
    
    title = input_filename;    # name of input file
    xaxis_title_1 = "Time (secs)";
    yaxis_title_1 = "Write Throughput (MB/s)";
    xaxis_title_2 = "Time (secs)";
    yaxis_title_2 = "Write IOPS";
    output_file_name = "./HTML_REPORT/write_throughput_iops.png";
    Plot_2_1(Write_obj.time, write_syscall_throughput_all_MB, 
             IOPS_obj.Time_Intervals_Write, IOPS_obj.IOPS_Write_Plot,
             title, xaxis_title_1, yaxis_title_1, 
             xaxis_title_2, yaxis_title_2, output_file_name);
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below has two plots. The \n";
    output_str = output_str + "upper plot is of the write \n";
    output_str = output_str + "throughput in MB/s versus application run time. The \n";
    output_str = output_str + "lower plot is of the Write IOPS versus application run time. \n";
    output_str = output_str + "Note that application run time means that the time is normalized \n";
    output_str = output_str + "to the application start time. So when the application starts \n";
    output_str = output_str + "the time is zero. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"write_throughput_iops.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Upper Plot: \n";
    output_str = output_str + "Write Throughput (MB/s) \n";
    output_str = output_str + "versus time (seconds). Lower Plot: Write IOPS versus time \n";
    output_str = output_str + "(seconds)</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    # ===========
    # Figure + 3: (x = time, y = write_syscall_size_all_cumulative)
    # ===========
    #
    # Plots cummlative write total over time
    #
    junk2 = 0.0;
    xdata3 = [];
    ydata3 = [];
    if (len(Write_obj.writedata) > 0 ):
        for item in Write_obj.writedata:
            junk = item[1];    # sec
            junk1 = float((float(junk)-float(BeginTime)));
            xdata3.append(junk1);
            junk2 = junk2 + item[5];   # bytes
            junk3 = junk2/1000000.0;   # in MB
            ydata3.append(junk3);
        # end for
    # end if
    
    # JEFFWASHERE - may be able to get rid of the following 3 lines
    ydata3.append(0.0);
    junk = (float(float(EndTime)-float(BeginTime)));
    xdata3.append(junk);
    
    title = input_filename;    # name of input file
    xaxis_title_1 = "Time (secs)";
    yaxis_title_1 = "Cummlative Write Total (MB)";
    output_file_name = "./HTML_REPORT/write_syscall_size_all_cumulative.png";
    Plot_1_1(xdata3, ydata3, title, xaxis_title_1, yaxis_title_1, output_file_name);
    xdata3 = [];
    ydata3 = [];
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below is a plot of \n";
    output_str = output_str + "the cummlative write data (in MB) \n";
    output_str = output_str + "versus application run time. Note that application run time means \n";
    output_str = output_str + "that the time is normalized to the application start time. So \n";
    output_str = output_str + "when the application starts the time is zero. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"write_syscall_size_all_cumulative.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Cummlative \n";
    output_str = output_str + "Write Size (MB) \n";
    output_str = output_str + "versus time (seconds)</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    
    # ===========
    # Fifgure +4: # Write syscall distribution
    # ===========
    #     The x axis data is the size of the write syscall in bytes
    #     The y axis data is the number of write syscalls with that value.
    #
    Local_Array = [];
    # Step 1 - extract syscall size values into array
    for item in Write_obj.writedata:
        junk1 = int(item[5]);
        Local_Array.append(junk1);
    # end for loop
    # Count duplicates
    Counts = count_dups(Local_Array) 
    
    xdata4 = [];
    ydata4 = [];
    for item in Counts:
        xdata4.append(int(item[0]));
        ydata4.append(int(item[1]));
    # end for loop
    
    title = input_filename;    # name of input file
    xaxis_title_1 = "Write syscall size (Bytes)";
    yaxis_title_1 = "Number of syscalls";
    output_file_name = "./HTML_REPORT/write_syscall_distribution.png";
    Plot_1_1(xdata4, ydata4, title, xaxis_title_1, yaxis_title_1, output_file_name);
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below is a plot of the \n";
    output_str = output_str + "write() system call distribution. \n";
    output_str = output_str + "It plots the size of the write() system call on the x-axis and \n";
    output_str = output_str + "the number of times that size is used in the y-axis. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"write_syscall_distribution.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Write() \n";
    output_str = output_str + "System Call Distribution \n";
    output_str = output_str + "</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    # ==========
    # Figure +5:
    # ==========
    #
    # Read syscall (MB) for all files over Read IOPS
    #   Output file is read_syscal_iops.png
    #
    #Read_obj.getbytes(BeginTime);   # write_syscall_size_all
    read_syscall_throughput_all_MB = [(x / 1000000.0) for x in Read_obj.read_syscall_throughput_all ];   # Convert throughput to MB/s
    read_syscall_size_all_MB = [(x / 1000000.0) for x in Read_obj.read_syscall_size_all ];   # Convert syscall size to MB
    
    
    title = str(input_filename);    # name of input file
    xaxis_title_1 = "Time (secs)";
    yaxis_title_1 = "Read syscall (MB)";
    xaxis_title_2 = "Time (secs)";
    yaxis_title_2 = "Read IOPS";
    output_file_name = "./HTML_REPORT/read_syscall_iops.png";
    Plot_2_1(Read_obj.time, read_syscall_size_all_MB,
             IOPS_obj.Time_Intervals_Read, IOPS_obj.IOPS_Read_Plot,
             title, xaxis_title_1, yaxis_title_1, 
             xaxis_title_2, yaxis_title_2, output_file_name);
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below has two plots. The \n";
    output_str = output_str + "upper plot is of the read \n";
    output_str = output_str + "system call size in bytes versus application run time. The \n";
    output_str = output_str + "lower plot is of the Read IOPS versus application run time. \n";
    output_str = output_str + "Note that application run time means that the time is normalized \n";
    output_str = output_str + "to the application start time. So when the application starts \n";
    output_str = output_str + "the time is zero. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"read_syscall_iops.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Upper Plot: ";
    output_str = output_str + "Read Syscall Size (Bytes) \n";
    output_str = output_str + "versus time (seconds). Lower Plot: Read IOPS versus time \n";
    output_str = output_str + "(seconds)</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    # ==========
    # Figure +6:
    # ==========
    # Read throughput (MB/s) for all files over Read IOPS
    #   Output file is read_throughput_iops.png
    #./pyplot2_4.py read_syscall_throughput_all.dat iops_read.dat
    #
    xaxis_title_1 = "Time (secs)";
    yaxis_title_1 = "Read Throughput (MB/s)";
    xaxis_title_2 = "Time (secs)";
    yaxis_title_2 = "Read IOPS";
    output_file_name = "./HTML_REPORT/read_throughput_iops.png";
    Plot_2_1(Read_obj.time, read_syscall_throughput_all_MB, 
             IOPS_obj.Time_Intervals_Read, IOPS_obj.IOPS_Read_Plot,
             title, xaxis_title_1, yaxis_title_1, 
             xaxis_title_2, yaxis_title_2, output_file_name);
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below has two plots. The \n";
    output_str = output_str + "upper plot is of the read \n";
    output_str = output_str + "throughput in MB/s versus application run time. The \n";
    output_str = output_str + "lower plot is of the Read IOPS versus application run time. \n";
    output_str = output_str + "Note that application run time means that the time is normalized \n";
    output_str = output_str + "to the application start time. So when the application starts \n";
    output_str = output_str + "the time is zero. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"read_throughput_iops.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Upper \n";
    output_str = output_str + "Plot: Read Throughput (MB/s) \n";
    output_str = output_str + "versus time (seconds). Lower Plot: Read IOPS versus time \n";
    output_str = output_str + "(seconds)</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    
    # ==========
    # Figure +7: read_syscall_size_all_cumulative.dat
    # ==========
    #
    # Read syscall cumulative (MB) for all files
    #   Output file is read_syscall_size_cumulative.png
    #
    junk2 = 0.0;
    xdata7 = [];
    ydata7 = [];
    if (len(Read_obj.readdata) > 0 ):
        for item in Read_obj.readdata:
            junk = item[1];
            junk1 = float((float(junk)-float(BeginTime)));
            xdata7.append(junk1);
            junk2 = junk2 + item[5];
            junk3 = junk2/1000000.0;   # in MB
            ydata7.append(junk3);
         # end for
    # end if
    
    # JEFFWASHERE - may be able to get rid of the following 3 lines
    ydata7.append(0.0);
    junk = (float(float(EndTime)-float(BeginTime)));
    xdata7.append(junk);
    
    # JEFFWASHERE - may be able to get rid of the following 3 lines
    ydata3.append(0.0);
    junk = (float(float(EndTime)-float(BeginTime)));
    xdata3.append(junk);
    
    title = input_filename;    # name of input file
    xaxis_title_1 = "Time (secs)";
    yaxis_title_1 = "Cummlative Read Total (MB)";
    output_file_name = "./HTML_REPORT/read_syscall_size_all_cumulative.png";
    Plot_1_1(xdata7, ydata7, title, xaxis_title_1, yaxis_title_1, output_file_name);
    xdata7 = [];
    ydata7 = [];
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below is a plot of \n";
    output_str = output_str + "the cummlative read data (in MB) \n";
    output_str = output_str + "versus application run time. Note that application run time means \n";
    output_str = output_str + "that the time is normalized to the application start time. So \n";
    output_str = output_str + "when the application starts the time is zero. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"read_syscall_size_all_cumulative.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Cummlative \n";
    output_str = output_str + "Read Size (MB) \n";
    output_str = output_str + "versus time (seconds)</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    
    # ==========
    # Figure +8: read_syscall_distribution.dat
    # ==========
    #
    # Read syscall distribution
    #   Output file is read_syscall_distribution.png
    #
    #     The x axis data is the size of the read syscall in bytes
    #     The y axis data is the number of read syscalls with that value.
    #
    Local_Array = [];
    # Step 1 - extract syscall size values into array
    for item in Read_obj.readdata:
        junk1 = int(item[5]);
        Local_Array.append(junk1);
    # end for loop
    # Count duplicates
    Counts = count_dups(Local_Array) 
    
    xdata8 = [];
    ydata8 = [];
    for item in Counts:
        xdata8.append(int(item[0]));
        ydata8.append(int(item[1]));
    # end for loop
    title = input_filename;    # name of input file
    xaxis_title_1 = "Read syscall size (Bytes)";
    yaxis_title_1 = "Number of syscalls";
    output_file_name = "./HTML_REPORT/read_syscall_distribution.png";
    Plot_1_1(xdata8, ydata8, title, xaxis_title_1, yaxis_title_1, output_file_name);
    xdata8 = [];
    ydata8 = [];
    
    # HTML:
    currentfigure = currentfigure + 1;
    output_str = "<P> \n";
    output_str = output_str + "Figure " + str(currentfigure) + " below is a plot of \n";
    output_str = output_str + "the read() system call distribution. \n";
    output_str = output_str + "It plots the size of the read() system call on the x-axis and \n";
    output_str = output_str + "the number of times that size is used in the y-axis. \n";
    output_str = output_str + "<BR><BR> \n";
    output_str = output_str + "<center> \n";
    output_str = output_str + "<img src=\"read_syscall_distribution.png\"> \n";
    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " - Read() \n";
    output_str = output_str + "System Call Distribution \n";
    output_str = output_str + "</strong></center><BR><BR> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    return currentfigure;
# end def




#
# Individual plot routines
#
def Individual_plots(f, VFLAGS, currentfigure, BeginTime, EndTime, 
                     input_filename, Write_obj, Read_obj, Open_obj, IOPS_obj,
                     READ, WRITE):
    
    output_str = "<H3>\n";
    output_str = output_str + "<hr /> \n";
    output_str = output_str + "12. <a id=\"individual_file_perf\">Individual File Performance</a> \n";
    output_str = output_str + "</H3> \n";
    output_str = output_str + " \n";
    output_str = output_str + "<P>\n";
    output_str = output_str + "This section plots the write and read performance for each \n";
    output_str = output_str + "file that is opened by this application. For each file there \n";
    output_str = output_str + "are the following plots. \n";
    output_str = output_str + "<OL> \n";
    output_str = output_str + "   <LI>Two subplots: upper is write() payload size versus time and \n";
    output_str = output_str + "       the lower is write IOPS versus time \n";
    output_str = output_str + "   <LI>Two subplots: upper is write() throughput in MB/s versus time and \n";
    output_str = output_str + "       the lower is write IOPS versus time \n";
    output_str = output_str + "   <LI>Two subplots: upper is read() payload size versus time and \n";
    output_str = output_str + "       the lower is read IOPS versus time \n";
    output_str = output_str + "   <LI>Two subplots: upper is read() throughput in MB/s versus time and \n";
    output_str = output_str + "       the lower is read IOPS versus time \n";
    output_str = output_str + "   <LI>Just the write IOPS \n";
    output_str = output_str + "   <LI>Just the read IOPS \n";
    output_str = output_str + "   <LI>Just the total IOPS \n";
    output_str = output_str + "</OL> \n";
    f.write(output_str);
    output_str = "If no writing was performed to the file then a comment is made and no write \n";
    output_str = output_str + "plots are created. The same is true for reads - if no reading \n";
    output_str = output_str + "was done to the file then a comment is made and no read plots \n";
    output_str = output_str + "are created. \n"
    output_str = output_str + "</P> \n";
    f.write(output_str);
    output_str = " \n";
    output_str = output_str + "<P> \n";
    output_str = output_str + "Keep in mind that if your application uses a number of shared object \n";
    output_str = output_str + "libraries (.so files), then you will likely see a number of them below \n";
    output_str = output_str + "since the application reads them to load them. Since it is unknown if \n";
    output_str = output_str + "what the application is actually doing, the IO information of these \n";
    output_str = output_str + "files is left in this report. Apologies if that is annoying. \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
   
    # Loop over all files and create hyperlinked list
    output_str = "<P> \n";
    f.write(output_str);
    output_str = "Below is a list of the files that have IO plots. You can click on them \n";
    output_str = output_str + "to link to the specific plot files. \n";
    output_str = output_str + "<OL> \n";
    f.write(output_str);
    
    
    # Scan through write and read data and gather the list of unique file names
    Local_data = Write_obj.getwrite();
    write_filenames = list( set( [Local_data[i][3] for i in range(0,len(Local_data))] ) );
    Local_data = Read_obj.getread();
    read_filenames = list( set( [Local_data[i][3] for i in range(0,len(Local_data))] ) );
    
    # Go through the Open class and pull out all filenames
    Local_data = Open_obj.getopen();
    open_filenames = list( set( [Local_data[i][2] for i in range(0,len(Local_data))] ) );
    
    # Create final list of all possible file names used by application
    all_filenames = list( set(read_filenames + write_filenames + open_filenames) );
    
    # List of root directories where applications are not likely to write
    file_blacklist = [];
    if (VFLAGS == 3):
        file_blacklist.append("bin");
        file_blacklist.append("boot");
        file_blacklist.append("dev");
        file_blacklist.append("etc");
        file_blacklist.append("lib");
        file_blacklist.append("lib32");
        file_blacklist.append("lib64");
        file_blacklist.append("media");
        file_blacklist.append("proc");
        file_blacklist.append("root");
        file_blacklist.append("sbin");
        file_blacklist.append("srv");
        file_blacklist.append("sys");
        file_blacklist.append("user");
        file_blacklist.append("usr");
        file_blacklist.append("var");
    # end if
    
    # Write out hyperlinked file names for easier navigation
    # ------------------------------------------------------
    for item in all_filenames:
        
        # Check if file name is in "blacklist"
        filename_split = splitall(item);
        if (len(filename_split) == 1):
            comp_string = filename_split[0];
        else:
            comp_string = filename_split[1];
        #end if
        if (comp_string not in file_blacklist):
            output_str = "   <LI><a href=\"#" + item + "\">" + item + "</a> \n";
            f.write(output_str);
        # end if
    # end if
    output_str = "</OL> \n";
    output_str = output_str + "</P> \n";
    f.write(output_str);
    
    
    # Loop over all files and make plots
    # ----------------------------------
    iloop = 0;
    for item in all_filenames:
        
        # Check if file name is in "blacklist"
        filename_split = splitall(item);
        if (len(filename_split) == 1):
            comp_string = filename_split[0];
        else:
            comp_string = filename_split[1];
        # end if
        
        if (comp_string not in file_blacklist):
            # Create HTML H4 section for particular file
            output_str = "<H4>\n";
            output_str = output_str + "Plots for file: <a id=\"" + item + "\">" + item + "</a> \n";
            output_str = output_str + "</H4> \n";
            output_str = output_str + " \n";
            f.write(output_str);
            
            # -----------
            # Write Plots
            # -----------
            
            # Gather write data
            Local_Write = [];    # Used for gathering write data for particular file
            Local_Dict = {};     # Temporary data structure
            # Loop over Write data structure looking for a filename match
            #   if it matches copy data to local dictionary and then append it to list (Local_Write)
            for record in Write_obj.writedata:
                if (record[3] == item):
                    Local_Dict["sec"] = record[1];
                    Local_Dict["bytes"] = record[5];
                    Local_Dict["byte_sec"] = record[6];
                    Local_Write.append(Local_Dict);
                # end if
            # end for loop
            
            # If there is data in the list then proceed (i.e. write() IO has been done to this file)
            if (len(Local_Write) > 0):
                
                #
                # --------
                # Plot #1: Write syscall size (bytes) at top + Write throughput (MB/s) at bottom
                # --------
                #
                currentfigure = currentfigure + 1;    # Increment figure number
                
                # Definitions for plot names and location
                output_file_name = "./HTML_REPORT/write_syscall_size_throughput_"+str(currentfigure)+".png";
                
                # Initialize local data arrays
                xdata1 = [];
                ydata1 = [];
                xdata2 = [];
                ydata2 = [];
                xdata1.append(0.0);
                ydata1.append(0.0);
                xdata2.append(0.0);
                ydata2.append(0.0);
                
                # Loop over Local_Write and extract required data. Put data
                #    into lists for plotting
                for thing in Local_Write:
                    junk4 = thing["sec"];
                    junk4_out = float((float(junk4)-float(BeginTime)));
                    xdata1.append(junk4_out);    # time relative to start of application
                    
                    junk6 = thing["bytes"];
                    ydata1.append(junk6);        # Write() payload size in Bytes
                    
                    junk5 = float(thing["byte_sec"]);   # Throughput
                    ydata2.append(junk5);        # Throughput in Bytes/s
                # end for loop
                # Add final data point (end of run)
                junk5 = float(EndTime) - float(BeginTime);
                xdata1.append(junk5);
                xdata2 = xdata1;       # second copy of data (needed for plotting)
                ydata1.append(0.0);
                ydata2.append(0.0);
                ydata2_MB = [(x / 1000000.0) for x in ydata2 ];   # Convert throughput to MB/s
                
                # Titles and labels for plot
                title = "File: " + item;    # name of input file
                xaxis_title_1 = "Time (secs)";
                yaxis_title_1 = "Write syscall (Bytes)";
                xaxis_title_2 = "Time (secs)";
                yaxis_title_2 = "Write Throughput (MB/s)";
                Plot_2_1(xdata1, ydata1, xdata2, ydata2_MB, title, xaxis_title_1, yaxis_title_1, 
                         xaxis_title_2, yaxis_title_2, output_file_name);
                
                # Create the HTML for the plot
                output_str = "<P> \n";
                output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + ", \n";
                output_str = output_str + "shown below has two plots. The upper plot \n";
                output_str = output_str + "is of the write system call size in MB versus application run \n";
                output_str = output_str + "time. The lower plot is of the Write throughput in MB/s versus \n";
                output_str = output_str + "application run time. Note that application run time means that \n";
                output_str = output_str + "the time is normalized to the application start time. So when \n";
                output_str = output_str + "the application starts the time is zero. \n";
                output_str = output_str + "<BR><BR> \n";
                output_str = output_str + "<center> \n";
                output_file_name2 = "write_syscall_size_throughput_"+str(currentfigure)+".png";
                output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                output_str = output_str + " - Upper Plot: Write Syscall Size (Bytes) \n";
                output_str = output_str + "versus time (seconds). Lower Plot: Write Throughput (MB/s) \n";
                output_str = output_str + "versus time (seconds)</strong></center><BR><BR> \n";
                output_str = output_str + "</P> \n";
                f.write(output_str);
                
                #
                # Compute Write IOPS
                #
                Local_IOPS_Write = [];
                for item2 in IOPS_obj.iopsdata:
                    if ( (item2[1] == item) and (item2[4] == WRITE) ):   # filename matches and IO is a write
                        Local_IOPS_Write.append(item2);    # Create local array of Write IOPS data
                    # end if
                # end for
                
                if (len(Local_IOPS_Write) > 0):
                    #
                    # --------
                    # Plot #2: Write throughput (MB/s) at top +  Write IOPS at bottom
                    # --------
                    #
                    currentfigure = currentfigure + 1;
                    
                    xdata3 = [];
                    ydata3 = [];
                    xdata3.append(0);
                    ydata3.append(0);
                    for item2 in IOPS_obj.Time_Intervals:
                        isum = 0;
                        for item3 in Local_IOPS_Write:
                            if (item3[3] == item2):
                                isum = isum + 1;
                            # end if
                        # end if
                        xdata3.append(item2);
                        ydata3.append(isum);
                    # end for
                    # Checking beginning time:
                    junk1 = (float(EndTime)-float(BeginTime));
                    xdata3.append(junk1);
                    ydata3.append(0.0);
                    
                    # Create the second plot (throughput at top and IOPS at bottom)
                    output_file_name = "./HTML_REPORT/write_throughput_write_iops_"+str(currentfigure)+".png";
                    title = "File: " + item;    # name of input file
                    xaxis_title_1 = "Time (secs)";
                    yaxis_title_1 = "Write throughput (MB/s)";
                    xaxis_title_2 = "Time (secs)";
                    yaxis_title_2 = "Write IOPS";
                    Plot_2_1(xdata1, ydata2_MB, xdata3, ydata3, title, xaxis_title_1, yaxis_title_1, 
                             xaxis_title_2, yaxis_title_2, output_file_name);
                    
                    # HTML for plot
                    
                    output_str = "<P> \n";
                    output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + " \n";
                    output_str = output_str + "shown below has two plots. The upper plot is of the Write \n";
                    output_str = output_str + "throughput in MB/s versus application run time. The lower \n";
                    output_str = output_str + "plot is of the Write IOPS versus application time. The \n";
                    output_str = output_str + "plots are for the file " + item + ". Note that application  \n";
                    output_str = output_str + "run time means that the time is normalized to the application \n";
                    output_str = output_str + "start time. So when the application starts the time is zero. \n";
                    output_str = output_str + "<BR><BR> \n";
                    output_str = output_str + "<center> \n";
                    output_file_name2 = "write_throughput_write_iops_"+str(currentfigure)+".png";
                    output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                    output_str = output_str + " - Upper Plot: Write Throughput (MB/s) \n";
                    output_str = output_str + "versus time (seconds). Lower Plot: Write IOPS \n";
                    output_str = output_str + "versus time (seconds)</strong></center><BR><BR> \n";
                    output_str = output_str + "</P> \n";
                    f.write(output_str);
                    
                    #
                    # --------
                    # Plot #3: Write IOPS only
                    # --------
                    #
                    currentfigure = currentfigure + 1;
                    output_file_name = "./HTML_REPORT/write_iops_"+str(currentfigure)+".png";
                    
                    title = "File: " + item;    # name of input file
                    xaxis_title_1 = "Time (secs) - Relative to beginning of run";
                    yaxis_title_1 = "Write IOPS";
                    Plot_1_1(xdata3, ydata3, title, xaxis_title_1, yaxis_title_1, output_file_name);
                    
                    # HTML Output:
                    output_str = "<P> \n";
                    output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + " \n";
                    output_str = output_str + "shown below plots the time history of the Write IOPS for this \n";
                    output_str = output_str + "file. \n";
                    output_str = output_str + "<BR><BR> \n";
                    output_str = output_str + "<center> \n";
                    output_file_name2 = "write_iops_"+str(currentfigure)+".png";
                    output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                    output_str = output_str + " - Write IOPS versus Application Time (seconds)</strong></center><BR><BR> \n";
                    output_str = output_str + "</P> \n";
                    f.write(output_str); 
                else:
                    print "No Write IOPS - seems to be a problem";
                # end if 
            # end if

            # ----------
            # Read Plots
            # ----------
            
            # Gather write data
            Local_Read = [];     # Used for gathering read data for particular file
            Local_Dict = {};     # Temporary data structure
            # Loop over Read data structure looking for a filename match
            #   if it matches print to the data files
            for record in Read_obj.readdata:
                if (record[3] == item):
                    Local_Dict["sec"] = record[1];
                    Local_Dict["bytes"] = record[5];
                    Local_Dict["byte_sec"] = record[6];
                    Local_Read.append(Local_Dict);
                # end if
            # end for loop
            
            if (len(Local_Read) > 0):
                #
                # --------
                # Plot #4: Read syscall size (bytes) at top + Read throughput (MB/s) at bottom
                # --------
                #
                currentfigure = currentfigure + 1;
                
                # Definitions for plot names and locations
                output_file_name = "./HTML_REPORT/read_syscall_size_throughput_"+str(currentfigure)+".png";
                
                # Initialize local data arrays
                xdata5 = [];
                ydata5 = [];
                xdata6 = [];
                ydata6 = [];
                xdata5.append(0.0);
                ydata5.append(0.0);
                xdata6.append(0.0);
                ydata6.append(0.0);
                
                # Loop over Local_Read and write to output files
                for thing in Local_Read:
                    junk4 = thing["sec"];
                    junk4_out = float((float(junk4)-float(BeginTime)));
                    xdata5.append(junk4_out);          # time
                    
                    junk6 = thing["bytes"];
                    ydata5.append(junk6);              # Read() payload size in Bytes
                    
                    junk5 = float(thing["byte_sec"]);   # Throughput
                    ydata6.append(junk5);              # Throughput in Bytes/s
                # end for loop
                # Add final data point (end of run)
                junk5 = float(EndTime) - float(BeginTime);
                xdata5.append(junk5);
                xdata6 = list(xdata5);       # second copy of data
                ydata5.append(0.0);
                ydata6.append(0.0);
                ydata6_MB = [(x / 1000000.0) for x in ydata6 ];   # Convert throughput to MB/s
                
                # Create the first plot (syscall size at top and throughput at bottom)
                #   syscall in bytes, throughput in MB/S
                title = "File: " + item;    # name of input file
                xaxis_title_1 = "Time (secs)";
                yaxis_title_1 = "Read syscall (Bytes)";
                xaxis_title_2 = "Time (secs)";
                yaxis_title_2 = "Read Throughput (MB/s)";
                Plot_2_1(xdata5, ydata5, xdata6, ydata6_MB, title, xaxis_title_1, yaxis_title_1, 
                         xaxis_title_2, yaxis_title_2, output_file_name);
                
                # Create the HTML for the plot
                output_str = "<P> \n";
                output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + " \n";
                output_str = output_str + "shown below has two plots. The upper plot \n";
                output_str = output_str + "is of the read system call size in MB versus application run \n";
                output_str = output_str + "time. The lower plot is of the Read throughput in MB/s versus \n";
                output_str = output_str + "application run time. Note that application run time means that \n";
                output_str = output_str + "the time is normalized to the application start time. So when \n";
                output_str = output_str + "the application starts the time is zero. \n";
                output_str = output_str + "<BR><BR> \n";
                output_str = output_str + "<center> \n";
                output_file_name2 = "read_syscall_size_throughput_"+str(currentfigure)+".png";
                output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                output_str = output_str + " - Upper Plot: Read Syscall Size (Bytes) \n";
                output_str = output_str + "versus time (seconds). Lower Plot: Read Throughput (MB/s) \n";
                output_str = output_str + "versus time (seconds)</strong></center><BR><BR> \n";
                output_str = output_str + "</P> \n";
                f.write(output_str);
                
                
                #
                # Compute Read IOPS
                #
                Local_IOPS_Read = [];
                for item2 in IOPS_obj.iopsdata:
                    if ( (item2[1] == item) and (item2[4] == READ) ):
                        Local_IOPS_Read.append(item2);    # Create local array of Read IOPS data (filename matches)
                    # end if
                # end for
            
                if (len(Local_IOPS_Read) > 0):
                    #
                    # --------
                    # Plot #5: Read syscall size (bytes) at top + Read throughput (MB/s) at bottom
                    # --------
                    #
                    currentfigure = currentfigure + 1;
                    
                    output_file_name = "./HTML_REPORT/read_throughput_read_iops_"+str(currentfigure)+".png";
                    xdata7 = [];
                    ydata7 = [];
                    xdata7.append(0);
                    ydata7.append(0);
                    for item2 in IOPS_obj.Time_Intervals:
                        isum = 0;
                        for item3 in Local_IOPS_Read:
                            if (item3[3] == item2):
                                isum = isum + 1;
                            # end if
                        # end if
                        xdata7.append(item2);
                        ydata7.append(isum);
                    # end for
                    # Checking beginning time:
                    junk1 = (float(EndTime)-float(BeginTime));
                    xdata7.append(junk1);
                    ydata7.append(0.0);
                    
                    # Create the second plot (throughput at top and IOPS at bottom)
                    title = "File: " + item;    # name of input file
                    xaxis_title_1 = "Time (secs)";
                    yaxis_title_1 = "Read throughput (MB/s)";
                    xaxis_title_2 = "Time (secs)";
                    yaxis_title_2 = "Read IOPS";
                    Plot_2_1(xdata5, ydata6_MB, xdata7, ydata7, title, xaxis_title_1, yaxis_title_1, 
                             xaxis_title_2, yaxis_title_2, output_file_name);
            
                    # HTML for plot
                    output_str = "<P> \n";
                    output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + " \n";
                    output_str = output_str + "shown below has two plots. The upper plot is of the Read \n";
                    output_str = output_str + "throughput in MB/s versus application run time. The lower \n";
                    output_str = output_str + "plot is of the Read IOPS versus application time. The \n";
                    output_str = output_str + "plots are for the file " + item + ". Note that application  \n";
                    output_str = output_str + "run time means that the time is normalized to the application \n";
                    output_str = output_str + "start time. So when the application starts the time is zero. \n";
                    output_str = output_str + "<BR><BR> \n";
                    output_str = output_str + "<center> \n";
                    output_file_name2 = "read_throughput_read_iops_"+str(currentfigure)+".png";
                    output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                    output_str = output_str + " - Upper Plot: Read Throughput (MB/s) \n";
                    output_str = output_str + "versus time (seconds). Lower Plot: Read IOPS \n";
                    output_str = output_str + "versus time (seconds)</strong></center><BR><BR> \n";
                    output_str = output_str + "</P> \n";
                    f.write(output_str); 
                    
                    #
                    # --------
                    # Plot #6: Read IOPS only
                    # --------
                    #
                    currentfigure = currentfigure + 1;
                    
                    output_file_name = "./HTML_REPORT/read_iops_"+str(currentfigure)+".png";
                    
                    # Create the plot
                    title = "File: " + item;    # name of input file
                    xaxis_title_1 = "Time (secs) - Relative to beginning of run";
                    yaxis_title_1 = "Read IOPS";
                    Plot_1_1(xdata7, ydata7, title, xaxis_title_1, yaxis_title_1, output_file_name);
            
                    # HTML Output:
                    output_str = "<P> \n";
                    output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + " \n";
                    output_str = output_str + "shown below plots the time history of the Read IOPS for this \n";
                    output_str = output_str + "file. \n";
                    output_str = output_str + "<BR><BR> \n";
                    output_str = output_str + "<center> \n";
                    output_file_name2 = "read_iops_"+str(currentfigure)+".png";
                    output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                    output_str = output_str + " - Read IOPS versus Application Time (seconds)</strong></center><BR><BR> \n";
                    output_str = output_str + "</P> \n";
                    f.write(output_str); 
                # end if
            # end Read

            # -------------------------
            # Pure Total IOPS goes last
            # -------------------------
            Local_IOPS_Total = [];
            for item2 in IOPS_obj.iopsdata:
                if (item2[1] == item):
                    Local_IOPS_Total.append(item2)
                # end if
            # end for
            
            if (len(Local_IOPS_Total) > 0):
                #
                # --------
                # Plot #7: Read syscall size (bytes) at top + Read throughput (MB/s) at bottom
                # --------
                #
                currentfigure = currentfigure + 1;
                    
                output_file_name = "./HTML_REPORT/read_throughput_read_iops_"+str(currentfigure)+".png";
                xdata9 = [];
                ydata9 = [];
                xdata9.append(0);
                ydata9.append(0);
                for item2 in IOPS_obj.Time_Intervals:
                    isum = 0;
                    for item3 in Local_IOPS_Total:
                        if (item3[3] == item2):
                            isum = isum + 1;
                        # end if
                    # end if
                    xdata9.append(item2);
                    ydata9.append(isum);
                # end for
                # Checking beginning time:
                junk1 = (float(EndTime)-float(BeginTime));
                xdata9.append(junk1);
                ydata9.append(0.0);
                
                # File name
                output_file_name = "./HTML_REPORT/total_iops_single_plot_"+str(currentfigure)+".png";
               
                # Create the plot
                title = "File: " + item;    # name of input file
                xaxis_title_1 = "Time (secs) - Relative to beginning of run";
                yaxis_title_1 = "Total IOPS";
                Plot_1_1(xdata9, ydata9, title, xaxis_title_1, yaxis_title_1, output_file_name);
               
                # HTML for plot
                output_str = "<P> \n";
                output_str = output_str + "Figure " + str(currentfigure) + " for file: " + item + " \n";
                output_str = output_str + "shown below plots the time history of the Total IOPS for this \n";
                output_str = output_str + "file. \n";
                output_str = output_str + "<BR><BR> \n";
                output_str = output_str + "<center> \n";
                output_file_name2 = "total_iops_single_plot_"+str(currentfigure)+".png";
                output_str = output_str + "<img src=\"" + output_file_name2 + "\"> \n";
                output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: " + item + "\n";
                output_str = output_str + " - Total IOPS versus Application Time (seconds)</strong></center><BR><BR> \n";
                output_str = output_str + "</P> \n";
                f.write(output_str); 
            # end if (Total)
        # end if  (file not in blacklist)
    # end for
    
    return currentfigure;
# end def


#
# One plot
#
def Plot_1_1(xdata1, ydata1, title, xaxis_title_1, yaxis_title_1, output_file_name):
    #
    # Data needed:
    #   xdata1
    #   ydata1
    #   Title
    #   x-axis title
    #   y-axis title
    #
    #   output file name
    
    fig = plt.figure()
    plt.plot(xdata1,ydata1,'o')
    plt.xlabel(xaxis_title_1, fontsize='x-small');
    plt.ylabel(yaxis_title_1, fontsize='x-small');
    plt.title(title, fontsize='x-small');
    plt.xticks(fontsize='x-small');
    plt.yticks(fontsize='x-small');
    
    fig.autofmt_xdate();
    
    plt.savefig(output_file_name);
    plt.close();
    
# end def



#
# Two plots (one above the other)
#
def Plot_2_1(xdata1, ydata1, xdata2, ydata2, title, xaxis_title_1, yaxis_title_1, 
             xaxis_title_2, yaxis_title_2, output_file_name):
    #
    # Data needed:
    #   xdata1
    #   ydata1
    #   Title
    #   x-axis title
    #   y-axis title
    #   
    #   xdata2
    #   ydata2
    #   x-axis title 2
    #   y-axis titale 2
    #
    #   output file name
    
    # Upper plot
    fig = plt.figure();
    plt.subplot(211)
    plt.plot(xdata1,ydata1,'o')
    plt.xlabel(xaxis_title_1, fontsize='x-small');
    plt.ylabel(yaxis_title_1, fontsize='x-small');
    plt.title(title, fontsize='x-small');
    plt.xticks(fontsize='x-small');
    plt.yticks(fontsize='x-small');
    
    # Lower plot (IOPS)
    plt.subplot(212)
    plt.plot(xdata2,ydata2,'x');
    plt.xlabel(xaxis_title_2, fontsize='x-small');
    plt.ylabel(yaxis_title_2, fontsize='x-small');
    plt.xticks(fontsize='x-small');
    plt.yticks(fontsize='x-small');
    
    # Adjust x-axis labels
    fig.autofmt_xdate();
    
    # Create .png
    plt.savefig(output_file_name);
    #plt.show();
    plt.close();
    
# end def




