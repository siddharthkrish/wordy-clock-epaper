#!/usr/bin/python
# -*- coding:utf-8 -*-

def timeInWords(h, m):
    nums = ["zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen",
            "twenty", "twenty one", "twenty two",
            "twenty three", "twenty four",
            "twenty five", "twenty six", "twenty seven",
            "twenty eight", "twenty nine"];

    if (m == 0):
        return(nums[h] + "\n o' clock");

    elif (m == 1):
        return("one minute past\n" + nums[h]);

    elif (m == 59):
        return("one minute to\n" + nums[(h % 12) + 1]);

    elif (m == 15):
        return("quarter past\n" + nums[h]);

    elif (m == 30):
        return("half past\n" + nums[h]);

    elif (m == 45):
        return("quarter to\n" + (nums[(h % 12) + 1]));

    elif (m <= 30):
        return(nums[m] + "\n minutes past\n" + nums[h]);

    elif (m > 30):
        return(nums[60 - m] + "\n minutes to\n" +  nums[(h % 12) + 1]);
