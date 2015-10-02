"""
Classes to help with the process of "filling-in" DOM elements which refer to model objects
with data from the referenced object, so that people don't have to copy.

For each new referenceable model type, add a resolve here and "register" it in REF_RESOLVERS.
"""
# from django.utils.html import escape
from django.utils.safestring import mark_safe
from html import escape, unescape
from lxml.html.clean import clean_html

from .models import Lesson, ZoomingImage, CapsuleUnit, GlossaryTerm
from lxml.etree import Comment
from lxml.html import fromstring, tostring
from collections import defaultdict

import logging

def evaluate_content(element,strip_bad_references=False):
    """Convert any convenience markup (such as object references) into the ideal markup
       for delivering to the page. Optionally remove from DOM elements which have ref
       attributes which don't resolve to actual objects. (Do this in production but show them in draft/editing mode.)
    """
    for elem in element.findall('.//*[@ref]'):
        try:
            REF_RESOLVERS[elem.tag].resolve_ref(elem,strip_bad_references)
        except KeyError:
            self.note_error(elem,"Unrecognized ref type", strip_bad_references)

    """Escape Codeblocks"""
    for elem in element.findall('.//code-block'):
        inner_html = (elem.text or '') + ''.join([tostring(child).decode('utf-8') for child in elem.iterchildren()])
        for child in elem.iterchildren():
            child.drop_tree()
        elem.text = mark_safe(unescape(inner_html))


class ReferenceResolver(object):
    """An abstract class"""
    klass = None
    ref_attr = 'ref'
    property = 'slug'
    def get_object(self, elem):
        id = elem.attrib[self.ref_attr]
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
            self.note_error(elem,"Reference could not be resolved", strip_bad_references)

    def note_error(self, elem, message, strip):
        elem.addnext(Comment(message))
        if strip:
            elem.getparent().remove(elem)

    def update_element(self, elem, obj):
        pass

class LessonRefResolver(ReferenceResolver):
    klass = Lesson

    def update_element(self, elem, obj):
        elem.attrib['image'] = obj.banner_image.url
        elem.attrib['header'] = obj.title
        elem.attrib['url'] = obj.get_absolute_url()
        elem.text = obj.reference_blurb

class ZoomingImageRefResolver(ReferenceResolver):
    klass = ZoomingImage

    def update_element(self, elem, obj):
        elem.attrib['src'] = obj.thumbnail.url
        elem.attrib['full-src'] = obj.image.url


class CapsuleRefResolver(ReferenceResolver):
    """A Capsule Unit has a header, an image URL, and HTML content."""
    klass = CapsuleUnit

    def update_element(self, elem, obj):
        elem.attrib['image'] = obj.image.url
        elem.attrib['header'] = obj.title
        elem.append(fromstring(obj.content))

REF_RESOLVERS = {
    'zooming-image': ZoomingImageRefResolver(),
    'lesson-ref': LessonRefResolver(),
    'capsule-unit': CapsuleRefResolver(),
}
