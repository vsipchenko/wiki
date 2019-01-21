from django.test import TestCase

from .models import Page, Version
from .utils import activate_version, create_active_version, create_new_page


class WikiBaseTestCase(TestCase):
    """
    Base class for testing utils.
    """
    test_data = {'title': 'new_page_title', 'text': 'new_page_text'}

    def setUp(self):
        page_1 = Page.objects.create()
        Version.objects.create(page=page_1, title='active_version_title1',
                               text='active_version_text1', is_active=True)
        Version.objects.create(page=page_1, title='inactive_version_title1',
                               text='inactive_version_text1', is_active=False)


class PageVersionUtilsTestCase(WikiBaseTestCase):
    """
    Test utils from page application.
    """

    def test_create_new_page(self):
        """
        Test create_new_page util.
        """
        pages_count_before = Page.objects.count()
        versions_count_before = Version.objects.count()
        new_page_version = create_new_page(self.test_data)
        pages_count_after = Page.objects.count()
        versions_count_after = Version.objects.count()

        # Check pages quantity was increased.
        self.assertEqual(pages_count_before + 1, pages_count_after)

        # Check versions quantity increased.
        self.assertEqual(versions_count_before + 1, versions_count_after)

        # Check new version is active.
        self.assertTrue(new_page_version.is_active)

    def test_create_active_version(self):
        """
        Test create_active_version util.
        """
        page = Page.objects.last()
        versions_count_before = Version.objects.filter(page_id=page.id).count()
        active_version_before = Version.objects.filter(page_id=page.id, is_active=True).first()
        active_version_after = create_active_version(page.id, self.test_data)
        versions_count_after = Version.objects.filter(page_id=page.id).count()
        active_version_count = Version.objects.filter(page_id=page.id, is_active=True).count()

        # Check versions quantity was increased.
        self.assertEqual(versions_count_before + 1, versions_count_after)

        # Check page of new version stayed same.
        self.assertEqual(page.id, active_version_after.page_id)

        # Check only one active version exists.
        self.assertEqual(active_version_count, 1)

        # Check active version changed.
        self.assertNotEqual(active_version_before.id, active_version_after.id)

        # Check new version is active.
        self.assertTrue(active_version_after.is_active)

    def test_activate_version(self):
        """
        Test activate_version util.
        """
        page = Page.objects.last()
        versions_count_before = Version.objects.filter(page_id=page.id).count()
        active_version_before = Version.objects.filter(page_id=page.id, is_active=True).first()
        version_to_activate = Version.objects.filter(page_id=page.id, is_active=False).first()
        activate_version(page.id, version_to_activate.id)
        activated_version = Version.objects.filter(page_id=page.id, is_active=True).first()
        versions_count_after = Version.objects.filter(page_id=page.id).count()
        active_version_count = Version.objects.filter(page_id=page.id, is_active=True).count()

        # Check only one active version exists.
        self.assertEqual(active_version_count, 1)

        # Check page versions quantity did not change.
        self.assertEqual(versions_count_before, versions_count_after)

        # Check page of new version stayed same.
        self.assertEqual(page.id, activated_version.page_id)

        # Check active version changed.
        self.assertNotEqual(active_version_before.id, activated_version.id)

        # Check new version is active.
        self.assertTrue(activated_version.is_active)
