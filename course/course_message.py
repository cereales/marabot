### Setup logger 
import logging
logger = logging.getLogger(__name__)
##logger.setLevel(logging.DEBUG)


class CourseMessage:
    def __init__(self, course, message_course, message_validation=None):
        self.course = course
        self.message_course = message_course
        self.message_validation = message_validation

        self.validated = False


    def set_validate(self):
        self.validated = True
        self.message_validation = None
    

    def __str__(self):
        return "<course=" + str(self.course) + " message=" + str(self.message_course.id) + " from=" + str(self.message_course.author.name) + " valid=" + str(self.message_validation.id) + ">"

    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.course < other.course
    
