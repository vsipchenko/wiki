from django.db import models


class Page(models.Model):
    """
    Page

    For now it has no attributes, only primary key, which can be used in Version model.

    """

    def __str__(self):
        return str(self.id)


class Version(models.Model):
    """
    Version of specific page.

    Due to business logic only one version can be active.

    Attributes:
       page: Page.
       title: Title of a page.
       text: Text of a page.
       is_active: Flag indicates whether version of a page is active.

    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.page_id, self.title)
