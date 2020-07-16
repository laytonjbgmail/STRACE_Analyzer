#!/usr/bin/python
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

try:
    from strace_output import *
except:
    print "Cannot find strace_output python file. This is needed for this application.";
    print "Stopping.";
    sys.exit();
# end try



#
#
# Open() Class definition
#
#
class openclass:

# Instantiated Object stores data as self.opendata. This is a list of lists (2D list).
# Each row of the list consists of a record. Each record consists of:
#
#
# Each record stored in object consists of:
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   filename       (filename for file being opened)
#   unit           (file descriptor associated with file)
#   elapsed_time   (elapsed time for open)
#
#
# There are methods (functions) that add, read, extract, and manipulate
# this data. Many of these methods store results as part of the object
#
#
    
    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.opendata = [];
    # end if
    
    
    #
    # This function appenda data to self.opendata
    #    
    def storeopen(self,data):
        self.opendata.append(data)
    # end if
    
    
    #
    # Return the list to caller
    #
    def getopen(self):
        return self.opendata;
    # end if
    
    
    #
    # Get list of times for all open()
    #    
    def get_elapsed_time(self):
        elapsed_time = [];
        for item in self.opendata:
            elapsed_time.append(float(item[4]));
        # end for
        self.elapsed_time = elapsed_time;
        return elapsed_time;
    # end def
    
    
    #
    # Compute statistics on self.opendata
    #
    def getstats(self, BeginTime):
        #
        # Compute statistics
        #
        if (len(self.opendata) > 0):
            #
            # Initialization:
            #
            Opensmall_junk = 1000000000.0;
            Openlarge_junk = -1.0;
            total_open_time = 0.0;
            junk1_line = -1;
            junk2_line = -1;
            
            #
            # Extract all the elapsed time information (bytes per open() call)
            #    Also find the following:
            #        1. fastest and slowest open() calls
            #
            self.get_elapsed_time();
            
            for item in self.opendata:
                elapsed_time = float(item[4]);
                linenum = item[0];
                
                # Fastest and slowest open() times
                if (elapsed_time > Openlarge_junk):
                    Openlarge_junk = float(elapsed_time);
                    junk1_line = item[0];
                elif (elapsed_time < Opensmall_junk):
                    Opensmall_junk = float(elapsed_time);
                    junk2_line = item[0];
                # end if
                total_open_time = total_open_time + elapsed_time;
            # end for
            self.total_open_time = total_open_time;
           
            # Store results from loop into data structures (added to self further down in the code)
            self.OpenMax = {};
            self.OpenMin = {};
            self.OpenMax["MaxTime"] = Openlarge_junk;
            self.OpenMax["line"] = junk1_line;
            self.OpenMin["MinTime"] = Opensmall_junk;
            self.OpenMin["line"] = junk2_line;
            
            #
            # Compute statistics on Open() elapsed time payload
            #
            self.arthimetic_mean = arithmean(self.elapsed_time);                        # Arthimetic Mean (average)
            self.sigma_am = std_dev(self.elapsed_time, self.arthimetic_mean)            # Standard Deviation around Arthimentic Mean
            self.mode = My_Mode(self.elapsed_time);                                     # Mode  (returns a list)
            self.open_range = max(self.elapsed_time) - min(self.elapsed_time);         # Range
            self.variance = self.sigma_am*self.sigma_am;                                # Variance
            self.mad = my_abs_deviation(self.elapsed_time,self.arthimetic_mean);        # Mean Absolute Deviation
            self.mse = (self.variance)/float(len(self.elapsed_time));                   # Mean Squared Error (MSE)
            self.median = my_median(self.elapsed_time);                                 # Median
            self.sigma_median = std_dev(self.elapsed_time, self.median);                # Standard Deviation around Median
            self.median_variance = self.sigma_median*self.sigma_median;                 # Median Variance
            self.medianad = my_abs_deviation(self.elapsed_time, self.median);           # Median Absolute Deviation
            self.mse_median = self.median_variance/float(len(self.elapsed_time));       # Median Squared Error (MSE)
            self.skewness_mean = my_skewness(self.elapsed_time, self.arthimetic_mean);  # Fisher-Pearson Generalized moment (skewness measure) - g1
            self.FP_coeff = my_fp_coeff(self.elapsed_time, self.arthimetic_mean);       # Adjusted Fisher-Pearson standardized moment coefficient - G1
            self.sk2 = my_sk2(self.arthimetic_mean, self.median, self.sigma_am);        # SK2 (Pearson 2 skewness coefficient)
            self.kurtosis_v1 = my_kurtosis(self.elapsed_time, self.arthimetic_mean);    # Kurtosis
        else:
            self.OpenMax = {};
            self.OpenMin = {};
            self.OpenMax["MaxTime"] = 0.0;
            self.OpenMax["line"] = 0;
            self.OpenMin["MinTime"] = 0.0;
            self.OpenMin["line"] = 0;
            
            self.arthimetic_mean = 0.0;
            self.sigma_am = 0.0;
            self.mode = [];
            self.open_range = 0;
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
        # end if
    # end def    

    
    #
    # Write open() statistics to stdout and HTML
    #
    def open_statistics(self, f, dirname, FileSizes, FileSizeCounter, BeginTime,
                        EndTime, currentfigure, VFLAGS, matplotlib_var, numpy_var,
                        CmdCounter, OPEN):
        # Initialization:
        bincount = 100;
        
        # Get elapsed time for open() functions
        self.get_elapsed_time();
        
        # Compute stats
        self.getstats(BeginTime);
        
        # Write out statistics output section header (stdout and HTML)

        self.open_header(f, currentfigure);
        
        if (VFLAGS >= 2):
            if ( (matplotlib_var > 0) and (numpy_var > 0) ):
                # Increment currentfigure number
                currentfigure = currentfigure + 1;
                
                if (len(self.elapsed_time) > 0):
                    # Create plots for close() function
                    self.open_plot(f, dirname, bincount, currentfigure);
                else:
                    output_str = "No open functions in the strace output. \n";
                    output_str = output_str + "<BR>";
                    f.write(output_str);
                # end if
            # end if
        # end if
        
        if (len(self.elapsed_time) > 0):
            
            # Finish statistical output
            output_str = "<BR <BR> \n";
            output_str = output_str + "This sub-section presents statistical information about the open() functions in the \n";
            output_str = output_str + "application. Below are the statistics across all files in the analysis. \n";
            output_str = output_str + "<BR><BR> \n";
            f.write(output_str);
            
            #
            # statistics output header - stdout
            #
            print " ";
            print "-- Open() Statistical Summary -- ";
            print " ";
            
            # Total number of open() function calls:
            junk1 = CmdCounter[OPEN];
            print "Total number of open function calls = ", junk1;
            # HTML:
            output_str = "<UL> \n";
            f.write(output_str);
            output_str = "   <LI>Total number of Open Function Calls = " + commify3(CmdCounter[OPEN]) + " \n";
            f.write(output_str);
            output_str = "</UL> \n";
            f.write(output_str);
            
            # Range:
            junk1a = commify3(self.open_range);
            print "Range of open() function calls: ",junk1a," secs";
            # HTML
            output_str = "<UL> \n";
            output_str = output_str + "   <LI>Range of open() function calls = " + junk1a + " secs \n";
            f.write(output_str);
            output_str = "</UL> \n";
            f.write(output_str);
            
            # Average (mean or arthimetic mean):
            #   Location, spread, and skewness measures
            self.mean_output(f);
            
            # Median
            #   Location, spread, and skewness measures
            self.median_output(f);
            
            # Skewness:
            self.skewness_output(f);
            
            # Other Stats:
            self.other_stats(f);
        else:
            print "No more statistical output";
            output_str = "No more statistical output. \n";
            output_str = output_str + "<BR>";
            f.write(output_str);
        # endif
        
        return currentfigure;
    # end def
    
    
    #
    # Write out HTML write statistics header
    #   
    def open_header(self, f, currentfigure):
        # Open statistics header
        print " ";
        print "--------------------- ";
        print "-- Open Statistics -- ";
        print "--------------------- ";
        # HTML report output (top of section)
        output_str = " \n";
        output_str = output_str + "<hr /> \n";
        output_str = output_str + "<H3> \n"
        output_str = output_str + "6. <a id=\"open_stat\">Open Statistics</a> \n";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P> \n";
        output_str = output_str + "This section presents statistical information about the open() functions. \n";
        output_str = output_str + " Figure "+str(currentfigure)+" below is a histogram of the times for the open () function. \n";
        output_str = output_str + "<BR><BR> \n";
        f.write(output_str);
    # end def


    #
    # Create plot of close time() versus count
    #
    def open_plot(self, f, dirname, bincount, currentfigure):
        
        # Open() plot
        plt.hist(self.elapsed_time, bins=bincount);
        junk1 = "Open time Histogram - " + commify3(bincount) + " intervals";
        plt.title(junk1, fontsize='x-small');
        plt.xlabel("Time in seconds", fontsize='x-small');
        plt.ylabel("Count", fontsize='x-small');
        plt.xticks(rotation=35, fontsize='x-small');
        plt.yticks(fontsize='x-small');
        plot_name = dirname + "/open_time_histogram";
        plt.savefig(plot_name);
        plt.close();
            
        # HTML Output:
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"open_time_histogram.png\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure "+str(currentfigure)+" - Open Time histogram</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        f.write(output_str);
        junk1 = 0.0;
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
        print "Average (arthimetic mean or AM) = ",junk3," (secs per open function)";   # stdout
        output_str = "<UL> \n";
        output_str = output_str + "   <LI>Average (arthimetic mean or AM)  = ";
        output_str = output_str + str(junk3) + "  (secs per open function) \n";
        f.write(output_str);
        if (self.arthimetic_mean != 0.0):
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
        print "   AM Standard Deviation = ",junk1b," (secs per open function)  (",junk3," of AM)";   # stdout
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>AM Standard Deviation = \n";
        output_str = output_str + str(junk1b) + " (secs per open function)  (" + str(junk3) + " of AM) \n";
        f.write(output_str);
            
        junk1 = num_output(self.variance,5);              # Variance
        junk1b = commify3(junk1);
        print "   Variance = ",junk1b," (secs per open function)";   # stdout
        output_str = "      <LI>Variance = " + str(junk1b) + " (secs per open function) \n";
        f.write(output_str);
               
        junk2 = num_output(self.mad,5);                   # Mean Absolute Deviation
        junk2b = commify3(junk2);
        print "   Mean Absolute Deviation = ",junk2b," (secs per open function)";   # stdout
        output_str = "      <LI>Mean Absolute Deviation = ";
        output_str = output_str + str(junk2b) + " (secs per open function) \n";
        f.write(output_str);
         
        junk2 = num_output(self.mse,5);                    # Mean Squared Error (MSE)
        junk2b = commify3(junk2);
        print "   Mean Squared Error (MSE) = ",junk2b," (secs per open function)";   # stdout
        output_str = "      <LI>Mean Squared Error (MSE) = ";
        output_str = output_str + str(junk2b) + " (secs per open function) \n";
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
        junk2 = num_output(self.median,5);                    # Median
        junk3 = commify3( junk2 );
        print "Median = ",junk3," (secs per open function)";
        output_str = "   <LI>Median = " + junk3 + " (secs per open function)\n";
        f.write(output_str);
   
        if (self.median != 0.0):
            junk4 = (self.sigma_median/self.median)*100.0;
            junk1 = num_output(self.sigma_median,5);           # Standard Deviation around Median
            junk1b = commify3(junk1);
            junk2 = "%.2f" % junk4;
            junk2b = commify3(junk2);
            junk3 = junk2b + "%";
        else:
            junk4 = 0.0;
            junk3 = 0.0;
        # endif
        print "   Median Standard Deviation = ",junk1b," (secs per open function)  (",junk3," of Median)";
        output_str = "   <UL> \n";
        output_str = output_str + "      <LI>Median Standard Deviation = ";
        output_str = output_str + str(junk1b) + " (secs per open function)  (" + str(junk3) + " of Median) \n";
        f.write(output_str);
        
        junk1 = num_output(self.median_variance,5);             # Median Variance
        junk1b = commify3(junk1);
        print "   Variance time using Median = ",junk1b," (secs per open function)";
        output_str = "      <LI>Variance time using Median = ";
        output_str = output_str + str(junk1b) + " (secs per open function) \n";
        f.write(output_str);
   
        junk2 = num_output(self.medianad,5);         # Median Absolute Deviation
        junk2b = commify3(junk2);
        print "   Median Absolute Deviation = ",junk2b," (secs per open function)";
        output_str = "      <LI>Median Absolute Deviation = ";
        output_str = output_str + str(junk2b) + " (secs per open function) \n";
        f.write(output_str);
        
        junk2 = num_output(self.mse_median,5);      # Median Squared Error (MSE)
        junk2b = commify3(junk2);
        print "   Median Squared Error (MSE) = ",junk2b," (secs per open function)";
        output_str = "      <LI>Median Squared Error (MSE) = ";
        output_str = output_str + str(junk2b) + " (secs per open function) \n";
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

        # Mode computation
        #   Location, spread, and skewness measures
        junk1 = len(Open_List);
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
            print "   Value for seconds per open function = ",junk2," Repeated ",junk3b," times  (",junk6," of total values)";
            output_str = "      <LI>Value for seconds per open function</strong> = ";
            output_str = output_str + str(junk2) + " Repeated " + str(junk3b) + " times  (";
            output_str = output_str + str(junk6) + " of total values) \n";
            f.write(output_str);
            
            v5 = junk2;
            v5_sigma = std_dev(self.elapsed_time, junk2);              # Standard Deviation around Mode
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
            # endif
            print "      Mode Standard Deviation = ",junk1b," (secs per open function)  (",junk3," of Median)";
            output_str = "      <UL> \n";
            output_str = output_str + "         <LI>Mode Standard Deviation = ";
            output_str = output_str + str(junk1b) + " (secs per open function)  (" + str(junk3) + " of Median) \n";
            f.write(output_str);
            
            Mode_v1 = v5_sigma*v5_sigma;                             # Mode Variance
            junk1 = num_output(Mode_v1,5);
            junk1b = commify3(junk1);
            print "      Variance using Mode = ",junk1b," (secs per open function)";
            output_str = "         <LI>Variance using Mode = "
            output_str =output_str + str(junk1b) + " (secs per open function) \n";
            f.write(output_str);
            
            Mode_v2 = my_abs_deviation(Open_List,v5);               # Mode Absolute Deviation
            junk2 = num_output(Mode_v2,5);
            junk2b = commify3(junk2);
            print "      Mode Absolute Deviation = ",junk2b," (secs per open function)";
            output_str = "         <LI>Mode Absolute Deviation = ";
            output_str = output_str + str(junk2b) + " (secs per open function) \n";
            
            Mode_v3 = (Mode_v1*Mode_v1)/float(len(Open_List));      # Mode Squared Error (MSE)
            junk2 = num_output(Mode_v2,5);
            junk2b = commify3(junk2);
            print "      Mode Squared Error (MSE) = ",junk2b," (secs per open function)";
            output_str = "         <LI>Mode Squared Error (MSE) = ";
            output_str = output_str + str(junk2b) + " (secs per open funtion) \n";
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
        
        # Shape of Curve (skewness, Kurosis)
        print " ";
        print " ";
        print "The following statistics are for the 'shape' of the distribution of the open() ";
        print "function times for all open() calls.";
        # HTML
        output_str = "<P> \n";
        f.write(output_str);
        output_str = "The following statistics are for the 'shape' of the distribution of \n";
        output_str = output_str + "the open() function time for all open() calls. \n <BR><BR> \n";
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
        print "   skewness or shape of the curve of the distribution of the open() times.";
        iloop = 0;
        output_str2 = "   ";
        for item in DD_local:
            iloop = iloop + 1;
            if (iloop == 1):
                output_str2 = output_str2 + item + " (" + str(D_local[item]) + ") ";
            else:
                output_str2 = output_str2 + " <  " + item + " (" + str(D_local[item]) + ") ";
            # end if
            if (iloop == 3):
                final_loop = item;
            # end if
        # end for
        output_str2 = output_str2 + " \n";
        print " ";
        print output_str2;
        # HTML:
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <LI>The following is the ascending order and value of the mean, median, and \n";
        output_str = output_str + "mode statistics. The order of these statistics can be important for the \n";
        output_str = output_str + "skewness or shape of the curve of the distribution of the open() times. \n";
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

        # Kurtosis
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
    # Fischer-Pearson skewness factors
    #
    def fisher_pearson(self,f):

        # Fisher-Pearson Generalized moment (skewness measure) - g1
        print " ";
        output_str = "<BR> \n";
        if (self.skewness_mean > 0.0):
            print "   Fisher-Pearson coefficient of skewness (g1) relative to mean = ",self.skewness_mean,"  (skewed right)";
            print "      This means the peak is shifted left and the tail extends to the right";
        else:
            print "   Fisher-Pearson coefficient of skewness (g1) relative to mean = ",self.skewness_mean,"  (skewed left)";
            print "      This means the peak skewed to the right and the tail extends to the left";
        # end if
        # HTML output:
        output_str = "   <LI>Fisher-Pearson coefficient of skewness (g1) relative to mean = " + str(self.skewness_mean);
        if (self.skewness_mean > 0.0):
            output_str = output_str + "  (skewed right) with the peak to the left and tail extending to the right \n";
        else:
            output_str = output_str + "  (skewed lerft) with the peak to the right and tail extending to the left \n";
        # end if
        f.write(output_str);
   
        # Adjusted Fisher-Pearson standardized moment coefficient - G1
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
            output_str = output_str + " (skewed right). Magnitude of G1 also determines how far \n";
            output_str = output_str + "it is from the normal distribution. Values that are larger than zero \n";
            output_str = output_str + "indicate a skewed sample \n";
        else:
            output_str = output_str + " (skewed left). Magnitude of G1 also determines how far \n";
            output_str = output_str + "it is from the normal distribution. Values that are larger than zero \n";
            output_str = output_str + "indicate a skewed sample \n";
        # end if
        f.write(output_str);
   
        # SK2 (Pearson 2 skewness coefficient)
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
            output_str = output_str + "  (skewed right) with the peak to the left and tail extending to the right \n";
        else:
            output_str = output_str + "  (skewed lerft) with the peak to the right and tail extending to the left \n";
        # end if
        f.write(output_str);
    # end def

    
    #
    # Skewness summary
    #
    def skewness_summary(self, f, final_loop):

        # skewness summary:
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
        
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        # Order of mean, median, mode:
        if (final_loop == 'mode'):
            string1 = "left";
            string2 = "mean < median < mode";
            string3 = "right";
            string4 = "negative";
            string5 = "_longer_";
        elif (final_loop == "mean"):
            string1 = "right";
            string2 = "mode < median < mean";
            string3 = "right";
            string4 = "positive";
            string5 = "_shorter_";
        # end if
        print "      Based on the order of the main statistics, best guess is the shape is skewed ",string1,".";
        print "      In general this usually means:  ",string2,"  but not necessarily ";
        print "      every time. Skewed ",string1," means that the peak is shifted to the ",string3," with";
        print "      a long tail to the ",string1,". It can also mean that the skewness value is ",string4,".";
        print "      In the case of the open() times this means there are more ",string5," open";
        print "      times relative to the average and median.";
        # HTML
        output_str = "      <LI>Based on the order of the main statistics, best guess is the shape \n";
        output_str = output_str + "is <strong>skewed "+string1+"</strong>. In general this usually means:  \n";
        output_str = output_str + string2+"  but not necessarily every time. Skewed "+string1+" \n";
        output_str = output_str + "means that the peak is shifted to the "+string3+" with a long tail to \n";
        output_str = output_str + "the "+string1+". It can also mean that the skewness value is "+string4+". \n"
        output_str = output_str + "In the case of the open() times this means there are more "+string5+" open \n";
        output_str = output_str + "times relative to the average and median. \n";
        f.write(output_str);
        
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str); 
        
        # Fisher-Pearson Generalized moment (skewness measure) - g1
        print " ";
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        if (self.skewness_mean > 0.0):
            string1 = "positive";
            string2 = "right";
            string3 = "left";
            string4 = "_shorter_";
        else:
            string1 = "negative";
            string2 = "left";
            string3 = "right";
            string4 = "_longer_";
        # end if
        print "      The Fisher-Pearson coefficient of skewness (g1) is ",string1," so the open() time ";
        print "      distribution is skewed ",string2,". This means the peak is shifted ",string3," and the tail ";
        print "      extends to the ",string2,". In the case of the open() function times, this means there ";
        print "      are more ",string4," opens relative to the average and median.";
        # HTML
        output_str = "   <LI>The Fisher-Pearson coefficient of skewness (g1) is "+string1+" so the open() time \n";
        output_str = output_str + "distibution is <strong>skewed to the "+string2+"</strong> with the peak to \n";
        output_str = output_str + "the "+string3+" and tail extending to the "+string2+". In the case of the open() \n";
        output_str = output_str + "function times, this means there are more "+string4+" opens relative \n";
        output_str = output_str + "to the average and median. \n";
        f.write(output_str);
        
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        # Adjusted Fisher-Pearson standardized moment coefficient - G1
        print " ";
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        if (self.FP_coeff > 0.0):
            string1 = "positive";
            string2 = "right";
            string3 = "left";
            string4 = "_shorter_"; 
        else:
            string1 = "negative";
            string2 = "left";
            string3 = "right";
            string4 = "_longer_";
        # end if
        print "      Since the adjusted Fisher-Pearon Standardized Moment Coefficient (G1) is ";
        print "      ",string1," the distribution appears to be skewed ",string2,". That is, the peak is";
        print "      shifted to the ",string3," with a tail extending to the ",string2,". The magnitude of G1";
        print "      also determines how far it is from the normal distribution. G1 values that are";
        print "      larger than zero indicate a skewed distribution relative to the normal distribution.";
        print "      One can think of a distribution with a large value of G1 being 'more skewed' than ";
        print "      a distribution with a smaller value. For the case of the distribution of open()";
        print "      function times, this generally means that there are more ",string4," open()";
        print "      than longer open.";
        # HTML:
        output_str = "   <LI>Since the adjusted Fisher-Pearon Standardized Moment Coefficient (G1) is \n";
        output_str = output_str + string1+" the distribution appears to be <strong>skewed "+string2+"</strong>. \n";
        output_str = output_str + "That is, the peak is shifted to the "+string3+" with a tail extending to the \n";
        output_str = output_str + string2+". The magnitude of G1 also determines how far it is from the \n";
        output_str = output_str + "normal distribution. G1 values that are larger than zero indicate a \n";
        output_str = output_str + "skewed distribution relative to the normal distribution. One can think \n";
        output_str = output_str + "of a distribution with a large value of G1 being 'more skewed' than a \n";
        output_str = output_str + "distribution with a smaller value. For the case of the distribution of \n";
        output_str = output_str + "open function times, this generally means that there are more "+string4+" \n";
        output_str = output_str + "opens than longer opens. \n";
        f.write(output_str);
        
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);
        
        
        # SK2 (Pearson 2 skewness coefficient)
        print " ";
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        if (self.sk2 > 0.0):
            string1 = "positive";
            string2 = "right";
            string3 = "left";
            string4 = "_shorter_"
        else:
            string1 = "negative";
            string2 = "left";
            string3 = "right";
            string4 = "_longer_";
        # end if
        print "      The Pearson 2 skewness coefficient (SK2) is ",string1," so that means the distribution is";
        print "      skewed to the ",string2,". This means the the peak is shifted to the ",string3," which means";
        print "      that there are more ",string4," open times than longer times. It also means there is ";
        print "      a tail that extends to the ",string2,". Notice that the value of SK2 must be between ";
        print "      -3 and 3 with these limits being extreme values.";
        # HTML
        output_str = "   <LI>The Pearson 2 skewness coefficient (SK2) is "+string1+" so that means the \n";
        output_str = output_str + "distribution is <strong>skewed to the "+string2+"</strong>. This means \n";
        output_str = output_str + "the the peak is shifted to the "+string3+" which means that there are \n";
        output_str = output_str + "more "+string4+" open than than longer times. It also means there is \n";
        output_str = output_str + "a tail that extends to the "+string2+". Notice that the value of SK2 must \n";
        output_str = output_str + "be between -3 and 3 with these limits being extreme values."

        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        output_str = "</UL> \n";
        f.write(output_str);

        # Kurtosis
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
   
        # Final comment
        print " ";
        print "      If you get conflicting indicators on the skewness (right or left), then";
        print "      it is impossible to say what the shape of the curve looks like. This means";
        print "      that it is difficult to say if the curve of the write() function payload";
        print "      size distribution is non-symmetrical and/or bends to one direction. It may. ";
        print "      also have several local minima, and it may have long or short tails.";
        # HTML
        output_str = "<UL> \n";
        f.write(output_str);
        output_str = "   <UL> \n";
        f.write(output_str);
        output_str = "   <LI>If you get conflicting indicators on the skewness (right or left), then \n";
        output_str = output_str + "it is impossible to say what the shape of the curve looks like. This means \n";
        output_str = output_str + "that it is difficult to say if the curve of the write() function payload \n";
        output_str = output_str + "size distribution is non-symmetrical and/or bends to one direction, \n"
        output_str = output_str + "also have several local minima, and it may have long or short tails. \n";
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
    # Other stats
    #    Slowest open (and line in file where it occurs)
    #    Fastest open (and line in file where is occurs)
    #    Range of open() times
    #
    def other_stats(self,f):

        # Other Stats:
        print "Other statistics:"
        print " ";
        # HTML:
        output_str = "<BR> \n";
        f.write(output_str);
        output_str = "<P> \n";
        f.write(output_str);
        output_str = "Other statistics: \n";
        f.write(output_str);
   
        junk1 = self.OpenMax["MaxTime"];
        junk1a = "%.4f" % junk1;
        junk1b = commify3(junk1a);
        print "Maximum Time for open function (secs) = ",junk1b;
        output_str = "   <LI>Maximum Time for open function (secs) = " + junk1b + " \n";
        f.write(output_str);
        junk1 = self.OpenMax["line"];
        junk1b = commify3(junk1);
        print "   Line location in file: ",junk1b;
        output_str = "   <UL> \n";
        f.write(output_str);
        output_str = "      <LI>Line location in file: " + junk1b + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        junk1 = self.OpenMin["MinTime"];
        junk1a = "%.4f" % junk1;
        junk1b = commify3(junk1a);
        print "Minimum Time for open function (secs) = ",junk1b;
        output_str = "      <LI>Minimum Time for open function (secs) = " + junk1b + " \n";
        f.write(output_str);
        junk1 = self.OpenMin["line"];
        junk1b = commify3(junk1);
        print "   Line location in file: ",junk1b;
        output_str = "   <UL> \n";
        f.write(output_str);
        output_str = "      <LI>Line location in file: " + junk1b + " \n";
        f.write(output_str);
        output_str = "   </UL> \n";
        f.write(output_str);
        junk1 = float(self.OpenMax["MaxTime"]) - float(self.OpenMin["MinTime"]);
        junk1a = "%.4f" % junk1;
        junk1b = commify3(junk1a);
        print "Range of Open data = ",junk1b," secs"
        output_str = "   <LI>Range of Open data = " + junk1b + " secs \n";
        f.write(output_str);
        print " ";
   
        # Finish html
        output_str = "</UL> \n";
        f.write(output_str);
        output_str = "</P> \n \n";
        f.write(output_str);
    # end def




# end class open

