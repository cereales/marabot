### Setup logger 
import logging
logger = logging.getLogger(__name__)
##logger.setLevel(logging.DEBUG)


class CourseList:
    courses = dict()
    runner_ids = list()
    
    @staticmethod
    def append(course):
        logger.debug("%s elements - Adding a new course", len(CourseList.courses))
        assert not CourseList.in_list(course.message_course.id)
        CourseList.courses[course.message_course.id] = course
        if course.message_course.author.id not in CourseList.runner_ids:
            CourseList.runner_ids.append(course.message_course.author.id)


    @staticmethod
    def in_list(course_message_id):
        return course_message_id in CourseList.courses


    @staticmethod
    def get_runner_ids():
        return CourseList.runner_ids

    @staticmethod
    def get_courses_of(runner_id):
        #TODO store 1 dict for each runner ?
        course_list = list()
        runner_nickname = runner_id
        for course_message_id in CourseList.courses:
            course_message = CourseList.courses[course_message_id]
            course = course_message.course
            if course_message.message_course.author.id == runner_id:
                course_list.append(course_message)
                message = course_message.message_course
                authorHasNickname = message.author.nick is not None # must be in server
                runner_nickname = message.author.nick if authorHasNickname else message.author.name
        course_list.sort()
        
        date_list, distance_list, vitesse_list = [], [], []
        for course_message in course_list:
            c = course_message.course
            vitesse = c.distance / c.total_second * 3600
            if vitesse > 20:
                logger.error("Vitesse %s is too high. Message %s : %s", vitesse, course_message.message_course.id, course_message.message_course.content)
            else:
                date_list.append(c.date)
                distance_list.append(c.distance)
                vitesse_list.append(vitesse)
        return date_list, distance_list, vitesse_list, runner_nickname

    
    @staticmethod
    def __str__():
        return str(CourseList.courses)
    
