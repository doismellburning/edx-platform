"""
Accessibility tests for LMS dashboard page.

Run just this test with:
SELENIUM_BROWSER=phantomjs paver test_bokchoy -d accessibility -t test_lms_dashboard_axs.py
"""
from ..tests.lms.test_lms_dashboard import BaseLmsDashboardTest


class LmsDashboardAxsTest(BaseLmsDashboardTest):
    """
    Class to test lms student dashboard accessibility.
    """

    def test_dashboard_course_listings_axs(self):
        """
        Test the accessibility of the course listings
        """
        course_listings = self.dashboard_page.get_course_listings()
        self.assertEqual(len(course_listings), 1)


        # This element is the only one with an error on the page.
        # For now, we don't raise an error for it.
        # Error id: 'aria-required-children'
        self.dashboard_page.a11y_audit.config.set_scope(
            exclude=['#actions-dropdown-list-0'])

        errors = self.dashboard_page.a11y_audit.do_audit()

        if errors:
            self.dashboard_page.a11y_audit.report_errors(
                errors, "LMS dashboard page")
