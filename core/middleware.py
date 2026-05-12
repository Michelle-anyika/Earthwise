from analytics.models import AuditLog

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log only mutation requests (POST, PUT, PATCH, DELETE)
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and response.status_code < 400:
            user = request.user if request.user.is_authenticated else None
            
            # Simple path parsing for resource and ID
            path_parts = request.path.strip('/').split('/')
            resource = path_parts[1] if len(path_parts) > 1 else 'root'
            resource_id = path_parts[2] if len(path_parts) > 2 else None

            AuditLog.objects.create(
                user=user,
                action=f"{request.method} {request.path}",
                resource=resource,
                resource_id=resource_id,
                method=request.method,
                path=request.path,
                ip_address=self.get_client_ip(request)
            )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
