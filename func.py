

import sys
try:
   from math import floor    # Needed for floor function
except ImportError:
   print "Cannot import math module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   from math import sqrt;    # Needed for sqrt function
except ImportError:
   print "Cannot import math module for sqrt - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   from math import log;     # Needed for log function
except ImportError:
   print "Cannot import math module for log - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   from math import exp;    # Needed for exp function
except ImportError:
   print "Cannot import math module for exp - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   from math import fabs;    # Needed for abs function
except ImportError:
   print "Cannot import math module for fabs - this is needed for this application.";
   print "Exiting..."
   sys.exit();


try:
   import decimal;
except ImportError:
   print "Cannot import decimal module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import re                 # Needed for regex
except ImportError:
   print "Cannot import re module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   from collections import defaultdict
except:
   print "cannot import defaultdict";
   print "exiting";
   sys.exit();



# =========
# =========
# Functions
# =========
# =========


#
# Insert data into IOPS array
#
# Note: "value" is the IO function name (e.g. READ, WRITE, LSEEK, etc.)
#
def IOPS_insert(IOPS_info,IOPS,value,sec,BeginTime,unit,debug,STRACE_LOG):
   # Insert data into IOPS array
   
   # local temporary dictionary
   temp_dict = {};
   
   # Step 1 - find "unit" in IOPS_info if unit > 0)
   #    if unit = -1 then just make pointr negative and put
   #    IOPS function in data structure
   if (unit > -1):
      # Examine IOPS_info to look for "unit"
      local_pointer = -2;
      for item in IOPS_info:
         if (int(item["unit"]) == int(unit) ):
            local_pointer = item["pointer"];
            break;
         # end if
      # end for loop
      if (local_pointer > -2):
         temp = int(floor(float(sec) - float(BeginTime)) + 1);
         temp_dict = {};
         temp_dict["pointer"] = local_pointer;
         temp_dict["type"] = value;
         temp_dict["time"] = temp;
         IOPS.append(temp_dict);
         if (debug > 0):
            junk1 = "      IOPS time = " + str(temp) + " \n";
            STRACE_LOG.write(junk1);
         # end if
      else:
         print "Interesting problem in IOPS_insert";
         print "   local_pointer from IOPS_info data structure is -2";
         print "   value = ",value," unit = ",unit;
         for item in IOPS_info:
            print "      item:",item;
         #end if
      #end if
   elif (unit == -1):
      temp = int(floor(float(sec) - float(BeginTime)) + 1);
      temp_dict = {};
      temp_dict["pointer"] = -1;
      temp_dict["type"] = value;
      temp_dict["time"] = temp;
      IOPS.append(temp_dict);
      if (debug > 0):
         junk1 = "      IOPS time = " + str(temp) + " \n";
         STRACE_LOG.write(junk1);
      # end if
   else:
      STRACE_LOG.write("IOPS_insert: Negative unit \n");
      STRACE_LOG.write("   unit is negative \n");
      junk1 = "   value = "+value+" unit = "+str(unit) + "\n";
      STRACE_LOG.write(junk1);
   # end if
#end def





#
# Insert data into Offset array
#
#
def Offset_insert(Offset_info,Offset,sec,BeginTime,bytes,LineNum,unit):

   # local variables
   Offset_Dict = {};

   j = -1;   # pointer into Offset_info
   local_pointer = -1;
   for item in Offset_info:
      j = j + 1;
      if (item["unit"] == unit):
         local_pointer = item["pointer"];
         junk1 = item["offset_cur"];
         break;
      # end if
   # end for loop
   
   # Step 2 - If local_pointer is positive then add data to Offset data structure
   if (local_pointer > -2):
      # Update current file offset in Offset_info array
      Offset_info[j]["offset_cur"] = int(junk1) + int(bytes);
      
      # Update Offset information (used for pattern observation)
      #    Local dictionary
      Offset_Dict = {};
      junk3 = float(sec) - float(BeginTime);
      Offset_Dict["pointer"] = local_pointer;
      Offset_Dict["time"] = junk3;
      Offset_Dict["offset"] = int(junk1) + int(bytes);
      # Append local dictionary to list of dictionaries
      Offset.append(Offset_Dict);
   else:
      print "      Offset_insert:";
      print "      Problem: Cannot find unit in Offset_info array";
      print "         unit:",unit;
      print "         Linenum:",LineNum;
      print "      Suggest killing job and checking strace file";
   # End if
