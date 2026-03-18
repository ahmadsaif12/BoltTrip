import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that provides consistent error responses.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log the exception
        logger.warning(
            f"API Error: {exc.__class__.__name__}",
            extra={
                'view': context.get('view'),
                'request': context.get('request'),
                'error': str(exc),
            }
        )
        
        # Customize response format
        if isinstance(response.data, dict):
            response.data = {
                'success': False,
                'error': response.data.get('detail', 'An error occurred'),
                'errors': response.data if 'detail' not in response.data else None,
                'status_code': response.status_code,
            }
        else:
            response.data = {
                'success': False,
                'error': str(response.data),
                'status_code': response.status_code,
            }
    else:
        # Handle unexpected errors
        logger.error(
            f"Unexpected Error: {exc.__class__.__name__}",
            exc_info=True,
            extra={'view': context.get('view')},
        )
        
        response = Response(
            {
                'success': False,
                'error': 'Internal server error. Please contact support.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    return response
