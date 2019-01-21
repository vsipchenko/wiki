from django.db import transaction

from .models import Page, Version


def create_new_page(validated_data):
    """
    Create new Page and it's Version.

    Args:
       validated_data (dict): Data used for page version creation.

    Returns:
        Version: Instance of newly created Version.

    """
    with transaction.atomic():
        page = Page.objects.create()
        version = Version.objects.create(page=page, is_active=True, **validated_data)
    return version


def create_active_version(page_id, validated_data):
    """
    Create new version of a page.

    Newly created version becomes active, all other become inactive.

    Args:
        page_id (int): ID of Page.
        validated_data (dict): Data used for page version creation.

    Returns:
        Version: Instance of newly created active Version.

    """
    with transaction.atomic():
        Version.objects.filter(page_id=page_id).update(is_active=False)
        version = Version.objects.create(page_id=page_id, is_active=True, **validated_data)
    return version


def activate_version(page_id, version_id):
    """
    Activate specific version of a page and deactivate all other page versions.

    This util does not check that version exist and belong to this page, such validation should be
    performed on a view level.

    Args:
        page_id (int): ID of Page.
        version_id (int): ID of Version to activate.

    """
    page_versions = Version.objects.filter(page_id=page_id)
    with transaction.atomic():
        page_versions.update(is_active=False)
        page_versions.filter(id=version_id).update(is_active=True)
