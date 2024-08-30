class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("run before ")
        response = self.get_response(request)
        print("run after")
        return response

