#
# Copyright 2008-2014 Jeffrey B. Layton
#



try:
     import matplotlib.pyplot as plt;
except:
     print "Cannot find matplotlib - needed for producing plots.";
     print "Stopping.";
     sys.exit();
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




#
#
# IOPS Class definition
#
#
class iopsclass:
#
# Instantiated Object stores data as self.iopsdata. This is a list of lists (2D list).
# Each row of the list consists of a record. Each record consists of:
#
#   LineNum        (line number of strace output file)
#   filename       (filename associated with IO operatio)
#   sec            (seconds since epoch when function was called)
#   sec_int        (seconds interval where IOP took place)
#   func           (IO function)
#

    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.iopsdata = [];
    # end def
    
    
    #
    # This function appenda data to self.iopsdata
    #
    def storeiops(self,data):
        self.iopsdata.append(data)
    # end def
    
    
    #
    # Return the list to caller
    #
    def getiops(self):
        return self.iopsdata;
    # end def
    
    
    #
    # Compute statistics on self.iopsdata
    #
    def getstats(self, CmdCounter, BeginTime, EndTime, WRITE, READ, VFLAGS):
        
        # Compute total run time (needed later)
        runtime = float(EndTime)-float(BeginTime);
        
        
        #
        # Get write IOPS Statistics
        # ----------------------------------
        
        #
        # Start with WRITE IOPS Statistics
        #
        if (CmdCounter[WRITE] > 0):
            
            #
            # Initialization
            #
            sum1_write = 0;
            itotal_write = 0;                  # Total number of WRITE function
            self.IOPS_Write_peak = 0;          # Peak Write IOPS
            self.IOPS_Write_peak_time = 0;     # Time interval where Peak Write IOPS occurs
            IOPS_Write_Plot = [];              # Used for plotting
            
            #
            # Extract all the WRITE IOPS information (how many in what time interval)
            #
            
            # Find Write time intervals
            #    extract time intervals into local array
            Local_Array = [];
            for item in self.iopsdata:
                if (item[4] == WRITE):
                    junk1 = int(item[3]);
                    Local_Array.append(junk1);
                # end if
            # end for loop
            
            # Count duplicates in time intervals
            Counts = count_dups(Local_Array);
            
            #
            # Create time interval list (all IO operations)
            #
            Time_Intervals_Write = [];
            for item in Counts:
                Time_Intervals_Write.append(item[0]);
            # end for
            Time_Intervals_Write.sort();                               # sort time interval array in ascending order
            self.Time_Intervals_Write = list(Time_Intervals_Write);    # Create time interval list stored in object
            Time_Intervals_Write = [];                                       # clear local time interval list
            
            # Search for major Write IOPS Statistics
            for item in self.Time_Intervals_Write:
                sum1_write = 0;
                for record in self.iopsdata:
                    if ( (record[4] == WRITE) and (record[3] == item) ):
                        sum1_write = sum1_write + 1;      # add the Write IOPS in this particular time interval
                        itotal_write = itotal_write + 1;
                    # end if
                # end for loop
                IOPS_Write_Plot.append(sum1_write);
                if (sum1_write > self.IOPS_Write_peak):
                    self.IOPS_Write_peak = sum1_write;
                    self.IOPS_Write_peak_time = item;
                # end if
            # end for loop
            junk1 = float(itotal_write);
            self.IOPS_Write_Final = 0.0;
            self.IOPS_Write_Final = junk1/runtime;    # Average Write IOPS?
            
            self.IOPS_Write_Plot = list(IOPS_Write_Plot);    # Store Write IOPS for plotting (and later analysis)
            
            #
            # Compute statistics
            #
            self.arthimetic_mean_write = arithmean(IOPS_Write_Plot);                           # Arthimetic Mean (AM_v1)
            self.sigma_am_write = std_dev(IOPS_Write_Plot, self.arthimetic_mean_write)         # Standard Deviation around Arthimentic Mean (v1_sigma)
            self.mad_write = my_abs_deviation(IOPS_Write_Plot,self.arthimetic_mean_write);     # Mean Absolute Deviation  (AM_v2)
            self.mse_write = (self.arthimetic_mean_write*self.arthimetic_mean_write)/float(len(IOPS_Write_Plot));    # Mean Squared Error (MSE) (AM_v3)
            self.median_write = my_median(IOPS_Write_Plot);                                    # Median (v4)
            self.sigma_median_write = std_dev(IOPS_Write_Plot, self.median_write);             # Standard Deviation around Median (v4_sigma)
            self.median_variance_write = self.sigma_median_write*self.sigma_median_write;           # Median Variance (M_v1)
            self.medianad_write = my_abs_deviation(IOPS_Write_Plot,self.median_write);         # Median Absolute Deviation  (M_v2)
            self.mse_median_write = (self.median_variance_write*self.median_variance_write)/float(len(IOPS_Write_Plot));      # Median Squared Error (MSE)   (M_v3)
            
            self.variance_write = self.sigma_am_write*self.sigma_am_write;                          # Variance
        else:
            #
            # If there are no write() calls then just "zero" out stats
            #
            self.IOPS_Write_peak = 0;
            self.IOPS_Write_peak_time = 0;
            self.IOPS_Write_Final = 0;
            self.IOPS_Write_Plot = [];
            
            self.arthimetic_mean_write = 0.0;    # Arthimetic Mean (AM_v1)
            self.sigma_am_write = 0.0;           # Standard Deviation around Arthimentic Mean (v1_sigma)
            self.mad_write = 0.0;                # Mean Absolute Deviation  (AM_v2)
            self.mse_write = 0.0;                # Mean Squared Error (MSE) (AM_v3)
            self.median_write = 0.0;             # Median (v4)
            self.sigma_median_write = 0.0;       # Standard Deviation around Median (v4_sigma)
            self.median_variance_write = 0.0;    # Median Variance (M_v1)
            self.medianad_write = 0.0;           # Median Absolute Deviation  (M_v2)
            self.mse_median_write = 0.0;         # Median Squared Error (MSE)   (M_v3)
            self.variance_write = 0.0;           # Variance
        # end if
        
        #
        # Start with READ Statistics
        #
        if (CmdCounter[READ] > 0):
            
            #
            # Initialization
            #
            sum1_read = 0;
            itotal = 0;                       # Total number of READ function
            self.IOPS_Read_peak = 0;          # Peak REad IOPS
            self.IOPS_Read_peak_time = 0;     # Time interval where Peak Read IOPS occurs
            IOPS_Read_Plot = [];         # Used for plotting
            
            # Find Read time intervals
            #    extract time intervals into local array
            Local_Array = [];
            for item in self.iopsdata:
                if (item[4] == WRITE):
                    junk1 = int(item[3]);
                    Local_Array.append(junk1);
                # end if
            # end for loop
        
            # Count duplicates in time intervals
            Counts = count_dups(Local_Array);
        
            #
            # Create time interval list (all IO operations)
            #
            Time_Intervals_Read = [];
            for item in Counts:
                Time_Intervals_Read.append(item[0]);
            # end for
            Time_Intervals_Read.sort();                               # sort time interval array in ascending order
            self.Time_Intervals_Read = list(Time_Intervals_Read);    # Create time interval list stored in object
            Time_Intervals_Read = [];                                       # clear local time interval list
            
            #
            # Extract all the READ IOPS information (how many in what time interval)
            #
            for item in self.Time_Intervals_Read:
                sum1_read = 0;
                for record in self.iopsdata:
                    if ( (record[4] == READ) and (record[3] == item) ):
                        sum1_read = sum1_read + 1;      # add the READ IOPS in this particular time interval
                        itotal = itotal + 1;
                    # end if
                # end for loop
                IOPS_Read_Plot.append(sum1_read);
                if (sum1_read > self.IOPS_Read_peak):
                    self.IOPS_Read_peak = sum1_read;
                    self.IOPS_Read_peak_time = item;
                # end if
            # end for loop
            junk1 = float(itotal);
            self.IOPS_Read_Final = 0.0;
            self.IOPS_Read_Final = junk1/runtime;    # Average Read IOPS?
            
            self.IOPS_Read_Plot = list(IOPS_Read_Plot);    # Store Read IOPS for plotting (and later analysis)
            
            #
            # Compute statistics
            #
            self.arthimetic_mean_read = arithmean(IOPS_Read_Plot);                          # Arthimetic Mean (AM_v1)
            self.sigma_am_read = std_dev(IOPS_Read_Plot, self.arthimetic_mean_read)         # Standard Deviation around Arthimentic Mean (v1_sigma)
            self.mad_read = my_abs_deviation(IOPS_Read_Plot,self.arthimetic_mean_read);     # Mean Absolute Deviation  (AM_v2)
            self.mse_read = (self.arthimetic_mean_read*self.arthimetic_mean_read)/float(len(IOPS_Read_Plot));    # Mean Squared Error (MSE) (AM_v3)
            self.median_read = my_median(IOPS_Read_Plot);                                   # Median (v4)
            self.sigma_median_read = std_dev(IOPS_Read_Plot, self.median_read);             # Standard Deviation around Median (v4_sigma)
            self.median_variance_read = self.sigma_median_read*self.sigma_median_read;           # Median Variance (M_v1)
            self.medianad_read = my_abs_deviation(IOPS_Read_Plot,self.median_read);         # Median Absolute Deviation  (M_v2)
            self.mse_median_read = (self.median_variance_read*self.median_variance_read)/float(len(IOPS_Read_Plot));      # Median Squared Error (MSE)   (M_v3)
            self.variance_read = self.sigma_am_read*self.sigma_am_read;                          # Variance
            IOPS_Read_Plot = [];
        else:
            #
            # If there are no write() calls then just "zero" out stats
            #
            self.IOPS_Read_peak = 0;
            self.IOPS_Read_peak_time = 0;
            self.IOPS_Read_Final = 0;
            self.IOPS_Read_Plot = [];
            
            self.arthimetic_mean_read = 0.0;    # Arthimetic Mean (AM_v1)
            self.sigma_am_read = 0.0;           # Standard Deviation around Arthimentic Mean (v1_sigma)
            self.mad_read = 0.0;                # Mean Absolute Deviation  (AM_v2)
            self.mse_read = 0.0;                # Mean Squared Error (MSE) (AM_v3)
            self.median_read = 0.0;             # Median (v4)
            self.sigma_median_read = 0.0;       # Standard Deviation around Median (v4_sigma)
            self.median_variance_read = 0.0;    # Median Variance (M_v1)
            self.medianad_read = 0.0;           # Median Absolute Deviation  (M_v2)
            self.mse_median_read = 0.0;         # Median Squared Error (MSE)   (M_v3)
            self.variance_read = 0.0;           # Variance
        # end if
        
        #
        # Step 4 - Get Total IOPS Statistics
        #
        
        #
        # Step 1 - extract time intervals into local array (all IO operations)
        #
        Local_Array = [];
        for item in self.iopsdata:
            junk1 = int(item[3]);
            Local_Array.append(junk1);
        # end for loop
        
        # Count duplicates in time intervals
        Counts = count_dups(Local_Array);
        
        #
        # Create time interval list (all IO operations)
        #
        Time_Intervals = [];
        for item in Counts:
            Time_Intervals.append(item[0]);
        # end for
        Time_Intervals.sort();                         # sort time interval array in ascending order
        self.Time_Intervals = list(Time_Intervals);    # Create time interval list stored in object
        Time_Intervals = [];                           # clear local time interval list
        
        
        #
        # Initialization
        #
        sum1_total = 0.0;
        itotal = 0;
        self.IOPS_Total_peak = 0;
        self.IOPS_Total_peak_time = 0.0;
        IOPS_Total_Plot = [];        # Used for plotting
        
        #
        # Extract all the TOTAL IOPS information (how many in what time interval)
        #
        for item in self.Time_Intervals:
            sum1_total = 0;
            for record in self.iopsdata:
                if (record[3] == item):
                    sum1_total = sum1_total + 1;   # add the IOPS in this particular time interval
                    itotal = itotal + 1;
                # end if
            # end for loop
            IOPS_Total_Plot.append(sum1_total);
            if (sum1_total > self.IOPS_Total_peak):
                self.IOPS_Total_peak = sum1_total;
                self.IOPS_Total_peak_time = item;
            # end if
        # end for loop
        junk1 = float(itotal);
        self.IOPS_Total_Final = 0.0;
        self.IOPS_Total_Final = junk1/runtime;
        
        self.IOPS_Total_Plot = list(IOPS_Total_Plot);    # Store TOTAL IOPS for plotting (and later analysis)
        
        #
        # Compute statistics
        #
        self.arthimetic_mean_total = arithmean(IOPS_Total_Plot);                           # Arthimetic Mean (AM_v1)
        print "self.arthimetic_mean_total: ",self.arthimetic_mean_total
        self.sigma_am_total = std_dev(IOPS_Total_Plot, self.arthimetic_mean_total)         # Standard Deviation around Arthimentic Mean (v1_sigma)
        self.mad_total = my_abs_deviation(IOPS_Total_Plot,self.arthimetic_mean_total);     # Mean Absolute Deviation  (AM_v2)
        self.mse_total = (self.arthimetic_mean_total*self.arthimetic_mean_total)/float(len(IOPS_Total_Plot));    # Mean Squared Error (MSE) (AM_v3)
        self.median_total = my_median(IOPS_Total_Plot);                                    # Median (v4)
        self.sigma_median_total = std_dev(IOPS_Total_Plot, self.median_total);             # Standard Deviation around Median (v4_sigma)
        self.median_variance_total = self.sigma_median_total*self.sigma_median_total;           # Median Variance (M_v1)
        self.medianad_total = my_abs_deviation(IOPS_Total_Plot,self.median_total);         # Median Absolute Deviation  (M_v2)
        self.mse_median_total = (self.median_variance_total*self.median_variance_total)/float(len(IOPS_Total_Plot));      # Median Squared Error (MSE)   (M_v3)
        self.variance_total = self.sigma_am_total*self.sigma_am_total;                     # Variance
        
    # end def
    
    
    
    #
    # Write iops statistics to stdout and HTML
    #
    def iops_output_stats(self, f, CmdCounter, BeginTime, EndTime, WRITE, READ, VFLAGS, dirname, currentfigure):
        
        #
        # IOPS output header
        #
        self.iops_header(f);
        
        #
        # Compute IOPS Stats
        #
        self.getstats(CmdCounter, BeginTime, EndTime, WRITE, READ, VFLAGS);
        
        #
        # Write IOPS output:
        #
        if (CmdCounter[WRITE] > 0):
            currentfigure2 = self.write_iops_stats(f, CmdCounter, VFLAGS, dirname, currentfigure);
            currentfigure = currentfigure2;
        else:
            print "   No Write IO functions. Maximum Write IOPS = 0.0";
            print "   Write IOPS = 0.0";
            print "   No Write IOPS so no statistics";
            output_str = "</UL \n\n";
            output_str = "No Write IOPS so no Write IOPS Statistics. \n";
            output_str = "</P> \n \n";
            f.write(output_str);
        # end if
        
        #
        # Read IOPS output:
        #
        if (CmdCounter[READ] > 0):
            currentfigure2 = self.read_iops_stats(f, CmdCounter, VFLAGS, dirname, currentfigure);
            currentfigure = currentfigure2;
        else:
            print "   No Read IO functions. Maximum Read IOPS = 0.0";
            print "   Read IOPS = 0.0";
            print "   No Read IOPS so no statistics";
            output_str = "</UL \n\n";
            output_str = "No Read IOPS so no Read IOPS Statistics. \n";
            output_str = "</P> \n \n";
            f.write(output_str);
        # end if
        
        #
        # Total IOPS output:
        #
        currentfigure2 = self.total_iops_stats(f, CmdCounter, VFLAGS, dirname, currentfigure);
        currentfigure = currentfigure2;
        
        #
        # IOPS summary
        #
        print " ";
        print "********************";
        print "Final IOPS report";
        print "   Note: Average is based on total IOPS divided by total runtime. The values";
        print "         will be different than what was reported previously";
        print " ";
        print "Maximum Write IOPS = ",commify3(self.IOPS_Write_peak),"  occured at ",commify3(self.IOPS_Write_peak_time)," seconds";
        junk2 = num_output(self.arthimetic_mean_write,5);
        print "Average Write IOPS = ",commify3(junk2);
        print " ";
        print "Maximum Read IOPS = ",commify3(self.IOPS_Read_peak),"  occured at ",commify3(self.IOPS_Read_peak_time)," seconds";
        junk2 = num_output(self.arthimetic_mean_read,5);
        print "Average Read IOPS = ",commify3(junk2);
        print " ";
        print "Maximum Total IOPS = ",commify3(self.IOPS_Total_peak),"  occured at ",commify3(self.IOPS_Total_peak_time)," seconds";  
        junk2 = num_output(self.arthimetic_mean_total,5); 
        print "Average Total IOPS = ",commify3(junk2);
        print " "
        print "********************";
        print " "
        print " "
        print " "
   
        output_str = "<P> \n";
        output_str = output_str + "The following statistical data is for the peak and average IOPS.  \n";
        output_str = output_str + "The peak IOPS is defined as the second time interval where the number \n";
        output_str = output_str + "IOPS is greatest. The average IOPS is defined as the the sum of all  \n";
        output_str = output_str + "IOPS divided by the run time of the application. <BR><BR>  \n";
        output_str = output_str + "<strong>Maximum Write IOPS</strong> = " + commify3(self.IOPS_Write_peak) + "&nbsp &nbsp time: " + commify3(self.IOPS_Write_peak_time) + " (secs) \n";
        output_str = output_str + "<BR> \n";
        output_str = output_str + "<strong>Average Write IOPS</strong> = " + commify3(self.IOPS_Write_Final) +" \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "<strong>Maximum Read IOPS</strong> = " + commify3(self.IOPS_Read_peak) + "&nbsp &nbsp time: " + commify3(self.IOPS_Read_peak_time) + " (secs) \n";
        output_str = output_str + "<BR> \n";
        output_str = output_str + "<strong>Average Read IOPS</strong> = " + commify3(self.IOPS_Read_Final) +" \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "<strong>Maximum Total IOPS</strong> = " + commify3(self.IOPS_Total_peak) + "&nbsp &nbsp time: " + commify3(self.IOPS_Write_peak_time) + " (secs) \n";
        output_str = output_str + "<BR> \n";
        output_str = output_str + "<strong>Average Total IOPS</strong> = " + commify3(self.IOPS_Total_Final) +" \n";
        output_str = output_str + "<BR> \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + "<BR> \n";
        output_str = output_str + " \n";
        f.write(output_str); 
    
        return currentfigure;
    # end def
    
    
    #
    # Write out HTML write statistics header
    #
    def iops_header(self,f):

        print " ";
        print "--------------------- ";
        print "-- IOPS Statistics -- ";
        print "--------------------- ";
        print " ";
        print "This section reports the IOPS Statistics for the application. The first set of";
        print "statistics is computed by dividing the application run into 1 second intervals";
        print "and couting the number of write() functions, read() functions, and any IO ";
        print "function that this tool tracks, in each interval. This is defined as the particular";
        print "IOPS for that time interval, resulting in a time distribution of Write IOPS,";
        print "Read IOPS, and Total IOPS.";
        print " "
        print "Then Statistics are computed on those values. Statistics such as the average mean";
        print "(the classic average) and the median are computed as well as standard deviations,";
        print "variance, mean absolute deviation, and mean squared error (MSE). This is done";
        print "for Write IOPS, Read IOPS, and Total IOPS.";
        print " ";
        print "At the end of this section the peak Write IOPS value, peak Read IOPS, and peak ";
        print "Total IOPS value, are presented and at what time interval they occurred relative";
        print "to beginning of the run. Also presented is the average IOPS value where the ";
        print "average is computed by adding all of the particular IO operations and dividing";
        print "by the total run time."
        print " ";
   
        # HTML report output (top of section)
        output_str = " \n";
        output_str = output_str + "<hr /> \n";
        output_str = output_str + "<H3> \n"
        output_str = output_str + "8. <a id=\"iops_stat\">IOPS Statistics</a> \n";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P> \n";
        f.write(output_str);
        output_str = "This section reports the IOPS Statistics for the application. The first set of \n";
        output_str = output_str + "statistics is computed by dividing the application run into 1 second intervals \n";
        output_str = output_str + "and couting the number of write() functions, read() functions, and any IO  \n";
        output_str = output_str + "function that this tool tracks, in each interval. This is defined as the particular \n";
        output_str = output_str + "IOPS for that time interval, resulting in a time distribution of Write IOPS, \n";
        output_str = output_str + "Read IOPS, and Total IOPS. Plots of the time distribution of these are also presented. \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + "  \n"
        output_str = output_str + "<P> \n";
        output_str = output_str + "Then Statistics are computed on those values. Statistics such as the average mean \n";
        output_str = output_str + "(the classic average) and the median are computed as well as standard deviations, \n";
        output_str = output_str + "variance, mean absolute deviation, and mean squared error (MSE). This is done \n";
        output_str = output_str + "for Write IOPS, Read IOPS, and Total IOPS. \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + "  \n";
        output_str = output_str + "<P> \n";
        output_str = output_str + "At the end of this section the peak Write IOPS value, peak Read IOPS, and peak  \n";
        output_str = output_str + "Total IOPS value, are presented and at what time interval they occurred relative \n";
        output_str = output_str + "to beginning of the run. Also presented is the average IOPS value where the  \n";
        output_str = output_str + "average is computed by adding all of the particular IO operations and dividing \n";
        output_str = output_str + "by the total run time. \n"
        output_str = output_str + "</P> \n";
        output_str = output_str + "  \n";
        f.write(output_str);
   
    # end def
    
    
    
    #
    # Write out the WRITE IOPS (stdout, HTML)
    #
    def write_iops_stats(self, f, CmdCount, VFLAGS, dirname, currentfigure):
        
        #
        # Write IOPS vs Time Plot
        #
        if (VFLAGS >= 2):
            currentfigure = currentfigure + 1;
            
            plt.plot(self.Time_Intervals_Write, self.IOPS_Write_Plot, marker="o", linestyle="none", color="b");
            plt.title("Write IOPS History", fontsize='x-small');
            plt.xlabel("Time (secs) - Relative to beginning of run", fontsize='x-small');
            plt.ylabel("Write IOPS", fontsize='x-small');
            plt.xticks(rotation=35, fontsize='x-small');
            plt.yticks(fontsize='x-small');
            plot_name = dirname + "/write_iops_time_history";
            plt.savefig(plot_name);
            plt.close();
            
            # HTML Output:
            output_str = "<P> \n";
            output_str = output_str + "Figure "+str(currentfigure)+" below is a time history of the Write IOPS in one \n";
            output_str = output_str + "second intervals. <BR>\n";
            f.write(output_str);
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"write_iops_time_history.png\"> \n";
            output_str = output_str + "<BR><BR><strong>Figure "+str(currentfigure)+" - Write IOPS Time history</strong></center><BR><BR> \n";
            output_str = output_str + "</P> <BR> \n";
            f.write(output_str);
        # endif
        
        # stdout:
        print " ";
        print "Write IOPS Statistics:"
        print " ";
        print "   Maximum Write IOPS = ",commify3(self.IOPS_Write_peak),"  occured at ",commify3(self.IOPS_Write_peak_time)," seconds";
        print " "
        
        # HTML:
        output_str = "<P> \n";
        output_str = output_str + "<strong>Write IOPS Statistics:</strong> \n";
        output_str = output_str + "<BR> <BR>\n";
        f.write(output_str);
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>Maximum Write IOPS = " + commify3(self.IOPS_Write_peak) + "  occured at ";
        output_str = output_str + commify3(self.IOPS_Write_peak_time) + " seconds \n";
        output_str = output_str + "<BR> \n";
        f.write(output_str);
        
        #
        # Write out Write IOPS statistics (stdout and HTML)
        #
        
        # HTML:
        # Average (mean or arthimetic mean):
        #   Location, spread, and skewness measures
        junk2 = num_output(self.arthimetic_mean_write,5);
        junk3 = commify3( junk2 );
        print "   Average (arthimetic mean or AM) Write IOPS = ",junk3;   # stdout
        output_str = "   <LI>Average (arthimetic mean or AM) Write IOPS = ";
        output_str = output_str + str(junk3) + "\n";
        f.write(output_str);
        if (self.arthimetic_mean_write != 0.0):
            junk4 = (self.sigma_am_write/self.arthimetic_mean_write)*100.0;
            junk1 = num_output(self.sigma_am_write,5);
            junk1b = commify3( junk1 );
            junk2 = "%.2f" % junk4;
            junk2b = commify3( junk2 );
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "      AM Standard Deviation Write IOPS = ",junk1b,"  (",junk3," of AM)";   # stdout
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>AM Standard Deviation Write IOPS = \n";
        output_str = output_str + str(junk1b) + "  (" + str(junk3) + " of AM) \n";
        f.write(output_str);
        
        # Variance  (AM_v1)
        junk1 = num_output(self.variance_write,5);
        junk1b = commify3(junk1);
        print "   Variance in Write IOPS = ",junk1b;   # stdout
        output_str = "      <LI>Variance in number Write IOPS = " + str(junk1b) + " \n";
        f.write(output_str);
        
        # Mean Absolute Deviation
        junk2 = num_output(self.mad_write,5);
        junk2b = commify3(junk2);
        print "      Mean Absolute Deviation for Write IOPS = ",junk2b;   # stdout
        output_str = "      <LI>Mean Absolute Deviation for Write IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        
        # Mean Squared Error (MSE)
        junk2 = num_output(self.mse_write,5);
        junk2b = commify3(junk2);
        print "      Mean Squared Error (MSE) in Write IOPS = ",junk2b;   # stdout
        output_str = "      <LI>Mean Squared Error (MSE) in Write IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        
        # Median
        #   Location, spread, and skewness measures
        junk2 = num_output(self.median_write,5);
        junk3 = commify3( junk2 );
        print " ";
        print "   Median Write IOPS = ",junk3;
        output_str = "   <LI>Median Write IOPS = " + junk3 + " \n";
        f.write(output_str);
        
        if (self.median_write != 0.0):
            junk4 = (self.sigma_median_write/self.median_write)*100.0;
            junk1 = num_output(self.sigma_median_write,5);
            junk1b = commify3(junk1);
            junk2 = "%.2f" % junk4;
            junk2b = commify3(junk2);
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "      Median Standard Deviation Write IOPS = ",junk1b,"  (",junk3," of Median)";
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>Median Standard Deviation Write IOPS = ";
        output_str = output_str + str(junk1b) + "  (" + str(junk3) + " of Median) \n";
        f.write(output_str);
        
        # Median Variance
        junk1 = num_output(self.median_variance_write,5);
        junk1b = commify3(junk1);
        print "      Variance in Write IOPS using Median = ",junk1b;
        output_str = "      <LI>Variance in Write IOPS using Median = ";
        output_str = output_str + str(junk1b) + " \n";
        f.write(output_str);
        
        # Median Absolute Deviation
        junk2 = num_output(self.medianad_write,5);
        junk2b = commify3(junk2);
        print "      Median Absolute Deviation Write IOPS = ",junk2b;
        output_str = "      <LI>Median Absolute Deviation Write IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        
        # Median Squared Error (MSE)
        junk2 = num_output(self.mse_median_write,5);
        junk2b = commify3(junk2);
        print "      Median Squared Error (MSE) Write IOPS = ",junk2b;
        output_str = "      <LI>Median Squared Error (MSE) Write IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        output_str = "</P> \n \n";
        f.write(output_str);
        
        print " ";
        
        return currentfigure;
    # end def
    
    
    #
    # Write out the READ IOPS (stdout, HTML)
    #
    def read_iops_stats(self, f, CmdCount, VFLAGS, dirname, currentfigure):
        
        # =========
        # Read IOPS
        # =========
        
        #
        # Read IOPS vs Time Plot
        #
        
        # Extract Read IOPS data
        if (VFLAGS >= 2):
            
            currentfigure = currentfigure + 1;
            plt.plot(self.Time_Intervals_Read, self.IOPS_Read_Plot, marker="o", linestyle="none", color="b");
            plt.title("Read IOPS History", fontsize='x-small');
            plt.xlabel("Time (secs) - Relative to beginning of run", fontsize='x-small');
            plt.ylabel("Read IOPS", fontsize='x-small');
            plt.xticks(rotation=35, fontsize='x-small');
            plt.yticks(fontsize='x-small');
            plot_name = dirname + "/read_iops_time_history";
            plt.savefig(plot_name);
            plt.close();
            
            # HTML Output:
            output_str = "<BR> <BR> \n";
            f.write(output_str);
            output_str = "<P> \n";
            output_str = output_str + "Figure "+str(currentfigure)+" below is a time history of the Read IOPS in one \n";
            output_str = output_str + "second intervals. <BR>\n";
            f.write(output_str);
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"read_iops_time_history.png\"> \n";
            output_str = output_str + "<BR><BR><strong>Figure "+str(currentfigure)+" - Read IOPS Time history</strong></center><BR><BR> \n";
            output_str = output_str + "</P> <BR> \n";
            f.write(output_str);
        # end if

        # stdout:
        print " ";
        print "Read IOPS Statistics:"
        print " ";
        print "   Maximum Read IOPS = ",commify3(self.IOPS_Read_peak),"  occured at ",commify3(self.IOPS_Read_peak_time)," seconds";
        print " "
        
        # HTML:
        output_str = "<P> \n";
        output_str = output_str + "<strong>Read IOPS Statistics:</strong> \n";
        output_str = output_str + "<BR> \n";
        f.write(output_str);
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>Maximum Read IOPS = " + commify3(self.IOPS_Read_peak) + "  occured at ";
        output_str = output_str + commify3(self.IOPS_Read_peak_time) + " seconds \n";
        output_str = output_str + "<BR> \n";
        f.write(output_str);
        
        #
        # Compute Read IOPS statistics
        #
        
        # HTML:
        # Average (mean or arthimetic mean):
        #   Location, spread, and skewness measures
        junk2 = num_output(self.arthimetic_mean_read,5);
        junk3 = commify3( junk2 );
        print "   Average (arthimetic mean or AM) Read IOPS = ",junk3;   # stdout
        output_str = "   <LI>Average (arthimetic mean or AM) Read IOPS = ";
        output_str = output_str + str(junk3) + "\n";
        f.write(output_str);
        if (self.arthimetic_mean_read != 0.0):
            junk4 = (self.sigma_am_read/self.arthimetic_mean_read)*100.0;
            junk1 = num_output(self.sigma_am_read,5);
            junk1b = commify3( junk1 );
            junk2 = "%.2f" % junk4;
            junk2b = commify3( junk2 );
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "      AM Standard Deviation Read IOPS = ",junk1b,"  (",junk3," of AM)";   # stdout
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>AM Standard Deviation Read IOPS = \n";
        output_str = output_str + str(junk1b) + "  (" + str(junk3) + " of AM) \n";
        f.write(output_str);
        
        # Variance  (AM_v1)
        junk1 = num_output(self.variance_read,5);
        junk1b = commify3(junk1);
        print "   Variance in Read IOPS = ",junk1b;   # stdout
        output_str = "      <LI>Variance in number Read IOPS = " + str(junk1b) + " \n";
        f.write(output_str);
        
        # Mean Absolute Deviation
        junk2 = num_output(self.mad_read,5);
        junk2b = commify3(junk2);
        print "      Mean Absolute Deviation for Read IOPS = ",junk2b;   # stdout
        output_str = "      <LI>Mean Absolute Deviation for Read IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        
        # Median
        #   Location, spread, and skewness measures
        junk2 = num_output(self.median_read,5);
        junk3 = commify3( junk2 );
        print " ";
        print "   Median Read IOPS = ",junk3;
        output_str = "   <LI>Median Read IOPS = " + junk3 + " \n";
        f.write(output_str);
        
        if (self.median_read != 0.0):
            junk4 = (self.sigma_median_read/self.median_read)*100.0;
            junk1 = num_output(self.sigma_median_read,5);
            junk1b = commify3(junk1);
            junk2 = "%.2f" % junk4;
            junk2b = commify3(junk2);
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "      Median Standard Deviation Read IOPS = ",junk1b,"  (",junk3," of Median)";
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>Median Standard Deviation Read IOPS = ";
        output_str = output_str + str(junk1b) + "  (" + str(junk3) + " of Median) \n";
        f.write(output_str);
        
        # Median Variance
        junk1 = num_output(self.median_variance_read,5);
        junk1b = commify3(junk1);
        print "      Variance in Read IOPS using Median = ",junk1b;
        output_str = "      <LI>Variance in Read IOPS using Median = ";
        output_str = output_str + str(junk1b) + " \n";
        f.write(output_str);
        
        # Median Absolute Deviation
        junk2 = num_output(self.medianad_read,5);
        junk2b = commify3(junk2);
        print "      Median Absolute Deviation Read IOPS = ",junk2b;
        output_str = "      <LI>Median Absolute Deviation Read IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        
        # Median Squared Error (MSE)
        junk2 = num_output(self.mse_median_read,5);
        junk2b = commify3(junk2);
        print "      Median Squared Error (MSE) Read IOPS = ",junk2b;
        output_str = "      <LI>Median Squared Error (MSE) Read IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        output_str = "</P> \n \n";
        f.write(output_str);
        
        print " ";
        
        return currentfigure;
    # end def
    
    
    
    #
    # Write out the TOTAL IOPS (stdout, HTML)
    #
    def total_iops_stats(self, f, CmdCount, VFLAGS, dirname, currentfigure):
        
        # ==========
        # Total IOPS
        # ==========
        
        #
        # Total IOPS vs Time Plot
        #
        
        # Extract Total IOPS data
        if (VFLAGS >= 2):
            
            currentfigure = currentfigure + 1;
            plt.plot(self.Time_Intervals, self.IOPS_Total_Plot, marker="o", linestyle="none", color="b");
            plt.title("Total IOPS History", fontsize='x-small');
            plt.xlabel("Time (secs) - Relative to beginning of run", fontsize='x-small');
            plt.ylabel("Total IOPS", fontsize='x-small');
            plt.xticks(rotation=35, fontsize='x-small');
            plt.yticks(fontsize='x-small');
            plot_name = dirname + "/total_iops_time_history";
            plt.savefig(plot_name);
            plt.close();
            
            # HTML Output:
            output_str = "<BR> <BR> \n";
            f.write(output_str);
            output_str = "<P> \n";
            output_str = output_str + "Figure "+str(currentfigure)+" below is a time history of the Total IOPS in one \n";
            output_str = output_str + "second intervals. <BR>\n";
            f.write(output_str);
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"total_iops_time_history.png\"> \n";
            output_str = output_str + "<BR><BR><strong>Figure "+str(currentfigure)+" - Total IOPS Time history</strong></center><BR><BR> \n";
            output_str = output_str + "</P> <BR> \n";
            f.write(output_str);
        # end if
        
        # stdout:
        print " ";
        print "Total IOPS Statistics:"
        print " ";
        print "   Maximum Total IOPS = ",commify3(self.IOPS_Total_peak),"  occured at ",commify3(self.IOPS_Total_peak_time)," seconds";
        print " "
        
        # HTML:
        output_str = "<P> \n";
        output_str = output_str + "<strong>Total IOPS Statistics:</strong> \n";
        output_str = output_str + "<BR> \n";
        f.write(output_str);
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>Maximum Total IOPS = " + commify3(self.IOPS_Total_peak) + "  occured at ";
        output_str = output_str + commify3(self.IOPS_Total_peak_time) + " seconds \n";
        output_str = output_str + "<BR> \n";
        f.write(output_str);
        
        #
        # Compute Total IOPS statistics
        #
        
        # HTML:
        # Average (mean or arthimetic mean):
        #   Location, spread, and skewness measures
        junk2 = num_output(self.arthimetic_mean_total,5);
        junk3 = commify3( junk2 );
        print "   Average (arthimetic mean or AM) Total IOPS = ",junk3;   # stdout
        output_str = "   <LI>Average (arthimetic mean or AM) Total IOPS = ";
        output_str = output_str + str(junk3) + "\n";
        f.write(output_str);
        if (self.arthimetic_mean_total != 0.0):
            junk4 = (self.sigma_am_total/self.arthimetic_mean_total)*100.0;
            junk1 = num_output(self.sigma_am_total,5);
            junk1b = commify3( junk1 );
            junk2 = "%.2f" % junk4;
            junk2b = commify3( junk2 );
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "      AM Standard Deviation Total IOPS = ",junk1b,"  (",junk3," of AM)";   # stdout
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>AM Standard Deviation Total IOPS = \n";
        output_str = output_str + str(junk1b) + "  (" + str(junk3) + " of AM) \n";
        f.write(output_str);
        
        # Variance  (AM_v1)
        junk1 = num_output(self.variance_total,5);
        junk1b = commify3(junk1);
        print "   Variance in Total IOPS = ",junk1b;   # stdout
        output_str = "      <LI>Variance in number Total IOPS = " + str(junk1b) + " \n";
        f.write(output_str);
        
        # Mean Absolute Deviation
        junk2 = num_output(self.mad_total,5);
        junk2b = commify3(junk2);
        print "      Mean Absolute Deviation for Total IOPS = ",junk2b;   # stdout
        output_str = "      <LI>Mean Absolute Deviation for Total IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        
        # Median
        #   Location, spread, and skewness measures
        junk2 = num_output(self.median_total,5);
        junk3 = commify3( junk2 );
        print " ";
        print "   Median Total IOPS = ",junk3;
        output_str = "   <LI>Median Total IOPS = " + junk3 + " \n";
        f.write(output_str);
        
        if (self.median_total != 0.0):
            junk4 = (self.sigma_median_total/self.median_total)*100.0;
            junk1 = num_output(self.sigma_median_total,5);
            junk1b = commify3(junk1);
            junk2 = "%.2f" % junk4;
            junk2b = commify3(junk2);
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        #endif
        print "      Median Standard Deviation Total IOPS = ",junk1b,"  (",junk3," of Median)";
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>Median Standard Deviation Total IOPS = ";
        output_str = output_str + str(junk1b) + "  (" + str(junk3) + " of Median) \n";
        f.write(output_str);
        
        # Median Variance
        junk1 = num_output(self.median_variance_total,5);
        junk1b = commify3(junk1);
        print "      Variance in Total IOPS using Median = ",junk1b;
        output_str = "      <LI>Variance in Total IOPS using Median = ";
        output_str = output_str + str(junk1b) + " \n";
        f.write(output_str);
        
        # Median Absolute Deviation
        junk2 = num_output(self.medianad_total,5);
        junk2b = commify3(junk2);
        print "      Median Absolute Deviation Total IOPS = ",junk2b;
        output_str = "      <LI>Median Absolute Deviation Total IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        
        # Median Squared Error (MSE)
        junk2 = num_output(self.mse_median_total,5);
        junk2b = commify3(junk2);
        print "      Median Squared Error (MSE) Total IOPS = ",junk2b;
        output_str = "      <LI>Median Squared Error (MSE) Total IOPS = ";
        output_str = output_str + str(junk2b) + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        output_str = "</P> \n \n";
        f.write(output_str);
        
        print " ";
        
        return currentfigure;
    # end def



# end class iops




