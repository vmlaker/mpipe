"""Defines RateTicker class."""

import datetime
from .SortedList import SortedList

class RateTicker(SortedList):
    """Computes rates of ticking."""
    
    def __init__(self, periods):
        """Initialize the object with a tuple of time periods in seconds.
        For example, use (60, 300, 900) to track rates at 1, 5 and 15 minute
        periods (like when reporting system load.)"""
        super(RateTicker, self).__init__()
        self._periods = periods

    def tick(self):
        """Tick the ticker. 
        Return a tuple of values corresponding to periods given in initializer, 
        each value representing the rate of ticks (number of ticks per second)
        during that period."""
        now = datetime.datetime.now()
        self.add(now)

        # Create a list of timestamps, one for each period and 
        # representing the beginning of that period (i.e. since now.)
        tstamps = [now - datetime.timedelta(seconds=xx) for xx in self._periods]
        
        # Trim off any tick values older than the earliest timestamp.
        self.removeLessThan(min(tstamps))

        # Create a list of counts, one for each period and 
        # representing the number of ticks in that period.
        counts = [self.getCountGreaterThan(xx) for xx in tstamps]

        # Compute a list of rates for the periods.
        rates = [float(xx)/yy for xx,yy in zip(counts, self._periods)]

        # Return the rates as a tuple.
        return tuple(rates)

# The end.
