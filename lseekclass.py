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
# lseek() Class definition (and like lseek() functions)
#
#
class lseekclass:

# Instantiated Object stores data as self.writedata. This is a list of lists (2D list).
# Each row of the list consists of a record. Each record consists of:
#
#   LineNum        (line number of strace output file)
#   sec            (seconds since epoch when function was called)
#   elapsed_time   (elapsed time for open)
#   filename       (filename for file being opened)
#   unit           (file descriptor associated with file)
#   whence         (whence for lseek)
#   offset         (offset argument from lseek)
#   off_t_result   (final file offset)

    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.lseekdata = [];
    # end if
    
    #
    # This function appenda data to self.lseekdata
    #
    def storelseek(self,data):
        self.lseekdata.append(data);
    # end if
    
    #
    # Return the list to caller
    #
    def getlseek(self):
        return self.lseekdata;
    # end if
    


    #
    # Write out lseek statistics
    #
    def lseek_statistics(self, f, CmdCounter, LSEEK, VFLAGS, BeginTime, EndTime):

        if (CmdCounter[LSEEK] > 0):
            
            #
            # Write out header
            #
            print " ";
            print "------------------------------------ ";
            print "-- lseek unit activity Statistics -- ";
            print "------------------------------------ ";
            print " ";
            # HTML report output (top of section)
            output_str = " \n";
            output_str = output_str + "<hr /> \n";
            output_str = output_str + "<H3> \n"
            output_str = output_str + "7. <a id=\"lseek_stat\">Lseek Statistics</a> \n";
            output_str = output_str + "</H3> \n";
            output_str = output_str + " \n";
            output_str = output_str + "<P> \n";
            output_str = output_str + "This section presents statistical information about the lseek() functions. \n";
            output_str = output_str + "<BR><BR> \n";
            output_str = output_str + "</P> \n";
            f.write(output_str);
      
            if (VFLAGS > 2):
                # Create list of dictionaries with filenames and lseek counts
                
                # List of all filenames assocaited with LSEEK
                temp_list = [];
                for item in self.lseekdata:
                    temp_list.append(item["filename"]);
                # end for
                newlist = list(set(temp_list));     # http://mattdickenson.com/2011/12/31/find-unique-values-in-list-python/
                
                # Initialize dictionary (include ".")
                file_table = [];
                local_dist = {};
                local_dist["filename"] = ".";
                local_dist["count"] = 0;
                file_table.append(local_dist);

                # loop over list of some type 
                for item in newlist:
                    local_dist = {};
                    local_dist["filename"] = item;
                    local_dist["count"] = 0;
                    file_table.append(local_dist);
                # end if
                
                for item in self.lseekdata:
                    for item2 in file_table:
                        if (item2["filename"] == item["filename"].lower() ):
                            item2["count"] = item2["count"] + 1;
                            break;
                        # end if
                    # end for
                # end for
                
                print "File                                                                                      Number of lseeks";
                print "==========================================================================================================";
      
                # HTML table header:
                output_str = "<P> \n";
                output_str = output_str + "Table 4 below contains information on the lseek function usage in\n";
                output_str = output_str + "various input and output files used by the application. \n";
                output_str = output_str + "<BR><BR><center><strong>Table 4 - Lseek Function calls </strong><BR><BR> \n";   
                output_str = output_str + "<table border =" + "\"1\" " + "> \n";
                output_str = output_str + "   <tr> \n";
                output_str = output_str + "      <th align = left><font size=\"-2\">File</font></th> \n";
                output_str = output_str + "      <th align=right><font size=\"-2\">Number of Lseeks</font></th> \n";
                output_str = output_str + "   </tr> \n";
                f.write(output_str);
                
                itotal = 0;
                for item in file_table:
                    junk1 = item["filename"];
                    junk1_str = junk1.ljust(89," ");
                    junk2 = str(item["count"]);
                    junk2a = commify3(junk2);
                    itotal = itotal + int(item["count"]);
                    junk2_str = junk2a.rjust(16," ");
                    print junk1_str,junk2_str;
                    # HTML
                    output_str = "   <tr> \n";
                    output_str = output_str + "      <td align=left><font size=\"-2\">" + junk1 + "</font></td> \n";
                    output_str = output_str + "      <td align=right><font size=\"-2\">" + commify3(junk2) + "</font></td> \n";
                    output_str = output_str + "   </tr> \n";
                    f.write(output_str);
                # end for item
                print " ";
                print " ";
      
                # HTML - close table
                output_str = "</table></center><BR><BR> \n";
                output_str = output_str + "</P> \n";
                output_str = output_str + " \n";
                f.write(output_str);
            else:
                #
                # Compute some overall statistics on lseeks across all files
                #
                junk1 = int(CmdCounter[LSEEK]);
                junk1a = commify3(junk1);
                junk2 = float(CmdCounter[LSEEK])/(float(EndTime) - float(BeginTime));
                junk2a = "%.2f" % junk2;
                output_str = "<P> \n";
                output_str = output_str + "Simple lseek() statistics across all files: \n \n";
                output_str = output_str + "<UL> \n";
                output_str = output_str + "   <LI>Total number of lseeks: " + junk1a + " \n";
                output_str = output_str + "   <LI>Avg lseeks per second: " + commify3(junk2a) + " \n";
                output_str = output_str + "</UL> \n";
                output_str = output_str + "</P> \n \n ";
                f.write(output_str);
         
                junk3 = "Total lseeks across all files: " + junk1a;
                print junk3;
                junk3 = "Average lseeks across all files: " + commify3(junk2a);
                print junk3;
                print " ";
                print " ";
            # end if

        # end if (CmdCounter["lseek"] > 0):

    # end def


# end lseek class

