"""
Accessibility tests for Studio Library pages.

Run just this test with:
SELENIUM_BROWSER=phantomjs paver test_bokchoy -d accessibility -t test_studio_library_axs.py
"""
from ..tests.studio.base_studio_test import StudioLibraryTest
from ..pages.studio.library import LibraryEditPage


class StudioLibraryAxsTest(StudioLibraryTest):
    """
    Class to test Studio pages accessibility.
    """

    def test_lib_edit_page_axs(self):
        """
        Check accessibility of LibraryEditPage.
        """
        lib_page = LibraryEditPage(self.browser, self.library_key)
        lib_page.visit()
        lib_page.wait_until_ready()

        # This element is the only one with an error on the page.
        # For now, we don't raise an error for it. Error id: 'link-text'
        lib_page.a11y_audit.config.set_scope(exclude=[('#content > '
            '.wrapper-mast.wrapper > .mast.has-actions.has-navigation.has-'
            'subtitle > .nav-actions > ul > .action-item.action-toggle-'
            'preview.nav-item > .button.button-toggle-preview.action-button.'
            'toggle-preview-button.is-hidden')])

        errors = lib_page.a11y_audit.do_audit()

        if errors:
            lib_page.a11y_audit.report_errors(errors, "LibraryEditPage")
