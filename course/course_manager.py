### Setup logger 
import logging
logger = logging.getLogger(__name__)
##logger.setLevel(logging.DEBUG)

from course.course_message import CourseMessage
from course.course_list import CourseList


class CourseManager:
    courses_waiting = dict() # buffer of waiting validation courses
    
    @staticmethod
    async def add_new_course(course, message):
        logger.debug("Adding a new course.")

        message_validation = await message.channel.send("Valider " + str(course) + " ?")
        await message_validation.add_reaction("\U00002705")
        await message_validation.add_reaction("\U0000274C")
        # FIXME : there is delay issue with await/async
        assert not CourseManager.is_waiting_course(message_validation.id)
        CourseManager.courses_waiting[message_validation.id] = CourseMessage(course, message, message_validation)


    @staticmethod
    def delete_waiting_course(validation_id):
        course = CourseManager.courses_waiting.pop(validation_id)
        logger.debug("Removed course %s.", course.course)

    
    @staticmethod
    def is_waiting_course(validation_id):
        return validation_id in CourseManager.courses_waiting

    
    @staticmethod
    def get_waiting_course(validation_id):
        if CourseManager.is_waiting_course(validation_id):
            return CourseManager.courses_waiting[validation_id]
        else:
            return None


    @staticmethod
    async def validate_waiting_course(validation_id, emoji_unicode):
        logger.debug("Emoji %s was added as reaction.", emoji_unicode)
        validated = True if str(emoji_unicode) == "\u2705" else False if str(emoji_unicode) == "\u274C" else None
        if validated is None:
            logger.debug("Not expected reaction.")
            return

        course_message = CourseManager.get_waiting_course(validation_id)
        assert course_message is not None
        await course_message.message_validation.delete()
        if validated:
            CourseList.append(course_message)
            course_message.set_validate()
        else:
            CourseManager.delete_waiting_course(validation_id)

    
    @staticmethod
    def __str__():
        """ Works only with CourseManager.__str__() """
        return str(CourseManager.courses_waiting)

    @staticmethod
    def __repr__():
        return "<" + CourseManager.__str__() + ">"
