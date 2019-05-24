import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)

# Default landing page
def test(request):
    logger.info('Index')
    return render(request, 'gcm_app/base.html')