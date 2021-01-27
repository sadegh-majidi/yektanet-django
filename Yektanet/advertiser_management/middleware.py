class ExtractIpMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        target = ['ShowAllAdsListView', 'AdClickRedirectView']
        if view_func.__name__ in target:
            ip = request.META.get('REMOTE_ADDR')
            request.user_ip = ip
