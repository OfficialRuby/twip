from django.utils import timezone
from dash.models import Visitor
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2


class LogUserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = self.get_response(request)
        # only log ip in production
        if not settings.DEBUG:
            client_ip = self.get_client_ip(request)
            # client_ip = '129.205.113.146'
            visitor = Visitor.objects.filter(ip_address=client_ip)
            if not visitor:
                try:
                    geoip = GeoIP2()
                    ip_dict = geoip.city(client_ip)
                    Visitor.objects.create(
                        ip_address=client_ip,
                        city=ip_dict.get('city'),
                        continent_code=ip_dict.get('continent_code'),
                        continent_name=ip_dict.get('continent_name'),
                        country_code=ip_dict.get('country_code'),
                        country_name=ip_dict.get('country_name'),
                        region=ip_dict.get('region'),
                        time_zone=ip_dict.get('time_zone'),
                        latitude=ip_dict.get('latitude'),
                        longitude=ip_dict.get('longitude'),

                    )
                except Exception:
                    return response
            else:
                visitor.update(timestamp=timezone.now())

        return response

    def get_client_ip(self, request):
        ip = None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