# end def



#
# Routine to add commas to a float string
#
def commify3(amount):
    amount = str(amount)
    amount = amount[::-1]
    amount = re.sub(r"(\d\d\d)(?=\d)(?!\d*\.)", r"\1,", amount)
    return amount[::-1]
# end def commify3(amount):



def FileSizeStr(value):
   junk = int(value);
   
   #printf("FileSizeStr function: junk = %s \n", $junk);
   if (junk < 1000000):
      junk_str = "%3d" % (int(junk)/1000);
      junk_str = junk_str + "KB";
   elif (junk >= 1000000 and junk < 1000000000 ):
      junk_str = "%3d" % (int(junk)/1000000);
      junk_str = junk_str + "MB";
   elif (junk >= 1000000000  and junk < 1000000000000 ):
      junk_str = "%3d" % (int(junk)/1000000000);
      junk_str = junk_str + "GB";
   elif (junk >= 1000000000000):
      junk_str = "%3d" % (int(junk)/1000000000000);
      junk_str = junk_str + "TB";
   else:
      junk_str = "Are you sure that is correct? That is a huge file size";
   # end of if ladder
   return junk_str;
# end of def FileSizeStr(value);



#
# Following routine counts duplicates and returns it in a list of tuples
# taken from: http://bigbadcode.com/2007/04/04/count-the-duplicates-in-a-python-list/
#
def count_dups(l):
   tally = defaultdict(int)
   for x in l:
      tally[x] += 1
   # end for loop
   return tally.items()
# end def



#
# Arthimetic average (mean)
#
def arithmean(local_list):
   return sum(local_list) / float(len(local_list));
# end def



# 
# Standard deviation of data around a mean (can be arthimetic, geometric or harmonic)
#  (may need to add some error checking to sqrt argument)
#
def std_dev(local_list, mean_num):
   sum2 = 0.0;
   junk2 = float(len(local_list));
   junk3 = float(mean_num);
   for item in local_list:
      junk1 = float(item)-junk3;
      sum2 = sum2 + (junk1 * junk1);
   # end for
   
   junk4 = float(sum2)/junk2;
   junk5 = sqrt(junk4);
   return junk5
# end def



def geomean2(nums):
    return (reduce(lambda x, y: x*y, nums))**(1.0/len(nums))
# end def



#
# Geometric Mean
# (from: http://bytes.com/topic/python/answers/727876-geometrical-mean)
#
def geomean(numbers):
    product1 = 1.0
    for n in numbers:
       product1 *= n
    return product1 ** (1.0/float(len(numbers)))
# end def



#
# Geometric mean
#  (from: http://www.nmr.mgh.harvard.edu/Neural_Systems_Group/gary/python/stats.py)
#
def lgeometricmean (inlist):
   """
Calculates the geometric mean of the values in the passed list.
That is:  n-th root of (x1 * x2 * ... * xn).  Assumes a '1D' list.

Usage:   lgeometricmean(inlist)
   """
   mult1 = 1.0
   one_over_n = 1.0/float(len(inlist));
   for item in inlist:
      mult1 = mult1 * pow(item,one_over_n);
   # end if
   return mult1
# end def



#
# Harmonic mean
#  (from: http://www.nmr.mgh.harvard.edu/Neural_Systems_Group/gary/python/stats.py)
#
def lharmonicmean (inlist):
   """
Calculates the harmonic mean of the values in the passed list.
That is:  n / (1/x1 + 1/x2 + ... + 1/xn).  Assumes a '1D' list.

Usage:   lharmonicmean(inlist)
   """
   sum1 = 0
   for item in inlist:
      sum1 = sum1 + 1.0/item
   return len(inlist) / sum1
