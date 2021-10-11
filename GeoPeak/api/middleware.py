import ipinfo

from django.core.exceptions import PermissionDenied

from .models import AllowCountry


class FilterCountryIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.access_token = "c2c9f6a95b5286"

    def __call__(self, request):
        query_country = AllowCountry.objects.all()
        allowed_country = [item.code for item in query_country]
        handler = ipinfo.getHandler(self.access_token)
        ip_address = request.META.get('REMOTE_ADDR')
        details = handler.getDetails(ip_address)
        try:
            country = details.country.upper()
        except:
            country = "FR"
        if country in allowed_country:
            response = self.get_response(request)
        else:
            raise PermissionDenied
        return response
