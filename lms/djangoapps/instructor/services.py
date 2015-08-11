"""
Implementation of "Instructor" service
"""

import logging

from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey, UsageKey
from courseware.models import StudentModule
from instructor.views.tools import get_student_from_identifier
from django.core.exceptions import ObjectDoesNotExist
import instructor.enrollment as enrollment


log = logging.getLogger(__name__)


class InstructorService(object):
    """
    Instructor service for deleting the students attempt(s) of an exam. This service has been created
    for the edx_proctoring's dependency injection to cater for a requirement where edx_proctoring
    needs to call into edx-platform's functions to delete the students' existing answers, grades
    and attempt counts if there had been an earlier attempt.
    """

    def delete_student_attempt(self, student_identifier, course_id, content_id):
        """
        Deletes student state for a problem.

        Takes some of the following query parameters
            - content_id is a url-name of a problem
            - unique_student_identifier is an email or username
            - course_id is the id for the course
        """
        course_id = CourseKey.from_string(course_id)

        try:
            student = get_student_from_identifier(student_identifier)
        except ObjectDoesNotExist:
            err_msg = (
                'Error occurred while attempting to reset student attempts for user '
                '{student_identifier} for content_id {content_id}. '
                'User does not exist!'.format(
                    student_identifier=student_identifier,
                    content_id=content_id
                )
            )
            log.error(err_msg)
            return

        try:
            module_state_key = UsageKey.from_string(content_id)
        except InvalidKeyError:
            err_msg = (
                'Invalid content_id {content_id}!'.format(content_id=content_id)
            )
            log.error(err_msg)
            return

        if student:
            try:
                enrollment.reset_student_attempts(course_id, student, module_state_key, delete_module=True)
            except (StudentModule.DoesNotExist, enrollment.sub_api.SubmissionError):
                err_msg = (
                    'Error occurred while attempting to reset student attempts for user '
                    '{student_identifier} for content_id {content_id}.'.format(
                        student_identifier=student_identifier,
                        content_id=content_id
                    )
                )
                log.error(err_msg)
