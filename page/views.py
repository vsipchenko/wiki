from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Version, Page
from .serializers import PageVersionActivateInput, PageVersionSerializer
from .utils import activate_version, create_active_version, create_new_page


class PageListView(APIView):
    """
    API for managing pages.
    """

    def get(self, request):
        """
        Return JSON response containing data about all active pages.

        Returns:
            HTTP 200.

        """
        qs = Version.objects.filter(is_active=True).order_by('-page_id').distinct('page_id')
        serializer = PageVersionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create new page.

        Raises:
            HTTP 400: If input is invalid.

        Returns:
            HTTP 200: JSON response with information about newly created page.

        """
        serializer = PageVersionSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        page_version = create_new_page(serializer.validated_data)
        return Response(PageVersionSerializer(page_version).data)


class PageVersionsListView(APIView):
    """
    API for managing versions of specific page.
    """

    def get(self, request, page_id):
        """
        Return JSON response containing data about all versions of specific page.

        Raises:
            HTTP 404: If requested page was not found.

        Returns:
            HTTP 200.

        """
        qs = Version.objects.filter(page_id=page_id)
        if not qs.exists():
            raise NotFound(detail='Page not found.')

        serializer = PageVersionSerializer(qs.order_by('-is_active', '-id'), many=True)
        return Response(serializer.data)

    def post(self, request, page_id):
        """
        Create new active version of specific page.

        Raises:
            HTTP 400: If input is invalid.
            HTTP 404: If requested page was not found.

        Returns:
            HTTP 200: JSON response with information about newly created page version.

        """
        if not Page.objects.filter(id=page_id).exists():
            raise NotFound(detail='Page not found.')

        serializer = PageVersionSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        version = create_active_version(page_id, serializer.validated_data)
        return Response(PageVersionSerializer(version).data)


class PageVersionDetailView(APIView):
    """
    API for retrieving specific version of page.
    """

    def get(self, request, page_id, version_id):
        """
        Return JSON response containing information about specific version of page.

        Raises:
            HTTP 404: If requested page or its version was not found.

        Returns:
            HTTP 200.

        """
        version = Version.objects.filter(id=version_id, page_id=page_id).first()
        if not version:
            raise NotFound(detail='Page version not found.')

        return Response(PageVersionSerializer(version).data)


class PageVersionActivateView(APIView):
    """
    API for activating specific version a page.
    """

    def put(self, request, page_id):
        """
        Activate specific page version.

        Raises:
            HTTP 400: If input is invalid or received version does not belong to this page.

        Returns:
            HTTP 200.

        """
        serializer = PageVersionActivateInput(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        version_id = serializer.validated_data['version_id']
        if not Version.objects.filter(id=version_id, page_id=page_id).exists():
            raise ValidationError({'detail': 'Requested version does not belong to this page.'})

        activate_version(page_id, version_id)
        return Response()
