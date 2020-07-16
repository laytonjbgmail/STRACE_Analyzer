#!/usr/bin/python
#
# Copyright 2008-2014 Jeffrey B. Layton
#



#
#
# Results() Class definition
#
#
class commandclass:

# This class is simply a storage container for "command" data from the strace
# analysis. Instantiated Object stores data as self.commanddata. There is some predefined
# data (dictionaries) for this class.
#
    
    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.commanddata = {};
        self.commanddata["Command_List"] = [];
        self.commanddata["CmdCounter"] = {};
    # end if


# end command class


