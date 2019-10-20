from django.template.loader import render_to_string

from snapshottest.django import TestCase


class BasicTestCase(TestCase):
    def test_basic_single_arg_component(self):
        test_context = {
            "obj": { 
            "a": 5,
                "sentence": "<script> alert('hacked') </script> "
            },
            "num_list": [1,2,3,4],
        }

        rendered = render_to_string("example1.html", test_context)
        self.assertMatchSnapshot(rendered)