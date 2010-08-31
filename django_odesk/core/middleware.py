from django_odesk.core.clients import RequestClient

class RequestClientMiddleware(object):

    def process_request(self, request):
        """
        Injects an initialized oDesk client to every request, making 
        it easy to use it in views
        """
        request.odesk_client = RequestClient(request)
        return None
