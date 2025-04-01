import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


class AccessLogMiddleware:
    """
    Middleware that logs access attempts to protected paths
    if the user is not authenticated.
    """

    def __init__(self, get_response: Callable) -> None:
        """
        Standard Django middleware initializer.
        """
        self.get_response = get_response
        self.protected_paths = ['/', 'lookup/']

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Called for each request; logs unauthorized access to protected paths.
        :return: HttpResponse
        """
        if not request.user.is_authenticated and request.path in self.protected_paths:
            logger.info(f"Unauthorized access to {request.path}")
        return self.get_response(request)


class ErrorHandlerMiddleware:
    """
    Middleware to render custom 404 and 500 error pages.
    """

    def __init__(self, get_response: Callable) -> None:
        """
        Standard Django middleware initializer.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Called for each request; handles error pages.
        :return: HttpResponse
        """
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'minimal_user/404.html', status=404)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
        """
        Handles unhandled exceptions and renders a custom 500 error page.
        :return: HttpResponse
        """
        return render(request, 'minimal_user/500.html', status=500)