# end def



#
# Convert floating point number to decimal with no loss of information
#   http://stackoverflow.com/questions/2663612/nicely-representing-a-floating-point-number-in-python
#
def float_to_decimal(f):
    # http://docs.python.org/library/decimal.html#decimal-faq
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = decimal.Decimal(n), decimal.Decimal(d)
    ctx = decimal.Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[decimal.Inexact]:
        ctx.flags[decimal.Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result 
# end def



#
# Convert float to string with specified significant figures
#    http://stackoverflow.com/questions/2663612/nicely-representing-a-floating-point-number-in-python
#
def num_output(number, sigfig):
    # http://stackoverflow.com/questions/2663612/nicely-representing-a-floating-point-number-in-python/2663623#2663623
    assert(sigfig>0)
    try:
        d=decimal.Decimal(number)
    except TypeError:
        d=float_to_decimal(float(number))
    sign,digits,exponent=d.as_tuple()
    if len(digits) < sigfig:
        digits = list(digits)
        digits.extend([0] * (sigfig - len(digits)))    
    shift=d.adjusted()
    result=int(''.join(map(str,digits[:sigfig])))
    # Round the result
    if len(digits)>sigfig and digits[sigfig]>=5: result+=1
    result=list(str(result))
    # Rounding can change the length of result
    # If so, adjust shift
    shift+=len(result)-sigfig
    # reset len of result to sigfig
    result=result[:sigfig]
    if shift >= sigfig-1:
        # Tack more zeros on the end
        result+=['0']*(shift-sigfig+1)
    elif 0<=shift:
        # Place the decimal point in between digits
        result.insert(shift+1,'.')
    else:
        # Tack zeros on the front
        assert(shift<0)
        result=['0.']+['0']*(-shift-1)+result
    if sign:
        result.insert(0,'-')
    return ''.join(result)
# end def



#
# Find the median in a list
#
def my_median(local_list):
   # Find median value
   junk2 = len(local_list);
   local_list.sort();
   junk2 = len(local_list);     # length of array
   junk1 = ( junk2%2 and 'odd' or 'even');
   if (junk1 == "odd"):
      # number is odd
      middle = junk2 / 2;
      My_Median2 = local_list[middle];
   else:
      # number is even
      middle = (junk2 / 2) - 1;
      My_Median2 = ( local_list[middle] + local_list[middle+1]) / 2.0;
   # end if statement
   return My_Median2
# end def


#
# Compute geomteric standard deviation
# 
def my_geo_stddev(local_list, geomean):
   #
   junk5 = len(local_list);
   junk1 = 0.0;
   for item in local_list:
      junk2 = log( (item/geomean) )**2.0;
      junk1 = junk1 + junk2;
   # end for
   junk3 = sqrt((junk1/junk5));
   junk4 = exp(junk3);
   return junk4;
# end def


#
# Compute mode:
#   http://code.activestate.com/recipes/409413-a-python-based-descriptive-statistical-analysis-to/
#
def My_Mode(local_list):
   """Determine the most repeated value(s) in the data set."""

   # Initialize a dictionary to store frequency data.
   frequency = {}

   # Build dictionary: key - data set values; item - data frequency.
   for x in local_list:
      if (x in frequency):
         frequency[x] += 1
      else:
         frequency[x] = 1

   # Create a new list containing the values of the frequency dict.  Convert
   # the list, which may have duplicate elements, into a set.  This will
   # remove duplicate elements.  Convert the set back into a sorted list
   # (in descending order).  The first element of the new list now contains
   # the frequency of the most repeated values(s) in the data set.
   # mode = sorted(list(set(frequency.values())), reverse=True)[0]
   # Or use the builtin - max(), which returns the largest item of a
   # non-empty sequence.
   mode = max(frequency.values())

   # If the value of mode is 1, there is no mode for the given data set.
   if (mode == 1):
      Mymode = []
      return Mymode;
   # end if

   # Step through the frequency dictionary, looking for values equaling
   # the current value of mode.  If found, append the value and its
   # associated key to the self.mode list.
   Mymode = [(x, mode) for x in frequency if (mode == frequency[x])]
   return Mymode;
# end def



#
# Compute absolute standard deviation
# 
def my_abs_deviation(local_list, cpoint):
   #
   junk5 = len(local_list);
   junk2 = 0.0;
   for item in local_list:
      junk1 = float((item - cpoint));
      junk2 = junk2 + fabs(junk1);
   # end for
   junk3 = junk2/junk5;
   return junk3;
# end def



#
# Compute SK2 - Pearson 2 skewness coefficient
#
def my_sk2(mean, median, sigma):
   #
   SK2 = 3.0*((mean-median)/sigma);
   return SK2;
# end def



#
# Compute skewness
#   (Fisher-Pearson coefficient of skewness)
# 
def my_skewness(local_list, cpoint):
   #
   junk4 = len(local_list);
   junk2 = 0.0;                # denominator
   junk3 = 0.0;                # numerator
   for item in local_list:
      junk1 = float((item - cpoint));
      junk2 = junk2 + (junk1*junk1);
      junk3 = junk3 + (junk1*junk1*junk1);
   # end for
   numerator_local = junk3/junk4; 
   denominator_local = (junk2/junk4)**(3.0/2.0)
   junk7 = numerator_local / denominator_local
   return junk7;
# end def



#
# Compute kurtosis
#   "Excess Kurtosis" http://en.wikipedia.org/wiki/Kurtosis
# 
def my_kurtosis(local_list, cpoint):
   #
   junk4 = len(local_list);
   junk2 = 0.0;                # denominator
   junk3 = 0.0;                # numerator
   for item in local_list:
      junk1 = float((item - cpoint));
      junk3 = junk3 + (junk1*junk1*junk1*junk1);
      junk2 = junk2 + (junk1*junk1);
   # end for
   numerator_local = junk3/junk4; 
   denominator_local = (junk2/junk4)*(junk2/junk4);
   junk7 = (numerator_local / denominator_local) - 3.0;
   return junk7;
# end def



#
# Compute Fisher-Pearson standardized moment coefficient that has been
#   adjusted for sample size (G1). Same forumla used in Excel
# 
def my_fp_coeff(local_list, xbar):
   #
   N = float(len(local_list));
   junk3 = 0.0;   # third moment sum
   junk2 = 0.0;   # second moment sum
   for item in local_list:
      junk1 = float((item - xbar));
      junk2 = junk2 + junk1*junk1;
      junk3 = junk3 + junk1*junk1*junk1;
   # end for
   m2 = junk2/N;   # second moment
   m3 = junk3/N;   # third moment
   junk4 = (3.0/2.0);
   g1 = m3/(m2**junk4);
   junk7 = N*(N-1.0);
   junk8 = N-2.0;
   correction = sqrt(junk7)/junk8;
   G1 = correction*g1
   return G1;
# end def





#
# Return a list of keys in a dictionary corresponding to sorted
#  values (from smallest to largest)
#
# Example:
#
#    D['mean'] = 6131.2;
#    D['median'] = 100.0;
#    D['mode'] = 35345.0;
#    DD = sort_by_value(D);
#    print DD
#       DD =  ['median', 'mean', 'mode']
#
# taken from: http://code.activestate.com/recipes/52306-to-sort-a-dictionary/
#  (comment by Daniel Schult
#
def sort_by_value(d):
    """ Returns the keys of dictionary d sorted by their values """
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]




#
# Borrowed from http://my.safaribooksonline.com/book/programming/python/0596001673/files/pythoncook-chp-4-sect-16
#
import os, sys
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
# end def



def is_number(s):
   try:
      a=float(s);
      return a;
   except ValueError:
      return 0.0;
# end def




