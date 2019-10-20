from django.urls import path
from django.template.loader import render_to_string
from django.http import HttpResponse


from django.views.generic import TemplateView

example_context = {
    "obj": { 
        "a": 5,
        "sentence": "<script> alert('hacked') </script> "
    },
    "num_list": [1,2,3,4],
}

def plain_view(request):
    rendered = render_to_string("example1.html",example_context)
    return HttpResponse(rendered)


class Example(TemplateView):
    # just double checking render_to_string works identically to what views do...
    template_name="example1.html"
    def get_context_data(self):
        return {
            **super().get_context_data(),
            **example_context
        }



urlpatterns = [
    path('example-with-cbv/', Example.as_view(), name='example-with-cbv'),
    path('example-plain/', plain_view, name='example-plain'),
]
