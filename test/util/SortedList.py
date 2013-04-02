"""Defines SortedList class."""

import bisect

class SortedList(object):
    """Maintains a list of sorted items, with fast trimming
    using less-than/greater-than comparison."""
    
    def __init__(self, donor=[]):
        """Initialize the object with a copy of the donor list, sorted."""
        self._list = sorted(donor[:])
        
    def add(self, item):
        """Add item to the list while maintaining sorted order."""
        #
        # Native list append() should work, but
        # only if we guaranteed that we're adding the "greatest" item.
        #
        #self._list.append(item)
        #
        # But instead we'll use the sorted insertion.
        bisect.insort_left(self._list, item)

    def getCountLessThan(self, item):
        """Return number of elements less than *item*."""
        index = bisect.bisect_left(self._list, item)
        return index

    def getCountGreaterThan(self, item):
        """Return number of elements greater than *item*."""
        index = bisect.bisect_right(self._list, item)
        return len(self._list) - index

    def removeLessThan(self, item):
        """Trim off any elements less than *item*.
        Return number of elements trimmed."""
        count = self.getCountLessThan(item)
        self._list = self._list[count:]
        return count

# The end.
