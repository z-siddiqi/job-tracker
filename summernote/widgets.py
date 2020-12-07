import json

from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

config = {
    'empty': ('<p><br/></p>', '<p><br></p>'),
    'summernote': {
        'lang': 'en-US',
        'width': '100%',
        'height': '300',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline']],
            ['para', ['ul', 'ol']],
        ],
        'styleTags': ['p', 'h1', 'h2'],
        'disableResizeEditor': True,
    },
}


class SummernoteInplaceWidget(Textarea):

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)

        if value in config['empty']:
            return None

        return value

    def use_required_attribute(self, initial):
        return False
    
    def render(self, name, value, attrs=None, **kwargs):
        summernote_settings = config.get('summernote', {}).copy()
        html = super(SummernoteInplaceWidget, self).render(
            name, value, attrs=attrs, **kwargs
        )
        context = {
            'settings': json.dumps(summernote_settings),
        }
        html += render_to_string(
            'summernote/widget.html', 
            context=context
        )
        return mark_safe(html)
