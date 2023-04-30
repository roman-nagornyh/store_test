from .models import Bucket
from django.http import HttpResponseRedirect


class BucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if not isinstance(response, HttpResponseRedirect):
            if request.user.is_authenticated:
                pr_count = Bucket.objects.filter(user_id=request.user.id).count()
            else:
                if "products" in request.session:
                    pr_count = len(request.session["products"])
                else:
                    pr_count = 0
            response.context_data["pr_count"] = pr_count
        return response
