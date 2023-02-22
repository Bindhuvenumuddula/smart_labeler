from base64 import b64encode

from django import template

register = template.Library()
@register.filter(name="to_img")
def img_to_b64(_img):
    if _img is not None:
        return b64encode(_img).decode('utf-8')
