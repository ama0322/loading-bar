"""
Filename   : LoadingBar.py
Date       : December 20, 2018
Description: This file provides the two classes necessary for the loading bar. One class, nrange, provides a slightly
             modified class of the built-in "range" type in Python that allows me access to extra information. The other
             class, LoadingBar, provides everything to run the actual loading bar.
"""




import threading            # To create the LBar thread
import time                 # To time events in the LBar thread














# Wraps around range-type objects to allow for access to the current iteration
class nrange:
    """
    This class is a replacement for the built-in "range" object returned by Python's "range()" function. This is done
    because I cannot access the current index that is iterating in the regular "range" object. As a result, this class
    is essentially the same as the "range" object, except that it adds a couple things.

    1. An integer instance variable that keeps track of the iterating index.
    2. Extra keywords can be passed into nrange's constructor to customize the loading bar.
    """




    # Construct the object by wrapping an iterator around range(). Also begins the LoadingBar thread.
    def __init__(self, arg1, arg2=None, arg3=1, description="", bar_len=35, bar_char="█", loop_append="", unit="loop",
                       time_unit="s", ):
        """
        Using "nrange()" is exactly the same as using "range()" except that extra optional parameters can be passed in
        after the regular one, two, or three parameters that "range()" uses are passed in. These extra parameters allow
        for the loading bar to be customized.

        :param arg1       : (int)    The exclusive stop index if neither arg2 nor arg3 is provided. The inclusive
                                          start index otherwise.
        :param arg2       : (int)    The inclusive start index if arg1 is provided. The exclusive stop index otherwise
        :param arg3       : (int)    The step applied to the index at the end of every loop.
        :param description: (string) A description of what the for loop is doing.
        :param bar_len    : (int)    How long the bar is, in characters.
        :param bar_char   : (string) The character used to fill the bar.
        :param loop_append: (string) A string appended to the loop number update (such as "K" 857K/857K).
        :param unit       : (string) What object is being worked on in every loop (such as "file" in "file/s").
        :param time_unit  : (string) The unit of time used in measurement (such as "s" in "file/s"). Must be "s", "ms",
                                          "µs", "ns", "min", "hr", "second", "millisecond", "microsecond", "nanosecond",
                                          "minute", or "hour".
        """

        # Instance variables related to the "range" object
        self.range_iterator = None # The iterative form of the "range" object to iterate through
        self.start_idx      = 0    # The start index, inclusive. This is the default value
        self.end_idx        = 0    # The end index, exclusive
        self.step           = arg3 # The step variable added to the current index
        self.current_idx    = None # The current index that the iterator is on

        # Instance variables to save the loading bar details
        self.description = description
        self.bar_len     = bar_len
        self.bar_char    = bar_char
        self.loop_append = loop_append
        self.unit        = unit
        self.time_unit   = time_unit
        self.thread      = None


        # Figure out arg1, arg2, and arg3. If arg2 is not provided, arg1 is the end_idx
        if arg2 is None:
            end_idx   = arg1

        # Else, start_idx and end_idx is provided
        else:
            start_idx = arg1
            end_idx   = arg2


        # Raise exception if time_unit is not a valid choice
        if time_unit not in ["s", "ms", "µs", "ns", "min", "hr", "second", "millisecond", "microsecond", "nanosecond",
                             "minute","hour"]:
            raise ValueError("Invalid time unit given!")


        # Create the self.range_iterator
        self.range_iterator = iter(range(self.start_idx, self.end_idx, self.step))

        # Create the ProgressBar thread, and run it
        self.thread = LoadingBar(self)
        self.thread.start()




    # Called by "in"-operator. Returns the iterator (itself)
    def __iter__(self):
        return self



    # Called by "in"-operator. Used in for-loops to advance to the next element in this range
    def __next__(self):
        self.current = next(self.range_iterator)
        return self.current










# Not directly called (called from nrange's constructor), this class handles the progress bar
class LoadingBar(threading.Thread):
    """
    This class handles the progress bar.
    """


    # This is the constructor for the loading object
    def __init__(self, nrange_obj):
        """
        Creates the loading bar, and sets up important variables

        :param nrange_obj: (nrange) The iterator that the for-loop uses
        """

        # Instance variables copying over important nrange_obj instance variables
        self.nrange_obj  = nrange_obj
        self.start_idx   = nrange_obj.start_idx
        self.end_idx     = nrange_obj.end_idx
        self.step_idx    = nrange_obj.step
        self.current_idx = nrange_obj.start

        # Instance variables useful for loading bar
        self.start_time = time.time()

        self.description = nrange_obj.description
        self.bar_len     = nrange_obj.bar_len
        self.bar_char    = nrange_obj.bar_char
        self.loop_append = nrange_obj.loop_append
        self.unit        = nrange_obj.unit
        self.time_unit   = nrange_obj.time_unit


        # Call super-method
        super().__init__()



    # Called from nrange constructor. This runs the progress-bar
    def run(self):
        """
        This function runs the progress-bar, printing in one line how far progress has gone.

        :return: None
        """

        # Important variables
        bar_length = 100
        progress_bar = "{}{}%|{}| {}/{} [Time elapsed:{}, Time estimated:{}, {} {}/sec]"


        # Print out for the first time (No iterations taken place yet)
        print ("\r" + progress_bar.format(self.description, 0, "▏" * bar_length))


        pass
































