#!/usr/bin/python
#
# Copyright 2008-2014 Jeffrey B. Layton
#


#
# Import standard Python modiles if it is available
#
try:
     import matplotlib.pyplot as plt;
except:
     print "Cannot find matplotlib - needed for producing plots.";
     print "Stopping.";
     sys.exit();
# end try

#
# Import NUMPY Python module
try:
   import numpy as np
   numpy_var = 1;
except:
   numpy_var = 0;
   print "Cannot find numpy - will proceed without plots";
# end try




#
# Import python modules from other strace_analyzer files
#
try:
    from strace_func import *
except:
    print "Cannot find strace_func python file. This is needed for this application.";
    print "Stopping.";
    sys.exit();
# end try

try:
    from strace_output import *
except:
    print "Cannot find strace_output python file. This is needed for this application.";
    print "Stopping.";
    sys.exit();
# end try




#
#
# Write() Class definition
#
#
class writeclass:

# Instantiated Object stores data as self.writedata. This is a list of lists (2D list).
# Each row of the list consists of a record. Each record consists of:
#
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor associated with file)
#   bytes          (Number of bytes actually written)
#   bytes_sec      (Bytes per second = bytes/elapsed_time)
#
# There are methods (functions) that add, read, extract, and manipulate
# this data. Many of these methods store results as part of the object
#
#
    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.writedata = [];
    # end def
    
    
    #
    # This function appenda data to self.writedata
    #
    def storewrite(self,data):
        self.writedata.append(data);
    # end def
    
    
    #
    # Return the list to caller
    #
    def getwrite(self):
        return self.writedata;
    # end def
    
    
    #
    # Check if there is any write data
    #
    def anydata(self):
        if (len(self.writedata) > 0):
            return 1;
        else:
            return 0;
        # end if
    # end def
    
    
    #
    # Compute statistics on self.writedata
    #
    def getstats(self, BeginTime, EndTime):
        if (len(self.writedata) > 0):
            #
            # Initialization
            #
            bytes = [];
            self.write_syscall_throughput_all = [];
            self.write_syscall_size_all = [];
            self.time = [];
            
            syscall_size_min = 10000000.0;
            syscall_size_min_line = -1.0;
            syscall_size_max = 0.0;
            syscall_size_max_line = -1.0;
            
            WriteSmall = 1000000000;
            WriteLarge = -1;
            total_write_bytes = 0;
            throughput_min = 100000000.0;
            thoughtput_max = 0.0;
            throughput_min_time = -1.0;
            throughput_max_time = -1.0;
            
            #
            # Extract all the byte information (bytes per write() call) and time data
            #    Also find the following:
            #        1. largest and smallest number of bytes in write() calls
            #        2. Total number of bytes
            #        3. write() system throughput (bytes/s). This is stored into an array.
            #        4. Min and Max system throughput
            #
            for item in self.writedata:
                bytes.append(item[5]);
                self.write_syscall_size_all.append(item[5]);
                junk1 = float((float(item[1])-float(BeginTime)));
                
                # Syscall size
                if (item[2] > syscall_size_max):
                    syscall_size_max = item[2];
                    syscall_size_max_line = item[0];
                elif (item[2] < syscall_size_min):
                    syscall_size_min = item[2];
                    syscall_size_min_line = item[0];
                # endif
                
                # Throughput
                if (item[5] > WriteLarge):
                    WriteLarge = item[5];
                # end if
                if (item[5] < WriteSmall):
                    WriteSmall = item[5];
                # end if
                total_write_bytes = total_write_bytes + item[5];
                
                self.time.append(junk1);
                junk3 = float(item[6]);
                self.write_syscall_throughput_all.append(junk3);   # Bytes/s
                if (junk3 < throughput_min):
                    throughput_min = junk3;
                    throughput_min_time = junk1;
                elif (junk3 > thoughtput_max):
                    thoughtput_max = junk3;
                    throughput_max_time = junk1;
                # end if
            # end for
            
            # Add last data point so the entire time range gets plotted
            #   Note: Leave bytes() alone since it's used for stats and can be changed
            #         Make copy of bytes() data to self.bytes()
            junk1 = float( float(EndTime)-float(BeginTime) );
            self.time.append(junk1);
            self.write_syscall_size_all.append(0.0);
            self.write_syscall_throughput_all.append(0.0);
            self.bytes = list(bytes);
            self.bytes.append(0.0);
            
            # Store results min and max data in dictionary in object
            WriteMax = {};
            WriteMin = {};
            WriteMax["MaxTime"] = syscall_size_max;
            WriteMax["line"] = syscall_size_max_line;
            WriteMin["MinTime"] = syscall_size_min;
            WriteMin["line"] = syscall_size_min_line;
            self.WriteMax = WriteMax;                         # Maximum Write dictionary
            self.WriteMin = WriteMin;                         # Minimum Write dictionary
            self.WriteSmall = WriteSmall;                     # scalar - smallest write
            self.WriteLarge = WriteLarge;                     # scalar - largest write
            
            # Store results in object
            self.throughput_max = thoughtput_max;             # Maximum write throughput (scalar in Bytes/s)
            self.throughput_max_time = throughput_max_time;   # When does maximum write throughput happen during run
            self.throughput_min = throughput_min;             # Minimum write throughput (scalar in Bytes/s)
            self.throughput_min_time = throughput_min_time;   # When does minimum write throughput happen during run  
            self.throughput_max_MB = thoughtput_max/1000000.0;   # Maximum write throughput (scalar in MB/s)
            self.throughput_min_MB = throughput_min/1000000.0;   # Minimum write throughput (scalar in MB/s)       
            self.total_write_bytes = total_write_bytes;
            
            #
            # Compute statistics on write() payload
            #
            self.arthimetic_mean = arithmean(bytes);                          # Arthimetic Mean (average)
            self.sigma_am = std_dev(bytes, self.arthimetic_mean)              # Standard Deviation around Arthimentic Mean
            self.mode = My_Mode(bytes);                                       # Mode  (returns a list)
            self.write_range = max(bytes) - min(bytes);                       # Range
            self.variance = self.sigma_am*self.sigma_am;                      # Variance
            self.mad = my_abs_deviation(bytes, self.arthimetic_mean);         # Mean Absolute Deviation
            self.mse = (self.variance)/float(len(bytes));                     # Mean Squared Error (MSE)
            self.median = my_median(bytes);                                   # Median
            self.sigma_median = std_dev(bytes, self.median);                  # Standard Deviation around Median
            self.median_variance = self.sigma_median*self.sigma_median;       # Median Variance
            self.medianad = my_abs_deviation(bytes, self.median);             # Median Absolute Deviation
            self.mse_median = self.median_variance/float(len(bytes));         # Median Squared Error (MSE)
            self.skewness_mean = my_skewness(bytes, self.arthimetic_mean);    # Fisher-Pearson Generalized moment (skewness measure) - g1
            self.FP_coeff = my_fp_coeff(bytes, self.arthimetic_mean);         # Adjusted Fisher-Pearson standardized moment coefficient - G1
            self.sk2 = my_sk2(self.arthimetic_mean, self.median, self.sigma_am);   # SK2 (Pearson 2 skewness coefficient)
            self.kurtosis_v1 = my_kurtosis(bytes, self.arthimetic_mean);           # Kurtosis
        else:
            #
            # If there are no write() calls then just "zero" out stats
            #
            self.time = [];
            self.bytes = [];
            self.total_write_bytes = 0;
            self.arthimetic_mean = 0.0;
            self.sigma_am = 0.0;
            self.mode = [];
            self.write_range = 0;
            self.variance = 0.0;
            self.mad = 0.0;
            self.mse = 0.0;
            self.median = 0.0;
            self.sigma_median = 0.0;
            self.median_variance = 0.0;
            self.medianad = 0.0;
            self.mse_median = 0.0;
            self.skewness_mean = 0.0;
            self.FP_coeff = 0.0;
            self.sk2 = 0.0;
            self.kutosis_v1 = 0.0;
        
            self.WriteMax = [];
            self.WriteMIn = [];
            self.WriteSmall = 0.0;
            self.WriteLarge = 0.0;
            self.throughput_max = 0.0;
            self.throughput_max_time = 0.0;
            self.throughput_max_MB = 0.0;
            self.throughput_min_MB = 0.0;
            self.write_syscall_throughput_all = [];
        # end if
    # end def
    
    
    
    #
    # Write write() statistics to stdout and HTML
    #
    def write_statistics(self, f, dirname, FileSizes, FileSizeCounter, BeginTime,
                         EndTime, currentfigure, VFLAGS, matplotlib_var, numpy_var,
                         CmdCounter, WRITE):
        #
        # Compute write statistics
        #
        self.getstats(BeginTime, EndTime);
        
        #
        # Write out statistics output section header (stdout and HTML)
        #
        self.stats_header(f);
        
        #
        # Write File Size Interval Summary - Compute intervals first
        #
        self.file_interval_output(f, FileSizes, FileSizeCounter);

        #
        # Create Histograms of Write payload size using matplotlib (for HTML)
        #
        if (VFLAGS >= 2):
            if ( (matplotlib_var > 0) and (numpy_var > 0) ):
                output_str = "<P>The next set of plots are histograms of the payload size for write() \n";
                output_str = output_str + "function calls. Below is a set of hyperlinks so you can jump to \n";
                output_str = output_str + "the plots or the final statistics. \n";
                f.write(output_str);
                
                # Print out orderlist (OL) with hyper links to figures
                self.orderlist_output(f, currentfigure);
                
                # HTML output
                str1 = str((currentfigure + 1));
                str2 = str((currentfigure + 2));
                str3 = str((currentfigure + 3));
                output_str = "<P>The first figure, Figure "+str1+", plots the write()\n";
                output_str = output_str + "payload size in bytes for the entire range used in the application. \n";
                output_str = output_str + "The remaining plots are plotted in Byte, KB, MB, GB, and TB-TB+ \n";
                output_str = output_str + "ranges for better visualization. They start with Figure "+str1+" to plot \n";
                output_str = output_str + "the entire range, Figure "+str2+" for the Byte range, Figure "+str3+" for the \n";
                output_str = output_str + "KB range, and so on. If there no payloads in that range then there \n";
                output_str = output_str + "will be no plot and there will be some text stating that. \n";
                output_str = output_str + "<BR><BR>";
                f.write(output_str);
                
                # Plot histogram over entire range
                if (len(self.bytes) > 0):
                    currentfigure = currentfigure + 1;
                    self.histogram_entire_range(f, dirname, currentfigure);
                else:
                    output_str = "No write range histogram because there are no write functions. \n";
                    output_str = output_str + "<BR>";
                    f.write(output_str);
                # end if
                
                # Plot histogram over byte range
                bincount = 100;
                junk1 = [];         # Storing syscall size in the byte range
                for junk2 in self.bytes:
                    if (junk2 <= 1000):
                        junk1.append((junk2));
                    # end if
                # end for
                if (len(junk1) > 0):
                    currentfigure = currentfigure + 1;
                    self.histogram_byte_range(f, dirname, bincount, junk1, currentfigure);
                else:
                    output_str = "No Byte range histogram because there are no write functions payloads in the Byte range. \n";
                    output_str = output_str + "<BR>";
                    f.write(output_str);
                # end if
                
                # Plot histogram over KB range
                junk1 = [];         # Storing syscall size in the KB range
                for junk2 in self.bytes:
                    if ( (junk2 >= 1000) and (junk2 <= 1000000) ):
                        junk1.append((junk2/1000.0));
                    # end if
                # end for
                if (len(junk1) > 0):
                    currentfigure = currentfigure + 1;
                    self.histogram_KB_range(f, dirname, bincount, junk1, currentfigure);
                else:
                    output_str = "No KB range histogram because there are no write functions payloads in the KB range. \n";
                    output_str = output_str + "<BR>";
                    f.write(output_str);
                # end if
                
                # Plot histogram over MB range
                junk1 = [];         # Storing syscall size in the MB range
                for junk2 in self.bytes:
                    if ( (junk2 >= 1000000) and (junk2 <= 1000000000) ):
                        junk1.append((junk2/1000000.0));
                    # end if
                # end for
                if (len(junk1) > 0):
                    currentfigure = currentfigure + 1;
                    self.histogram_MB_range(f, dirname, bincount, junk1, currentfigure);
                # endif
                
                # Plot histogram over GB range
                junk1 = [];         # Storing syscall size in the GB range
                for junk2 in self.bytes:
                    if ( (junk2 >= 1000000000) and (junk2 <= 1000000000000) ):
                        junk1.append((junk2/1000000000.0));
                    # end if
                # end for
                if (len(junk1) > 0):
                    currentfigure = currentfigure + 1;
                    self.histogram_GB_range(f, dirname, bincount, junk1, currentfigure);
                # end if
                
                # Plot histogram over TB+ range
                junk1 = [];         # Storing syscall size in the TB+ range
                for junk2 in self.bytes:
                    if (junk2 > 1000000000000):
                        junk1.append((junk2/1000000000000.0));
                    # end if
                # end for
                if (len(junk1) > 0):
                    currentfigure = currentfigure + 1;
                    self.histogram_TB_range(f, dirname, bincount, junk1, currentfigure);
                # end if
            # end if
        # end if
        
        #
        # Compute and Write Statistical Computations and summary to stdout and HTML output file
        # 
        
        # Start HTML for statistical summary section
        output_str = " \n";
        output_str = output_str + "<P> \n";
        f.write(output_str);
        
        # Start stdout output
        print "-- WRITE() Statistical Summary -- \n";
        
        # HTML output:
        output_str = "Overall statistical summary of write() functions focusing on the payload size \n";
        output_str = output_str + "per write() function call. <BR><BR> \n";
        f.write(output_str);
        
        # Write out Total Bytes written (stdout and HTML)
        junk1 = self.total_write_bytes;
        junk1a = "%d" % junk1;
        junk1b = commify3(junk1a);
        junk2 = int(self.total_write_bytes) / 1000000.0;
        junk2a = "%.2f" % junk2;
        junk2b = commify3( junk2a );
        print "Total number of Bytes written = " + junk1b + "   (" + junk2b + "  MB)"
        # HTML:
        output_str = "<UL>  \n";
        output_str = output_str + "   <LI>Total number of Bytes written= " + junk1b + "   (" + junk2b + "  MB) \n";
        output_str = output_str + "</UL> \n";
        f.write(output_str);
        
        # Write out Total number of write() function calls (stdout and HTML)
        junk1 = CmdCounter[WRITE];
        junk1a = commify3(junk1);
        print "Number of Write function calls = ", junk1a;
        # HTML
        output_str = "<UL> \n";
        output_str = output_str + "   <LI>Number of Write function calls = " + junk1a + " \n";
        output_str = output_str + "</UL> \n";
        f.write(output_str);
        
        # Write out Range (stdout and HTML)
        junk1a = commify3(self.write_range);
        print "Range of write function payloads: ",junk1a," Bytes";
        print " ";
        # HTML
        output_str = "<UL> \n";
        output_str = output_str + "   <LI>Range of write function payloads = " + junk1a + " Bytes \n";
        output_str = output_str + "</UL> \n";
        f.write(output_str);
        
        # Average (mean or arthimetic mean): Write to stdout and HTML
        #   Location, spread, and skewness measures
        self.mean_output(f);
        
        # Median: Write to stdout and HTML
        #   Location, spread, and skewness measures
        self.median_output(f);
        
        # Mode: Write to stdout and HTML
        #   Location, spread, and skewness measures
        self.mode_output(f);
        
        # Skewness: Write to stdout and HTML
        self.skewness_output(f);
        
        # Other Stats: Write to stdout and HTML
        self.other_stats(f);
        
        #
        # Write() Throughput performance section
        # 
        print " "
        
        # HTML:
        if (VFLAGS > 1):
            output_str = "<P> \n";
            output_str = output_str + "This next subsection presents some brief data on the write throughput \n";
            output_str = output_str + "performance of the application. The min and max write throughput \n";
            output_str = output_str + "performance are listed below. \n";
            output_str = output_str + "(Figure " + str(currentfigure+1) + "). \n";
            output_str = output_str + "</P> \n \n";
            f.write(output_str);
        else:
            output_str = "<P> \n";
            output_str = output_str + "This next subsection presents some brief data on the write throughput \n";
            output_str = output_str + "performance of the application. First, the min and max write throughput \n";
            output_str = output_str + "performance will be listed followed by a plot of the write throughput \n";
            output_str = output_str + "(Figure " + str(currentfigure+1) + "). \n";
            output_str = output_str + "</P> \n \n";
            f.write(output_str);
        # end if
        
        #
        # Create throughput plots and output (HTML only - no stdout)
        #
        currentfigure2 = self.throughput_output(f, BeginTime, EndTime, VFLAGS, currentfigure);
        currentfigure = currentfigure2;
        
        return currentfigure;
    # end def
    
    
    
    
    #
    # Creates ordered list of hyperlinks to histogram plots in the HTML output (no stdout)
    #
    def orderlist_output(self, f, currentfigure):
        
        output_str = "<OL> \n";
        str1 = "Write function payload size histogram for the entire range";
        currentfigure = currentfigure + 1;
        str2 = str(currentfigure);
        output_str = output_str + "   <LI><a href=\"#" + str1 + "\">" + "Figure "+str2+": " + str1 + "</a> \n";
        f.write(output_str);
        
        # Byte range
        junk1 = [];
        for junk2 in self.bytes:
            if (junk2 <= 1000):
                junk1.append((junk2));
            # end if
        # end for
        if (len(junk1) > 0):
            str1 = "Write function payload size histogram for the Byte range"
            currentfigure = currentfigure + 1;
            str2 = str(currentfigure);
            output_str = "   <LI><a href=\"#" + str1 + "\">" + "Figure "+str2+": " + str1 + "</a> \n";
            f.write(output_str);
        # end if
        
        # KB range
        junk1 = [];
        for junk2 in self.bytes:
            if ( (junk2 >= 1000) and (junk2 <= 1000000) ):
                junk1.append((junk2/1000.0));
            # end if
        # end for
        if (len(junk1) > 0):
            str1 = "Write function payload size histogram for the KB range";
            currentfigure = currentfigure + 1;
            str2 = str(currentfigure);
            output_str = "   <LI><a href=\"#" + str1 + "\">" + "Figure "+str2+": " + str1 + "</a> \n";
            f.write(output_str);
        # end if
        
        # MB range
        junk1 = [];
        for junk2 in self.bytes:
            if ( (junk2 >= 1000000) and (junk2 <= 1000000000) ):
                junk1.append((junk2/1000000.0));
            # end if
        # end for
        if (len(junk1) > 0):
            str1 = "Write function payload size histogram for the MB range"
            currentfigure = currentfigure + 1;
            str2 = str(currentfigure);
            output_str = "   <LI><a href=\"#" + str1 + "\">" + "Figure "+str2+": " + str1 + "</a> \n";
            f.write(output_str);
        # end if
        
        # GB range
        junk1 = [];
        for junk2 in self.bytes:
            if ( (junk2 >= 1000000000) and (junk2 <= 1000000000000) ):
                junk1.append((junk2/1000000000.0));
            # end if
        # end for
        if (len(junk1) > 0):
            str1 = "Write function payload size histogram for the GB range";
            currentfigure = currentfigure + 1;
            str2 = str(currentfigure);
            output_str = "   <LI><a href=\"#" + str1 + "\">" + "Figure "+str2+": " + str1 + "</a> \n";
            f.write(output_str);
        # end if
        
        # TB+ range
        junk1 = [];
        for junk2 in self.bytes:
            if (junk2 > 1000000000000):
                junk1.append((junk2/1000000000000.0));
            # end if
        # end for
        if (len(junk1) > 0):
            str1 = "Write function payload size histogram for the TB-TB+ range";
            currentfigure = currentfigure + 1;
            str2 = str(currentfigure);
            output_str = "   <LI><a href=\"#" + str1 + "\">" + "Figure "+str2+": " + str1 + "</a> \n";
            f.write(output_str);
        # end if
        
        # Close out Ordered List
        output_str = "</OL> \n";
        output_str = output_str + "</P> \n";
        f.write(output_str);
    # end def
    
    
    # 
    # Matplotlib histogram of entire range of write payloads
    #
    def histogram_entire_range(self, f, dirname, currentfigure):
        
        # Histogram of entire range
        bincount = 100;
        fig = plt.hist(self.bytes, bins=bincount);
        junk2 = "Write() payload size Histogram (entire range) - " + commify3(bincount) + " intervals";
        plt.title(junk2, fontsize='x-small');
        plt.xlabel("Write() Function Payload Size (Bytes)", fontsize='x-small');
        plt.ylabel("Count", fontsize='x-small');
        plt.xticks(rotation=35, fontsize='x-small');
        plt.yticks(fontsize='x-small');
        plot_name = dirname + "/write_entire_histogram";
        plt.savefig(plot_name);
        plt.close();
        
        # HTML Output:
        str2 = str(currentfigure);
        output_str = "<a id=\"Write function payload size histogram for the entire range\"> </a> \n";
        f.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"write_entire_histogram.png\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure "+str2+" - <a id=\"Write function payload size histogram for the entire range\">Write function payload size histogram for the entire range</a></strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        f.write(output_str);
    # end def
    
    
    
    # 
    # Matplotlib histogram of byte range of write payloads
    #
    def histogram_byte_range(self, f, dirname, bincount, junk1, currentfigure):
        
        str2 = str(currentfigure);
        string1 = "Write data size Histogram (0-1KB range) - ";
        xlabel = "Write Size in Bytes";
        plot_name = dirname + "/write_byte_histogram";
        html_link_string = "\"Write function payload size histogram for the Byte range\"";
        html_file = "\"write_byte_histogram.png\"";
        img_name = "Figure "+str2+" - Write function payload size histogram for the Byte range";
        
        # Create bins
        delta = 1000.0/float(bincount);
        bins2 = [];
        for i in range(0,(bincount+1)):
           junk2 = int(i*delta);
           bins2.append(junk2);
        # end for
        
        # Actually create the plot
        self.histogram_plot(f, bincount, junk1, bins2, string1, xlabel, plot_name, 
                             html_link_string, html_file, img_name);
    # end def
    
    
    
    # 
    # Matplotlib histogram of KB range of write payloads
    #
    def histogram_KB_range(self, f, dirname, bincount, junk1, currentfigure):
        
        str2 = str(currentfigure);
        string1 = "Write data size Histogram (KB range) - ";
        xlabel = "Write Size in KB";
        plot_name = dirname + "/write_kb_histogram";
        html_link_string = "\"Write function payload size histogram for the KB range\"";
        html_file = "\"write_kb_histogram.png\"";
        img_name = "Figure "+str2+" - Write function payload size histogram for the KB range";
        
        # Create bins
        delta = (1000)/float(bincount);   # Delta in KB
        bins2 = [];
        for i in range(0,(bincount+1)):
            junk2 = int(i*delta);
            bins2.append(junk2);
        # end for
        
        # Actually create the plot
        self.histogram_plot(f, bincount, junk1, bins2, string1, xlabel, plot_name, 
                            html_link_string, html_file, img_name);
    # end def


    # 
    # Matplotlib histogram of MB range of write payloads
    #
    def histogram_MB_range(self, f, dirname, bincount, junk1, currentfigure):
        
        str2 = str(currentfigure);
        string1 = "Write data size Histogram (MB range) - ";
        xlabel = "Write Size in MB";
        plot_name = dirname + "/write_mb_histogram";
        html_link_string = "\"Write function payload size histogram for the MB range\"";
        html_file = "\"write_mb_histogram.png\"";
        img_name = "Figure "+str2+" - Write function payload size histogram for the MB range";
        
        # Create bins
        delta = (1000.0)/float(bincount);   # MB
        bins2 = [];
        for i in range(0,(bincount+1)):
            junk2 = int(i*delta);
            bins2.append(junk2);
        # end for
        
        # Actually create the plot
        self.histogram_plot(f, bincount, junk1, bins2, string1, xlabel, plot_name, 
                            html_link_string, html_file, img_name);
    # end def
    
    
    # 
    # Matplotlib histogram of GB range of write payloads
    #
    def histogram_GB_range(self, f, dirname, bincount, junk1, currentfigure):
        
        str2 = str(currentfigure);
        string1 = "Write data size Histogram (GB range) - ";
        xlabel = "Write Size in GB";
        plot_name = dirname + "/write_gb_histogram";
        html_link_string = "\"Write function payload size histogram for the GB range\"";
        html_file = "\"write_gb_histogram.png\"";
        img_name = "Figure "+str2+" - Write function payload size histogram for the GB range";
        
        # Create bins?
        delta = (1000)/float(bincount);   # Delta in GB
        bins2 = [];
        for i in range(0,(bincount+1)):
            junk2 = int(i*delta);
            bins2.append(junk2);
        # end for
        
        # Actually create the plot
        self.histogram_plot(f, bincount, junk1, bins2, string1, xlabel, plot_name, 
                            html_link_string, html_file, img_name);
    # end def
    
    
    # 
    # Matplotlib histogram of TB range of write payloads
    #
    def histogram_TB_range(self, f, dirname, bincount, junk1, currentfigure):
        
        str2 = str(currentfigure);
        string1 = "Write data size Histogram (TB+ range) - ";
        xlabel = "Write Size in TB";
        plot_name = dirname + "/write_tb_histogram";
        html_link_string = "\"Write function payload size histogram for the TB-TB+ range\"";
        html_file = "\"write_tb_histogram.png\"";
        img_name = "Figure "+str2+" - Write function payload size histogram for the TB-TB+ range";
        
        # Create bins?
        delta = (1000)/float(bincount);   # Delta in TB
        bins2 = [];
        for i in range(0,(bincount+1)):
            junk2 = int(i*delta);
            bins2.append(junk2);
        # end for
        
        # Actually create the plot
        self.histogram_plot(f, bincount, junk1, bins2, string1, xlabel, plot_name, 
                            html_link_string, html_file, img_name);
    # end def
    
    
    # 
    # Histogram plots - used for all histogram plot (write() ranges)
    #
    def histogram_plot(self, f, bincount, junk1, bins2, string1, xlabel, plot_name, 
                       html_link_string, html_file, img_name):
        
        plt.hist(junk1, bins=bins2);
            
        junk2 = string1 + commify3(bincount) + " intervals";
        plt.title(junk2, fontsize='x-small');
        plt.xlabel(xlabel, fontsize='x-small');
        plt.ylabel("Count", fontsize='x-small');
        plt.xticks(rotation=35, fontsize='x-small');
        plt.yticks(fontsize='x-small');
        plt.savefig(plot_name);
        plt.close();
         
        # HTML Output:
        output_str = "<a id="+ html_link_string + "> </a> \n";
        f.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=" + html_file + "> \n";
        output_str = output_str + "<BR><strong>" + img_name +"</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        f.write(output_str);
    # end def

    

    #
    # Mean output (stdout and HTML)
    #    Mean (average)
    #    Standard deviation
    #    Variance
    #    Mean absolute deviation  (mad)
    #    Mean Squared Error (MSE)
    #
    def mean_output(self, f):
        # Average (mean or arthimetic mean):
        #   Location, spread, and skewness measures
        junk2 = num_output(self.arthimetic_mean,5);
        junk3 = commify3( junk2 );
        print "Average (arthimetic mean or AM) = ",junk3," (Bytes per write() function)";   # stdout
        output_str = "<UL> \n";
        output_str = output_str + "   <LI>Average (arthimetic mean or AM)  = ";
        output_str = output_str + str(junk3) + " (Bytes per write() function) \n";
        f.write(output_str);
        if (self.arthimetic_mean > 0.0):
            junk4 = (self.sigma_am/self.arthimetic_mean)*100.0;
            junk1 = num_output(self.sigma_am,5);
            junk1b = commify3( junk1 );
            junk2 = "%.2f" % junk4;
            junk2b = commify3( junk2 );
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "   AM Standard Deviation = ",junk1b," (Bytes per write() function)  (",junk3," of AM)";   # stdout
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>AM Standard Deviation = \n";
        output_str = output_str + str(junk1b) + " (Bytes per write() function)  (" + str(junk3) + " of AM) \n";
        f.write(output_str);
        
        # Variance
        junk1 = num_output(self.variance,5); 
        junk1b = commify3(junk1);
        print "   Variance = ",junk1b," (Bytes per write() function)";   # stdout
        output_str = "      <LI>Variance = " + str(junk1b) + " (Bytes per write() function) \n";
        f.write(output_str);
        
        # Mean absolute deviation
        junk2 = num_output(self.mad,5);
        junk2b = commify3(junk2);
        print "   Mean Absolute Deviation = ",junk2b," (Bytes per write() function)";   # stdout
        output_str = "      <LI>Mean Absolute Deviation = ";
        output_str = output_str + str(junk2b) + " (Bytes per write() function) \n";
        f.write(output_str);
        
        # Mean Squared Error (MSE)
        junk2 = num_output(self.mse,5);
        junk2b = commify3(junk2);
        print "   Mean Squared Error (MSE) = ",junk2b," (Bytes per write() function)";   # stdout
        output_str = "      <LI>Mean Squared Error (MSE) = ";
        output_str = output_str + str(junk2b) + " (Bytes per write() function) \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
    # end def
    
    
    
    #
    # Median output
    #    Mean
    #    Standard Deviation around Median
    #    Median Variance
    #    Medain Absolute Deviation
    #    Mean Squared Error (MSE)
    #
    def median_output(self, f):
        # Median
        #   Location, spread, and skewness measures
        junk2 = num_output(self.median,5);
        junk3 = commify3( junk2 );
        print "Median = ",junk3," (Bytes per write() function)";
        output_str = "   <LI>Median = " + junk3 + " (Bytes per write() function) \n";
        f.write(output_str);
        
        if (self.median != 0.0):
            junk4 = (self.sigma_median/self.median)*100.0;
            junk1 = num_output(self.sigma_median,5);
            junk1b = commify3(junk1);
            junk2 = "%.2f" % junk4;
            junk2b = commify3(junk2);
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "   Median Standard Deviation = ",junk1b," (Bytes per write() function)  (",junk3," of Median)";
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>Median Standard Deviation = ";
        output_str = output_str + str(junk1b) + " (Bytes per write() function) (" + str(junk3) + " of Median) \n";
        f.write(output_str);
   
        # Median Variance
        junk1 = num_output(self.median_variance,5);
        junk1b = commify3(junk1);
        print "   Variance using Median = ",junk1b," (Bytes per write() function)";
        output_str = "      <LI>Variance using Median = ";
        output_str = output_str + str(junk1b) + " (Bytes per write() function) \n";
        f.write(output_str);
        
        # Median Absolute Deviation
        junk2 = num_output(self.medianad,5);
        junk2b = commify3(junk2);
        print "   Median Absolute Deviation = ",junk2b," (Bytes per write() function)";
        output_str = "      <LI>Median Absolute Deviation = ";
        output_str = output_str + str(junk2b) + " (Bytes per write() function) \n";
        f.write(output_str);
        
        # Median Squared Error (MSE)
        junk2 = num_output(self.mse_median,5);
        junk2b = commify3(junk2);
        print "   Median Squared Error (MSE) = ",junk2b," (Bytes per write() function)";
        output_str = "      <LI>Median Squared Error (MSE) = ";
        output_str = output_str + str(junk2b) + " (Bytes per write() function) \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
    # end def
    
    
    #
    # Mode output:
    #    Mode output (mode and frequency)
    #    Standard deviation around mode
    #    Mode variance
    #    Mode absolute deviation
    #    Mode squared error (MSE)
    #
    def mode_output(self, f):
        
        # Mode:
        #   Location, spread, and skewness measures
        junk1 = len(self.bytes);
        junk1b = commify3(junk1);
        print "Mode:   Total number of values = ",junk1b;
        output_str = "   <LI>Mode:   Total number of values = " + str(junk1b) + " \n";
        output_str = output_str + "   <UL> \n";
        f.write(output_str);
        for item in self.mode:
            junk2 = item[0];
            junk3 = item[1];
            junk3b = commify3(junk3)
            junk4 = float(junk3)/float(junk1)*100.0;
            junk5 = "%.4f" % junk4;
            junk5b = commify3(junk5);
            junk6 = junk5b + "%";
            print "   Value for number of bytes per write function = ",junk2," Repeated ",junk3b," times  (",junk6," of total values)";
            output_str = "      <LI>Value for number of bytes per write() function</strong> = ";
            output_str = output_str + str(junk2) + " Repeated " + str(junk3b) + " times  (";
            output_str = output_str + str(junk6) + " of total values) \n";
            f.write(output_str);
            
            v5 = junk2;
            v5_sigma = std_dev(self.bytes, junk2);              # Standard Deviation around Mode
            if (v5 != 0.0):
                junk4 = v5_sigma/v5;
                junk1 = num_output(v5_sigma,5);
                junk1b = commify3(junk1);
                junk2 = "%.2f" % junk4;
                junk2b = commify3(junk2);
                junk3 = junk2b + "%";
            else:
                junk4 = 0.0;
                junk3 = 0.0;
            #endif
            print "      Mode Standard Deviation = ",junk1b," (Bytes per write() function) (",junk3," of Median)";
            output_str = "      <UL> \n";
            output_str = output_str + "         <LI>Mode Standard Deviation = ";
            output_str = output_str + str(junk1b) + " (Bytes per write() function) (" + str(junk3) + " of Median) \n";
            f.write(output_str);
            
            Mode_v1 = v5_sigma*v5_sigma;                             # Mode Variance
            junk1 = num_output(Mode_v1,5);
            junk1b = commify3(junk1);
            print "      Variance using Mode = ",junk1b," (Bytes per write() function)";
            output_str = "         <LI>Variance using Mode = "
            output_str =output_str + str(junk1b) + " (Bytes per write() function) \n";
            f.write(output_str);
            
            Mode_v2 = my_abs_deviation(self.bytes,v5);               # Mode Absolute Deviation
            junk2 = num_output(Mode_v2,5);
            junk2b = commify3(junk2);
            print "      Mode Absolute Deviation = ",junk2b," (Bytes per write() function)";
            output_str = "         <LI>Mode Absolute Deviation = ";
            output_str = output_str + str(junk2b) + " (Bytes per write() function) \n";
            
            Mode_v3 = (Mode_v1*Mode_v1)/float(len(self.bytes));      # Mode Squared Error (MSE)
            junk2 = num_output(Mode_v2,5);
            junk2b = commify3(junk2);
            print "      Mode Squared Error (MSE) = ",junk2b," (Bytes per write() function)";
            output_str = "         <LI>Mode Squared Error (MSE) = ";
            output_str = output_str + str(junk2b) + " (Bytes per write() function) \n";
            f.write(output_str);
            
            output_str = "      </UL> \n";
            f.write(output_str);
        # end for
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        output_str = "</P> \n \n";
        f.write(output_str);
    # end def


    #
    # Skewness and commentary computation and output
    #    Computes order of mean, median, and mode
    #    Computes Fisher-Pearson skewness measures (separate function)
    #    Computes Kurtosis
    #
    #    Writes output skewness summary
    #
    def skewness_output(self,f):
        
        # Shape of Curve (skewness)
        print " ";
        print " ";
        print "The following statistics are for the 'shape' of the distribution of the write() ";
        print "function payload for all write() calls.";
        # HTML
        output_str = "<P> \n";
        f.write(output_str);
        output_str = "The following statistics are for the 'shape' of the distribution of ";
        output_str = output_str + "the write() function payload. \n <BR><BR> \n";
        f.write(output_str);
        
        # Sorted order of mean, median, and mode
        D_local = {};
        D_local['mean'] = self.arthimetic_mean;
        D_local['median'] = self.median;
        D_local['mode'] = self.mode[0][0];
        DD_local = sort_by_value(D_local);
        print " ";
        print "   The following is the ascending order and value of the mean, median, and ";
        print "   mode statistics. The order of these statistics can be important for the";
        print "   skewness or shape of the curve of the distribution of the write payload";
        print "   sizes.";
        iloop = 0;
        output_str2 = "   ";
        for item in DD_local:
            iloop = iloop + 1;
            if (iloop == 1):
                output_str2 = output_str2 + item + " (" + str(D_local[item]) + " Bytes) ";
            else:
                output_str2 = output_str2 + " <  " + item + " (" + str(D_local[item]) + " Bytes) ";
            # end if
        # end for
        if (iloop == 3):
            final_loop = item;
        # end if
        output_str2 = output_str2 + " \n";
        print " ";
        print output_str2;
        # HTML:
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>The following is the ascending order and value of the mean, median, and \n";
        output_str = output_str + "mode statistics. The order of these statistics can be important for the \n";
        output_str = output_str + "skewness or shape of the curve of the distribution of the write payload \n";
        output_str = output_str + "sizes. \n";
        f.write(output_str);
        output_str = "<BR><BR> \n";
        f.write(output_str);
        f.write(output_str2);
        output_str = "<BR><BR> \n";
        f.write(output_str);
        
        #
        # Fisher-Pearson skewness measures
        #
        self.fisher_pearson(f);
        
        #
        # Kurtosis
        #
        junk1 = commify3(self.kurtosis_v1);
        print "   Kurtosis relative to mean = ",junk1;
        output_str = "   <LI>Kurtosis relative to mean = " + str(junk1) + " \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        # skewness summary:
        self.skewness_summary(f, final_loop);
        
    # end def
    
    
    #
    # Other stats
    #    Slowest write (and line in file where it occurs)
    #    Fastest write (and line in file where is occurs)
    #    Smallet and largest payload
    #
    def other_stats(self, f):
         
         # Other Stats:
         print "Other statistics:"
         # HTML:
         output_str = "<BR> \n";
         f.write(output_str);
         output_str = "<P> \n";
         f.write(output_str);
         output_str = "Other statistics: \n";
         f.write(output_str);
         
         # Slowest write function
         print " ";
         junk1 = self.WriteMax["MaxTime"];
         print "Time for slowest write function (secs) = " + str(junk1);
         # HTML
         output_str = "<UL> \n";
         f.write(output_str);
         output_str = "   <LI>Time for slowest write function (secs) = " + commify3(junk1) + " \n";
         f.write(output_str);
         junk1 = self.WriteMax["line"];
         print "   Line location in file: ",commify3(junk1);
         # HTML
         output_str = "   <UL> \n";
         output_str = output_str + "      <LI>Line location in file</strong> = " + commify3(junk1) + " \n";
         output_str = output_str + "   </UL> \n";
         f.write(output_str);
         
         # Smallest and largest write function payload
         print " ";
         print "Smallest write syscall size: ",self.WriteSmall," (Bytes)";
         junk1 = commify3(self.WriteLarge);
         print "Largest write syscall size: ",junk1," (Bytes)";
         # HTML
         output_str = "   <LI>Smallest write syscall payload size</strong> = " + commify3(self.WriteSmall) + " (Bytes) \n";
         f.write(output_str);
         output_str = "   <LI>Largest write syscall payload size</strong> = " + commify3(junk1) + " (Bytes)  \n";
         f.write(output_str);
         output_str = "</UL> \n";
         f.write(output_str);
         output_str = "</P> \n \n";
         f.write(output_str);
    # end def

    #
    # File interval output
    #
    def file_interval_output(self, f, FileSizes, FileSizeCounter):

        #
        # File Size Interval Summary - Compute intervals first
        #
        junk1 = len(FileSizes);       # number of syscall sizes (junk3)
        for junk2 in self.bytes:
            if (junk2 <= FileSizes[0]):
                junk3 = FileSizes[0];
                FileSizeCounter[junk3] = FileSizeCounter[junk3] + 1;
            elif (junk2 >= FileSizes[junk1-1]):
                junk3 = FileSizes[junk1-1];
                FileSizeCounter[junk3] = FileSizeCounter[junk3] + 1;
            else:
                iloop = 0;
                for icount in range(1,(junk1+1)):
                    if (junk2 <= FileSizes[icount] and junk2 >= FileSizes[icount-1]):
                        iloop = icount;
                        break;
                     # end if
                # end for statement
                junk3 = FileSizes[iloop];
                FileSizeCounter[junk3] = FileSizeCounter[junk3] + 1;
            # end if
        # End for item in Write:
        
        #
        # Print out intervals and count
        #

        # stdout first
        print " ";
        print "-- Payload sizes for write() function --";
        print " ";
        print " ";
        print "IO Size Range                        Number of Syscalls";
        print "=======================================================";
        
        #
        # First File Size interval 
        #
        
        # stdout: Build string for interval
        iloop = 1;
        output_str = "(";
        junk1 = "%3d" % iloop;
        junk2 = "0KB";                                      # Lower bound
        junk3 = junk2.rjust(7," ");
        junk5 = FileSizeStr( FileSizes[iloop-1] );         # Call function "FileSizeStr" to return string
        junk6 = junk5.rjust(7," ");
        junk7 = commify3(FileSizeCounter[ FileSizes[iloop-1] ]);
        junk7a = commify3(junk7);
        junk8 = junk7a.rjust(30," ");
        output_str = output_str + junk1 + ")" + junk3 + " <   <" + junk6 + junk8
        print output_str;
        
        # First File Size Interval - HTML
        junk7a = commify3(FileSizeCounter[ FileSizes[iloop-1] ]);
        output_str = "   <tr> \n";
        output_str = output_str + "      <td align=center><font size=\"-2\"><strong><tt>" + junk3 + " <   <" + junk6 + "</tt></strong></font></td> \n";
        junk0 = "      <td align=center><font size=\"-2\">" + junk7a + "</font></td> \n";
        # end if
        output_str = output_str + junk0;
        f.write(output_str);
        
        #
        # Remaining File Size interval 
        #
        for icount in range(1,len(FileSizes)):
            iloop = iloop + 1;
            output_str = "(";
            junk1 = "%3d" % iloop;
            junk2 = FileSizeStr( FileSizes[icount-1] );                                      # Lower bound
            junk3 = junk2.rjust(7," ");
            junk5 = FileSizeStr( FileSizes[icount] );         # Call function "FileSizeStr" to return string
            junk6 = junk5.rjust(7," ");
            junk7 = commify3(FileSizeCounter[ FileSizes[iloop-1] ]);
            junk7a = commify3(junk7);
            junk8 = junk7a.rjust(30," ");
            output_str = output_str + junk1 + ")" + junk3 + " <   <" + junk6 + junk8
            print output_str
            
            # HTML
            junk7a = commify3(FileSizeCounter[ FileSizes[iloop-1] ]);
            output_str = "   <tr> \n";
            output_str = output_str + "      <td align=center><font size=\"-2\"><strong><tt>" + junk3 + " <   <" + junk6 + "</tt></strong></font></td> \n";
            junk0 = "      <td align=center><font size=\"-2\">" + junk7a + "</font></td> \n";
            output_str = output_str + junk0;
            f.write(output_str);
        # end for
        print " ";
        print " ";
        
        # HTML - close table
        output_str = "</table></center><BR><BR> \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + " \n";
        f.write(output_str);
    # end def


    #
    # Write out HTML write statistics header
    #
    def stats_header(self, f):
        
        print "---------------------- ";
        print "-- Write Statistics -- ";
        print "---------------------- ";
        
        # HTML report output (opt of section)
        output_str = " \n";
        output_str = output_str + "<hr /> \n";
        output_str = output_str + "<H3> \n"
        output_str = output_str + "3. <a id=\"write_stat\">Write Statistics</a> \n";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P> \n";
        output_str = output_str + "This section presents statistical information about the write functions in the \n";
        output_str = output_str + "application. It focuses on use of the write(2) function in glibc. The pertinent \n";
        output_str = output_str + "details of the man pages are: <BR><BR> \n"
        output_str = output_str + "<blockquote><em> \n";
        output_str = output_str + "<strong>NAME</strong><BR> \n";
        output_str = output_str + "       write - write to a file descriptor <BR><BR> \n";
        output_str = output_str + "<strong>SYNOPSIS</strong><BR> \n";
        output_str = output_str + "       #include <unistd.h> <BR><BR> \n";
        output_str = output_str + "       ssize_t write(int fd, const void *buf, size_t count); <BR><BR> \n";
        output_str = output_str + "<strong>DESCRIPTION</strong><BR> \n";
        output_str = output_str + "       write() writes up to <u>count</u> bytes from the buffer pointed <u>buf</u> \n";
        output_str = output_str + "to the file referred to by the file descriptor <u>fd</u>. <BR><BR> \n";
        output_str = output_str + "       The  number  of bytes written may be less than <u>count</u> if, for example, there \n";
        output_str = output_str + "is insufficient space on the underlying physical medium, or the RLIMIT_FSIZE \n";
        output_str = output_str + "resource limit is encountered (see setrlimit(2)), or the call was interrupted  \n";
        output_str = output_str + "by a signal handler after having written less than <u>count</u> bytes. \n";
        output_str = output_str + "(See also pipe(7).) <BR><BR>n";
        output_str = output_str + "       For a seekable file (i.e., one to which lseek(2) may be applied, for \n";
        output_str = output_str + "example, a regular file) writing takes place at the current file offset, and the \n";
        output_str = output_str + "file offset is incremented by the number of bytes  actually written.  If  \n";
        output_str = output_str + "the file was open(2)ed with O_APPEND, the file offset is first set to the end \n";
        output_str = output_str + "of the file before writing.  The adjustment of the file offset and the write \n";
        output_str = output_str + "operation are performed as an atomic step.<BR><BR> \n";
        output_str = output_str + "       POSIX requires that a read(2) which can be proved to occur after a \n";
        output_str = output_str + "write() has returned returns the new data.  Note that not all file systems are \n";
        output_str = output_str + "POSIX conforming.<BR><BR> \n";
        output_str = output_str + "</em></blockquote><BR> \n";
        f.write(output_str);
        
        output_str = "The information and statistics in this section focus on the write() aspects of the \n";
        output_str = output_str + "application. Both tabular and graphical information is provided. \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + " \n";
        f.write(output_str);
        
        output_str = "<P> \n";
        output_str = output_str + "Table 2 below contains information on the total number of write function \n";
        output_str = output_str + "calls as a function of the data transfer size. \n"
        output_str = output_str + "<BR><BR><center><strong>Table 2 - Total Write Function calls vs. data size</strong><BR><BR> \n";
        output_str = output_str + "<table border =" + "\"1\" " + "> \n";
        output_str = output_str + "   <tr> \n";
        output_str = output_str + "      <th><font size=\"-2\">&nbsp IO Size Range &nbsp</font></th> \n";
        output_str = output_str + "      <th><font size=\"-2\">&nbsp Total Number of Syscalls &nbsp</font></th> \n";
        output_str = output_str + "   </tr> \n";
        f.write(output_str);
        output_str = " ";

    # end def
    
    
    #
    # Fischer-Pearson skewness factors
    #
    def fisher_pearson(self, f):
        
        # Fisher-Pearson Generalized moment (skewness measure) - g1
        #    http://en.wikipedia.org/wiki/Pearson%27s_skewness_coefficients#Pearson.27s_skewness_coefficients
        print " ";
        output_str = "<BR> \n";
        if (self.skewness_mean > 0.0):
            print "   Fisher-Pearson coefficient of skewness (g1) relative to mean = ",self.skewness_mean,"  (skewed right).";
            print "      This means the peak is shifted left and the tail extends to the right";
        else:
            print "   Fisher-Pearson coefficient of skewness (g1) relative to mean = ",self.skewness_mean,"  (skewed left).";
            print "      This means the peak skewed to the right and the tail extends to the left";
        # end if
        # HTML output:
        output_str = "   <LI>Fisher-Pearson coefficient of skewness (g1) relative to mean = " + str(self.skewness_mean);
        if (self.skewness_mean > 0.0):
            output_str = output_str + "   (skewed right). This means the peak is shifted left and the tail extends to the right. \n";
        else:
            output_str = output_str + "   (skewed left).  This means the peak skewed to the right and the tail extends to the left. \n"
        # end if
        f.write(output_str);
        
        # Adjusted Fisher-Pearson standardized moment coefficient - G1
        #   http://en.wikipedia.org/wiki/Pearson%27s_skewness_coefficients#Pearson.27s_skewness_coefficients
        print "   Fisher-Pearson Adjusted Standardized Moment Coefficient (G1) = ",self.FP_coeff;
        if (self.FP_coeff > 0.0):
            print "      Note: (skewed right). Magnitude of G1 also determines how far it is from the normal";
            print "            distribution. Values that are larger than zero indicate a skewed sample.";
        else:
            print "      Note: (skewed left). Magnitude of G1 also determines how far it is from the normal";
            print "            distribution. Values that are larger than zero indicate a skewed sample.";
        # end if
        # HTML:
        output_str = "   <LI>Fisher-Pearson Adjusted Standardized Moment Coefficient (G1) = ";
        output_str = output_str + str(self.FP_coeff) + " \n";
        if (self.FP_coeff > 0.0):
            output_str = output_str + "  (skewed right). The magnitude of G1 also determines how far \n";
            output_str = output_str + "it is from the normal distribution. Values that are larger than zero \n";
            output_str = output_str + "indicate a skewed sample \n";
        else:
            output_str = output_str + "  (skewed left). The magnitude of G1 also determines how far \n";
            output_str = output_str + "it is from the normal distribution. Values that are larger than zero \n";
            output_str = output_str + "indicate a skewed sample \n";
        # end if
        f.write(output_str);
        
        # SK2 (Pearson 2 skewness coefficient)
        #   http://en.wikipedia.org/wiki/Pearson%27s_skewness_coefficients#Pearson.27s_skewness_coefficients
        output_str = "<BR> \n";
        if (self.sk2 > 0.0):
            print "   Pearson 2 skewness coefficient = ",self.sk2,"  (skewed right)";
            print "      This means the peak is shifted left and the tail extends to the right";
        else:
            print "   Pearson 2 skewness coefficient = ",self.sk2,"  (skewed left)";
            print "      This means the peak skewed to the right and the tail extends to the left";
        # end if
        # HTML output:
        output_str = "   <LI>Pearson 2 skewness coefficient = " + str(self.sk2);
        if (self.sk2 > 0.0):
            output_str = output_str + "   (skewed right). This means the peak is shifted left and the tail extends to the right. \n";
        else:
            output_str = output_str + "   (skewed lerft). This means the peak skewed to the right and the tail extends to the left. \n";
        # end if
        f.write(output_str);
        
    # end def
    
    
    #
    # Skewness summary
    #
    def skewness_summary(self, f, final_loop):
        #
        # Skewness summary:
        #
        print " ";
        print "   Final Comments on shape of curve based on statistical results:";
        print " ";
        # HTML:
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>Final comments on shape \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        #
        # First Skewness measure - order of mean, median, mode. stdout and HTML output
        #    Use unstructured list for HTML
        #
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        
        # Order of mean, median, mode:
        if (final_loop == 'mode'):
            string1 = "left";
            string2 = "right";
            string3 = "mean < median < mode"
            string4 = "negative"
            string5 = "_larger_";
        elif (final_loop == "mean"):
            string1 = "right";
            string2 = "left";
            string3 = "mode < median < mean"
            string4 = "positive"
            string5 = "_smaller_";
        # end if
        print "      Based on the order of the main statistics, best guess is the shape is skewed ",string1,".";
        print "      In general this usually means:  ",string3,"but not necessarily ";
        print "      every time. Skewed ",string1," means that the peak is shifted to the ",string2," with";
        print "      a long tail to the ",string1,". It can also mean that the skewness value is ",string4,".";
        print "      In the case of the write() function payload size (how many bytes in the write";
        print "      function), this means there are more ",string5," writes relative to the average ";
        print "      and median.";
        # HTML
        output_str = "      <LI>Based on order of statistics, best guess is the shape is <strong>skewed "+string1+"</strong>. \n";
        output_str = output_str + "         In general this usually means:  "+string3+", but not necessarily \n";
        output_str = output_str + "         every time. Skewed "+string1+" means that the peak is shifted to the "+string2+" with \n";
        output_str = output_str + "         a long tail to the "+string1+". It can also mean that the skewness value is "+string4+". \n"
        output_str = output_str + "         In the case of the write() function payload size (how many bytes in the write \n";
        output_str = output_str + "         function), this means there are more "+string5+" writes relative to the average \n";
        output_str = output_str + "         and median. \n";
        f.write(output_str);
        
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str); 
        
        #
        # Fisher-Pearson Generalized moment (skewness measure) - g1
        #   stdout and HTML output
        #
        print " ";
        # HTML output:
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        
        if (self.skewness_mean > 0.0):
            string1 = "positive";
            string2 = "right";
            string3 = "left";
            string4 = "_small_";
        else:
            string1 = "negative";
            string2 = "left";
            string3 = "right";
            string4 = "_large_";
        # end if
        print "      The Fisher-Pearson coefficient of skewness (g1) is ",string1," the write() payload.";
        print "      distribution is skewed ",string2,". This means the peak skewed to the ",string3," and the tail ";
        print "      extends to the ",string2,". In the case of the write() function payload size (how many ";
        print "      bytes in the write() function), this means there are more ",string4," writes relative ";
        print "      to the average and median.";
        
        output_str = "   <LI>The Fisher-Pearson coefficient of skewness (g1) is "+string1+" so the write() \n";
        output_str = output_str + "distibution is <strong>skewed to the "+string2+"</strong>. This means the peak \n";
        output_str = output_str + "is shifted to the "+string3+" and the tail extending to the "+string2+". \n";
        output_str = output_str + "In the case of the write() function payload size (how many bytes in the\n";
        output_str = output_str + " write() function, this means there are more "+string4+" writes relative \n";
        output_str = output_str + "to the average and median. \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        #
        # Adjusted Fisher-Pearson standardized moment coefficient - G1
        #
        print " ";
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        if (self.FP_coeff > 0.0):
            string1 = "positive";
            string2 = "right";
            string3 = "left";
            string4 = "_smaller_";
        else:
            string1 = "negative";
            string2 = "left";
            string3 = "right";
            string4 = "_larger_";
        # end if
        print "      Since the adjusted Fisher-Pearon Standardized Moment Coefficient (G1) is ";
        print "      ",string1,", the distribution appears to be skewed ",string2,". That is, the peak is";
        print "      shifted to the ",string3," with a tail extending to the ",string2,". The magnitude of G1";
        print "      also determines how far it is from the normal distribution. G1 values that are";
        print "      larger than zero indicate a skewed sample relative to the normal distribution.";
        print "      One can think of a distribution with a large value of G1 being 'more skewed' than";
        print "      a distribution with a smaller value. For the case of the distribution of write()";
        print "      function payload size (the number of bytes per write() function), this ";
        print "      generally means that there are more ",string4," writes than larger writes.";
        
        output_str = "   <LI>Since the adjusted Fisher-Pearon Standardized Moment Coefficient (G1) \n";
        output_str = output_str + "is "+string1+" the distribution appears to be <strong>skewed "+string2+"</strong>. \n";
        output_str = output_str + "That is, the peak is shifted to the "+string3+" with a tail extending to the \n";
        output_str = output_str + string2+". The magnitude of G1 also determines how far it is from the normal \n";
        output_str = output_str + "distribution. G1 values that are larger than zero indicate a skewed \n";
        output_str = output_str + "sample relative to the normal distribution. One can think of a distribution \n";
        output_str = output_str + "with a large value of G1 being 'more skewed' than a distribution with \n";
        output_str = output_str + "a smaller value. For the case of the distribution of write() function \n";
        output_str = output_str + "payload size (the number of bytes per write() function), this generally \n";
        output_str = output_str + "means that there are more "+string4+" writes than larger writes. \n";
        f.write(output_str);
        
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        #
        # SK2 (Pearson 2 skewness coefficient)
        #
        print " ";
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        if (self.sk2 > 0.0):
            string1 = "positive";
            string2 = "right";
            string3 = "left";
            string4 = "_smaller_";
            string5 = "larger";
        else:
            string1 = "negative";
            string2 = "left";
            string3 = "right";
            string4 = "_larger_";
            string5 = "smaller";
        # end if
        print "      The Pearson 2 skewness coefficient (SK2) is ",string1," so that means the distribution is";
        print "      skewed to the ",string2,". This means that the peak is shifted to the ",string3," which means";
        print "      that there are more ",string4," write payload sizes (number of bytes per write() ";
        print "      function) than ",string5," payloads. It also means there is a tail that extends to";
        print "      to the ",string2,". Notice that the value of SK2 must be between -3 and 3 with these";
        print "      limits being extreme values."
        # HTML
        output_str = "   <LI>The Pearson 2 skewness coefficient (SK2) is "+string1+" so that means the distribution is \n";
        output_str = output_str + "<strong>skewed to the "+string2+"</strong>. This means that the peak is shifted to the "+string3+" which means \n";
        output_str = output_str + "that there are more "+string4+" write payload sizes (number of bytes per write() \n";
        output_str = output_str + "function) than smaller payloads. It also means there is a tail that extends to \n";
        output_str = output_str + "to the "+string2+". Notice that the value of SK2 must be between -3 and 3 with these \n";
        output_str = output_str + "limits being extreme values. \n"
        
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        #
        # Kurtosis
        #
        print " ";
        print "      The value of Kurtosis refers to the shape of the distribution relative to a";
        print "      normal distribution. Larger values of Kurtosis can mean that the distribution";
        print "      has a sharper peak or heavy tails which means that the tail of the distribution";
        print "      curve can extend a long way. Larger values can also indicate large 'shoulders'";
        print "      which are smaller peaks that are between the mean and the first standard";
        print "      deviation. In the case of write() payload distributions, a large value of ";
        print "      kurtosis means that the peak of payload sizes around the mean is very sharp";
        print "      and/or there are some smaller peaks between the mean the first standard deviation.";
        # HTML
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        output_str = "   <LI>The value of Kurtosis refers to the shape of the distribution relative to a \n";
        output_str = output_str + "normal distribution. Larger values of Kurtosis can mean that the distribution \n";
        output_str = output_str + "has a sharper peak or heavy tails which means that the tail of the distribution \n";
        output_str = output_str + "curve can extend a long way. Larger values can also indicate large 'shoulders' \n";
        output_str = output_str + "which are smaller peaks that are between the mean and the first standard \n";
        output_str = output_str + "deviation. In the case of write() payload distributions, a large value of \n";
        output_str = output_str + "kurtosis means that the peak of payload sizes around the mean is very sharp \n";
        output_str = output_str + "and/or there are some smaller peaks between the mean the first standard deviation. \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        #
        # Final comment
        #
        print " ";
        print "      If you get conflicting indicators on the skewness (right or left), then";
        print "      it is impossible to say what the shape of the curve looks like. This means";
        print "      that it is difficult to say if the curve of the write() function payload";
        print "      size distribution is non-symmetrical and/or bends to one direction. It may ";
        print "      also have several local minima and it may have long or short tails.";
        # HTML
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        output_str = "   <LI>If you get conflicting indicators on the skewness (right or left), then \n";
        output_str = output_str + "it is impossible to say what the shape of the curve looks like. This means \n";
        output_str = output_str + "that it is difficult to say if the curve of the write() function payload \n";
        output_str = output_str + "size distribution is non-symmetrical and/or bends to one direction. It may \n"
        output_str = output_str + "also have several local minima and it may have long or short tails. \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        # finish output
        print " ";
        # HTML:
        output_str = "</P> \n \n";
        f.write(output_str);
    # end def
    
    
    #
    # Write Throughput stats (stdout, HTMl, and plots)
    #
    def throughput_output(self, f, BeginTime, EndTime, VFLAGS, currentfigure):
        
        # Compute the throughput to MB/s (local variable)
        write_syscall_throughput_all_MB = [(x / 1000000.0) for x in self.write_syscall_throughput_all ];   # Convert throughput to MB/s
        
        # Print Min, Max throughput (stdout and HTML)
        junk1 = "%.4f" % self.throughput_max_MB;
        print "Maximum Write Throughput = ",commify3(junk1)," MB/s";
        junk2 = "%.4f" % self.throughput_max_time;
        print "   occurred at ",commify3(junk2)," seconds";
        junk3 = "%.4f" % self.throughput_min;
        print "Minimum non-zero Write Throughput = ",commify3(junk3)," MB/s";
        junk4 = "%.4f" % self.throughput_min_time;
        print "   occurred at ",commify3(junk4)," seconds";
        print " ";
        # HTML:
        output_str = "<P> \n";
        output_str = output_str + "The minimum and maximum write throughput (in MB/s) of the appliction \n";
        output_str = output_str + "are listed below: \n";
        output_str = output_str + "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>Maximum Write Throughput: " + junk1 + " MB/s \n";
        output_str = output_str + "   <UL> \n";
        output_str = output_str + "      <LI>Occured at " + junk2 + " seconds \n";
        output_str = output_str + "   </UL> \n";
        output_str = output_str + "   <LI>Minimum non-zero Write Throughput = " + junk3 + " MB/s \n";
        output_str = output_str + "   <UL> \n";
        output_str = output_str + "      <LI>occurred at " + junk4 + " seconds \n";
        output_str = output_str + "   </UL> \n";
        output_str = output_str + "</UL> \n";
        output_str = output_str + "</P> \n \n";
        f.write(output_str);
   
        # Plot time vs. write_syscall_throughput_all
        if (VFLAGS > 1):
            # Increment figure number
            currentfigure = currentfigure + 1;
            str2 = str(currentfigure);
            
            # HTML header stuff
            output_str = "<P> \n";
            output_str = output_str + "Figure "+str2+" below plots the write throughput history (MB/s) when the \n";
            output_str = output_str + "application is run. \n";
            f.write(output_str);
            output_str = "<BR><BR> \n";
            f.write(output_str);
            
            # Define plot attributes (titles, etc.)
            title = " ";    # name of input file
            xaxis_title_1 = "Time (secs)";
            yaxis_title_1 = "Write Throughout (MB/s)";
            output_file_name = "./HTML_REPORT/write_throughput_1.png";
            
            # Call function to make plot (1 plot)
            Plot_1_1(self.time, write_syscall_throughput_all_MB,
                     title, xaxis_title_1, yaxis_title_1, output_file_name);
            
            # HTML Output for plot
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"write_throughput_1.png\"> \n";
            output_str = output_str + "</center> \n";
            output_str = output_str + "<center><strong>Figure "+str2+" - Write Throughput time history (MB/s)</strong></center><BR><BR> \n";
            output_str = output_str + "<BR><BR> \n";
            output_str = output_str + "</P> \n";
            f.write(output_str);
            
            # Plot of throughput (x-axis) vs. syscall size (y-axis)
            
            # Define plot attributes (titles, etc.)
            title = " ";    # name of input file
            xaxis_title_1 = "Throughput (MB/s)";
            yaxis_title_1 = "Syscall Size (Bytes)";
            output_file_name = "./HTML_REPORT/write_throughput_vs_syscall_size_all_cumulative.png";
            
            # Call function make plot (1 plot)
            Plot_1_1(write_syscall_throughput_all_MB, self.bytes, title, xaxis_title_1, yaxis_title_1, output_file_name);
            
            # Increment figure number
            currentfigure = currentfigure + 1;
            
            # HTML Output for plot
            output_str = "<BR> <BR> \n";
            f.write(output_str);
            output_str = "<P> \n";
            output_str = output_str + "Figure " + str(currentfigure) + " below is a plot of write throughput (MB/s) \n";
            output_str = output_str + "(x-axis) versus write syscall size in bytes (y-axis). <BR>\n";
            f.write(output_str);
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"write_throughput_vs_syscall_size_all_cumulative.png\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(currentfigure) + " - Write Throughput in MB/s ";
            output_str = output_str + "versus Write syscall size in bytes</strong></center><BR><BR> \n";
            output_str = output_str + "</P> <BR> \n \n";
            f.write(output_str);
        else:
            output_str = "</P> \n \n";
            f.write(output_str);
        # end if
        
        return currentfigure;
    # end def
    
    
# end class write


