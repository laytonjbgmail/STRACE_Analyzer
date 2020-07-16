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
# Filepointer() Class definition
#
#
class Filepointerclass:

# Instantiated Object stores data as self.storefilepointer data. The data is a 2D list
# (list of lists). Later on, the data can be massaged to get all of the data for a
# particular file put into one data structure.
#
#
# Each record stored in object consists of:
#  Filepointer = [];           # File pointer for a specific file (list of dictionaries)
#                              #    Filepointer[iloop]["sec"] = sec
#                              #    Filepointer[iloop]["unit"] = file descriptor
#                              #    Filepointer[iloop]["filename"] = filename
#                              #    Filepointer[iloop]["pointer"] = pointer value
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
        self.filepointerdata = [];
    # end if
    
    
    #
    # This function appenda data to self.filepointerndata
    #    
    def storefilepointer(self,data):
        self.filepointerdata.append(data)
    # end if
    
    
    #
    # Return the list to caller
    #
    def getfilepointer(self):
        return self.filepointerdata;
    # end if
    
    
    
    
    #
    # File pointer plots to HTML
    #
    def filepointer_output(self, Open_obj, f, dirname, BeginTime, EndTime, currentfigure,
                           VFLAGS, matplotlib_var, numpy_var):
        
        #
        # Write out statistics output section header (stdout and HTML)
        #
        self.stats_header(f);
        
        # Get file open data (what files to track)
        localdata2 = Open_obj.getopen();    # Get file open data
        
        localdata3 = [];
        for item in localdata2:
           localdata3.append(item[2]);
        # end for
        
        # Need to de-dup localdata3
        seen = set();
        seen_add = seen.add
        localdata = [ x for x in localdata3 if not (x in seen or seen_add(x))];
        
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
        
        iloop = 0;
        for item in localdata:
            
            # parse file name to exclude system files
            junk = item.split("/");
            if (len(junk) > 1):
                comp = junk[1];
            else:
                comp = junk[0];
            # end if
            
            # Check if "item" falls into blacklist (first directory of path)
            system_file_flag = 1;
            if (comp not in file_blacklist):
                system_file_flag = 0;
            # end if
            
            if (system_file_flag == 0):   # Not a system file
                iloop = iloop + 1;
                
                file_search = item;    # what file to search for
                
                # Grab all pointer data from Filepointer_obj()
                pt_data = [element for element in self.filepointerdata if element["filename"] == file_search];
                
                # Process pt_data into x and y arrays
                xdata = [];
                ydata = [];
                #xdata.append(0.0);
                #ydata.append(0);
                iopen = 0;
                iclose = 0;
                iseek = 0;
                iwrite = 0;
                iread = 0;
                for data in pt_data:
                    junk = float((float(data["sec"])-float(BeginTime)));
                    xdata.append(junk);
                    ydata.append(int(data["pointer"]));
                    if (data["type"].lower() == "open"):
                        iopen = iopen + 1;
                    elif (data["type"].lower() == "close"):
                        iclose = iclose + 1;
                    elif (data["type"].lower() == "seek"):
                        iseek = iseek + 1;
                    elif (data["type"].lower() == "write"):
                        iwrite = iwrite + 1;
                    elif (data["type"].lower() == "read"):
                        iread = iread + 1;
                    # end if
                # end for
                #ydata.append(0.0);
                #junk = (float(float(EndTime)-float(BeginTime)));
                #xdata.append(junk);
                #print "   xdata = ",xdata;
                #print "   ydata = ",ydata;
                
                output_str = "<P> \n";
                output_str = output_str + "The data below is for file <strong>" + file_search;
                output_str = output_str + "</strong>. The following is a list of the number of IO \n";
                output_str = output_str + "functions used that affect the file pointer location. \n";
                output_str = output_str + "What is significant is the number of times a file is opened \n";
                output_str = output_str + "since that resets the file pointer to the beginning of the \n";
                output_str = output_str + "file (0). \n\n <UL> \n";
                output_str = output_str + "   <LI>Number of opens: " + commify3(iopen) + " \n";
                output_str = output_str + "   <LI>Number of closes: " + commify3(iclose) + " \n";
                output_str = output_str + "   <LI>Number of seeks: " + commify3(iseek) + " \n";
                output_str = output_str + "   <LI>Number of writes: " + commify3(iwrite) + " \n";
                output_str = output_str + "   <LI>Number of reads: " + commify3(iread) + " \n";
                output_str = output_str + "</UL> \n\n";
                f.write(output_str);
                
                
                if (VFLAGS >= 2):
                    title = file_search;    # name of input file
                    xaxis_title_1 = "Time (secs)";
                    yaxis_title_1 = "File pointer (bytes)";
                    output_file_name = "./HTML_REPORT/filepointer"+str(iloop)+".png";
                    #print "** output_file_name = ",output_file_name;
                    #print "   xdata: ",xdata;
                    #print "   ydata:" ,ydata;
                    Plot_1_1(xdata, ydata, title, xaxis_title_1, yaxis_title_1, output_file_name);
                    
                    # HTML:
                    currentfigure = currentfigure + 1;
                    output_str = "<P> \n";
                    output_str = output_str + "Figure " + str(currentfigure) + " below is a plot of \n";
                    output_str = output_str + "the file pointer in bytes versus application run time. \n";
                    output_str = output_str + "Note that application run time means that the time is \n";
                    output_str = output_str + "normalized to the application start time. So \n";
                    output_str = output_str + "when the application starts the time is zero. \n";
                    output_str = output_str + "<BR><BR> \n";
                    output_str = output_str + "<center> \n";
                    output_str = output_str + "<img src=\"filepointer"+str(iloop)+".png\"> \n";
                    output_str = output_str + "<BR><BR><strong>Figure " + str(currentfigure) + " File: ";
                    output_str = output_str + file_search;
                    output_str = output_str + " - Cummlative File pointer location in bytes versus \n";
                    output_str = output_str + "time (seconds)</strong></center><BR><BR> \n";
                    f.write(output_str);
                # end if
                output_str =  "</P> \n\n";
                f.write(output_str);
                
            # end if
            
        # end for
        return currentfigure;
    # end def
    
    
    #
    # Write out HTML write statistics header
    #
    def stats_header(self, f):
        
        
        # HTML report output (opt of section)
        output_str = " \n";
        output_str = output_str + "<hr /> \n";
        output_str = output_str + "<H3> \n"
        output_str = output_str + "13. <a id=\"file_pointer\">File pointer tracking plots</a> \n";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P> \n";
        output_str = output_str + "This section presents plots tracking the file pointer of non \n";
        output_str = output_str + "system files. The plots are of the file offset versus time. \n";
        output_str = output_str + "Examining the file pointer history should help in understanding \n";
        output_str = output_str + "if the data access patterns are sequential or random or some \n";
        output_str = output_str + "combination. It assumes that when a file is opened the file offset \n";
        output_str = output_str + "is set to zero. If the application continually opens and closes \n";
        output_str = output_str + "a file you will see data with a zero file offset. The plots \n";
        output_str = output_str + "contain the impact of read(), write(), and lseek() on the file \n";
        output_str = output_str + "offset. \n";
        output_str = output_str + "</P> \n \n";
        
        output_str = output_str + "<P> \n";
        output_str = output_str + "Also included are some basic statistics for the particular file \n";
        output_str = output_str + "such as the number of times the file is either opened or closed, \n";
        output_str = output_str + "and the number of IO functions that affect the file offset. \n";
        output_str = output_str + "</P> \n \n";
        f.write(output_str);
    # end def




   
# end class Filepointer

