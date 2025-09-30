"""
Classes to help with the process of "filling-in" DOM elements which refer to model objects
with data from the referenced object, so that people don't have to copy.

For each new referenceable model type, add a resolve here and "register" it in REF_RESOLVERS.
"""

import re

from django.utils.safestring import mark_safe
from html import unescape, escape
from .models import Lesson, ZoomingImage, CapsuleUnit, GlossaryTerm

from bs4 import NavigableString
from bs4 import BeautifulSoup, Comment
import traceback

def evaluate_content(lesson_content, strip_bad_references=False):

    pattern = re.compile(r"(?<=\<code-block\>)(.*?)(?=\<\/code-block\>)", re.DOTALL)
    result = re.sub(pattern, encode_text, lesson_content)

    soup = BeautifulSoup(result, 'html.parser')

    """Convert any convenience markup (such as object references) into the ideal markup
       for delivering to the page. Optionally remove from DOM elements which have ref
       attrutes which don't resolve to actual objects. (Do this in production but show them in draft/editing mode.)
    """
    for elem in soup.find_all(ref=True):
        try:
            REF_RESOLVERS[elem.name].resolve_ref(elem, strip_bad_references)
        except KeyError:
            pass

    return soup.prettify()


def encode_text(match):
    return escape(unescape(match.group(0)))


class ReferenceResolver(object):
    """An abstract class"""
    klass = None
    ref_attr = 'ref'
    property = 'slug'

    def get_object(self, elem):
        id = elem.attrs['ref']
        kwargs = {self.property: id}
        self.klass.objects.get(**kwargs)
        return self.klass.objects.get(slug=id)

    def resolve_ref(self, elem, strip_bad_references):
        """Given an element, look up the matching object and populate the given element.
           If strip_bad_references is True, then remove the element if no corresponding object
           could be found. Whether or not the object is removed, add an HTML comment
           indicating that the reference could not be resolved.
        """
        try:
            obj = self.get_object(elem)
            self.update_element(elem, obj)
        except Exception as e:
            self.note_error(elem, "Reference could not be resolved", strip_bad_references)
            self.note_error(elem, traceback.format_exc(), strip_bad_references)

    def note_error(self, elem, message, strip):
        elem.append(Comment(message))
        if strip:
            elem.parent().clear()

    def update_element(self, elem, obj):
        pass


class LessonRefResolver(ReferenceResolver):
    klass = Lesson

    def update_element(self, elem, obj):
        elem.attrs['image'] = obj.banner_image.url
        elem.attrs['header'] = obj.title
        elem.attrs['url'] = obj.get_absolute_url()
        for i,item in enumerate(BeautifulSoup(obj.reference_blurb, "lxml").html.body.contents):
            elem.insert(i+1, item)



class ZoomingImageRefResolver(ReferenceResolver):
    klass = ZoomingImage

    def update_element(self, elem, obj):
        # Use local static files instead of S3
        from django.templatetags.static import static
        import os

        # Extract filename from the image field
        image_filename = os.path.basename(obj.image.name)

        # Construct local static URLs using Django's static() function
        static_path = f"zimages/{image_filename}"
        elem.attrs['src'] = static(static_path)
        elem.attrs['full-src'] = static(static_path)


class CapsuleRefResolver(ReferenceResolver):
    """A Capsule Unit has a header, an image URL, and HTML content."""
    klass = CapsuleUnit

    def update_element(self, elem, obj):
        elem.attrs['image'] = obj.image.url
        elem.attrs['header'] = obj.title
        for i,item in enumerate(BeautifulSoup(obj.content, "lxml").html.body.contents):
            elem.insert(i+1, item)


REF_RESOLVERS = {
    'zooming-image': ZoomingImageRefResolver(),
    'lesson-ref': LessonRefResolver(),
    'capsule-unit': CapsuleRefResolver(),
}
