### Setup logger 
import logging
logger = logging.getLogger(__name__)
##logger.setLevel(logging.INFO) # localy

import asyncio
import datetime as d
from course.course import Course
from course.course_list import CourseList


def extract_date(string):
    """ Expected format : 00/00/0000 or 00/00/00 """
    logger.debug("Date : %s", string)
    splitted_date = string.split("/")
    try:
        if len(splitted_date[2]) == 2:
            splitted_date[2] = "20" + splitted_date[2]
        else:
            assert len(splitted_date[2]) == 4
        date = d.date(int(splitted_date[2]), int(splitted_date[1]), int(splitted_date[0]))
        return True, date
    except (IndexError, ValueError):
        logger.debug("Is not a date.")
    return False, None

def extract_distance(string):
    """ Expected format : 00.0 or 00,0 or 00.km or 00,0km """
    logger.debug("Distance : %s", string)
    try:
        string = string.replace(',', '.')
        string = string.replace('km', '')
        distance = float(string)
        return True, distance
    except ValueError:
        logger.debug("Is not a distance.")
    return False, None

def extract_time(string):
    """ Expected format : (00'0) or 00'00" or 00' or 00min00sec or 00m00s or 0h0'0"""
    logger.debug("Time : %s", string)
    try:
        string = string.replace('m', 'min')
        string = string.replace('s', 'sec')
        string = string.replace('min', "'")
        string = string.replace('sec', '')
        string = string.replace('(', '')
        string = string.replace(')', '')
        string = string.replace('"', '')

        heure, minute, second = 0, 0, 0
        if "h" in string:
            heure, string = string.split("h")
            heure = int(heure)
        if "'" in string:
            minute, string = string.split("'")
            minute = int(minute)
        quote_in_string = '"' in string
        if quote_in_string:
            string, _ = string.split('"')
        if len(string) > 0 and minute + heure > 0 or quote_in_string:
            second = int(string)

        timedelta = d.timedelta(hours=heure, minutes=minute, seconds=second)
        time = d.time(hour=heure, minute=minute, second=second) # Need values in 0..59
        if timedelta.total_seconds() == 0:
            raise ValueError
        return True, time, timedelta
    except ValueError:
        logger.debug("Is not a time.")
    return False, None, None


async def parse_course_message(message_content):
    logger.info("Message to parse is :\"%s\"", message_content)
    course = Course()
    splitted_message = message_content.split()
    part_max_index = len(splitted_message)

    logger.debug("Splitted message into %s parts.", part_max_index)
    
    part_index = 0
    while part_index < part_max_index:
        is_extracted, date = extract_date(splitted_message[part_index])
        if is_extracted:
            course.set_date(date)
        is_extracted, distance = extract_distance(splitted_message[part_index])
        if is_extracted:
            course.set_distance(distance)
        is_extracted, time, timedelta = extract_time(splitted_message[part_index])
        if is_extracted:
            course.set_time(time, timedelta.total_seconds())
        part_index += 1

    if course.isCourse():
        logger.debug("Parsed course : %s", course)
        return course
    else:
        logger.debug("Parsed message is not a course.")
        return None

