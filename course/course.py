import logging
logger = logging.getLogger(__name__)
##logger.setLevel(logging.DEBUG)
import datetime as d


class Course:
    def __init__(self):
        self.date = None
        self.distance = None
        self.time = None
        self.total_second = None

                
    def isCourse(self):
        """
        Return true or false.
        """
        return self.date is not None and self.distance is not None and self.time is not None and self.total_second is not None

    def __str__(self):
        """ Return course in format "dd/mm/yyyy : 0,0 km (00'00)". """
        res = ""
        if self.date is not None:
            res += self.date.strftime("%d/%m/%Y") + " : "
        else:
            res += "**/**/**** : "
        if self.distance is not None:
            res += str(self.distance).replace('.', ',') + " km "
        else:
            res += "*,* km "
        if self.time is not None:
            res += "("
            if self.time >= d.time(hour=1):
                res += str(self.time.hour) + "h"
            if self.time.second == 0:
                res += self.time.strftime("%M'")
            else:
                res += self.time.strftime("%M'%S")
            res += ")"
        else:
            res += "(**')"
        return res

    def __repr__(self):
        return "<" + str(self) + ">"

    def __lt__(self, course):
        return self.date < course.date

    def set_date(self, date):
        assert type(date) == d.date
        if self.date is None:
            logger.debug("Setting date to %s.", date)
            self.date = date
        else:
            logger.warning("Date already on %s.", self.date)

    def set_distance(self, distance):
        assert type(distance) == float
        if self.distance is None:
            logger.debug("Setting distance to %s km.", distance)
            self.distance = distance
        else:
            logger.warning("Distance already on %s.", self.distance)

    def set_time(self, time, total_second):
        assert type(time) == d.time
        assert type(total_second) == float
        if self.time is None:
            logger.debug("Setting time to %s.", time)
            self.time = time
            self.total_second = total_second
        else:
            logger.warning("Time already on %s.", self.time)
