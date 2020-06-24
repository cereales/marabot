### Setup logger 
import logging
logger = logging.getLogger(__name__)
##logger.setLevel(logging.DEBUG)

import discord
from actions.action import AbstractAction
from course.course_list import CourseList
from course.course_message import CourseMessage
from course.parser import parse_course_message

import datetime as d
import matplotlib.pyplot as plt
import numpy as np


class Graphe(AbstractAction):

    @staticmethod
    def command():
        return "graphe"

    @staticmethod
    def command_short():
        return "g"

    @staticmethod
    def help_description():
        return "Tracer le graphe des performances"

    @staticmethod
    def help_args():
        return [""]


    @staticmethod
    async def on_call(message, client):
        start_processing_time = d.datetime.now()
        async with message.channel.typing():
            start_day = await get_courses_from_search(client, message.channel)
            chart_path = draw_chart(client)
            chart = discord.File(chart_path + ".png")
            await message.channel.send("Performances des coureurs depuis le " + str(start_day.date()) + ".", file=chart)
        logger.info("Processed during %s.", d.datetime.now() - start_processing_time)


async def get_courses_from_search(client, channel):
    today = d.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    start_day = today - d.timedelta(days=56)
    found_new_courses = 0
    logger.info("Parsing message since %s.", start_day)
    async for message in channel.history(limit=None, after=start_day):
        course = await parse_course_message(message.content)
        if course is not None and not CourseList.in_list(message.id):
            logger.debug('Message %s from %s on %s : "%s"', message.id, message.author.name, message.created_at, message.content)
            found_new_courses += 1
            course_message = CourseMessage(course, message)
            CourseList.append(course_message)
    logger.info("Found %s new courses since %s", found_new_courses, start_day)
    return start_day


def draw_chart(client):
    plt.clf()
    for runner_id in CourseList.get_runner_ids():
        x, bar, courbe, nickname = CourseList.get_courses_of(runner_id)
        plt.bar(x, bar, label=str("Distance de " + nickname))
        line,  = plt.plot(x, courbe, '+-', label=str("Vitesse de " + nickname))
    plt.xticks(rotation='vertical')
    plt.legend()
    plt.savefig("ressources/graphe")
    #TODO use msg id to avoid concurent issue
    return "ressources/graphe"
