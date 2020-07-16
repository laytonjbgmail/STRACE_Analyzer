#!/usr/bin/python
#
# Copyright 2008-2014 Jeffrey B. Layton
#


#
#
# Results() Class definition
#
#
class resultsclass:

# This class is simply a storage container for "results" data from the strace
# analysis. Instantiated Object stores data as self.resultsdata. There is some predefined
# data (dictionaries) for this class.
#
    
    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.resultsdata = {};
        self.resultsdata["IOTimeSum"] = 0.0;
        self.resultsdata["IOTime_count"] = 0;
        self.resultsdata["NumLines"] = 0;
        self.resultsdata["IOTime_count"] = 0.0;
        self.resultsdata["IOPS_Total_Final"] = 0;
        self.resultsdata["IOPS_Read_Final"] = 0;
        self.resultsdata["IOPS_Write_Final"] = 0;

        self.resultsdata["IOPS_Write_peak"] = 0.0;
        self.resultsdata["IOPS_Write_peak_time"] = 0.0;
        self.resultsdata["IOPS_Read_peak"] = 0.0;
        self.resultsdata["IOPS_Read_peak_time"] = 0.0;
        self.resultsdata["IOPS_Total_peak"] = 0.0;
        self.resultsdata["IOPS_Total_peak_time"] = 0.0;

        self.resultsdata["BeginTime"] = -1.0;
        self.resultsdata["EndTime"] = -1.0;
        self.resultsdata["WriteSmall"] = 0;
        self.resultsdata["WriteLarge"] = 0;
        self.resultsdata["ReadSmall"] = 0;
        self.resultsdata["ReadLarge"] = 0;
    # end if
    
    


# end results class


