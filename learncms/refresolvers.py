"""
Classes to help with the process of "filling-in" DOM elements which refer to model objects
with data from the referenced object, so that people don't have to copy.

For each new referenceable model type, add a resolve here and "register" it in REF_RESOLVERS.
"""
from django.utils.safestring import mark_safe
from html import unescape
from .models import Lesson, ZoomingImage, CapsuleUnit, GlossaryTerm

from bs4 import NavigableString
from bs4 import BeautifulSoup, Comment


def evaluate_content(lesson_content, strip_bad_references=False):
    soup = BeautifulSoup(lesson_content, 'html.parser')

    """Convert any convenience markup (such as object references) into the ideal markup
       for delivering to the page. Optionally remove from DOM elements which have ref
       attrutes which don't resolve to actual objects. (Do this in production but show them in draft/editing mode.)
    """
    for elem in soup.find_all(ref=True):
        try:
            REF_RESOLVERS[elem.name].resolve_ref(elem, strip_bad_references)
        except KeyError:
            pass
            # error_resolver = LessonRefResolver()
            # error_resolver.note_error(elem, "Unrecognized ref type", strip_bad_references)

    """Escape Codeblocks"""
    for elem in soup.find_all('code-block'):
        string = elem.decode_contents()
        elem.string = mark_safe(unescape(string))

    return soup.prettify()


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
        print("SDGSDGSDGSDG")
        try:
            obj = self.get_object(elem)
            self.update_element(elem, obj)
        except Exception as e:
            self.note_error(elem, "Reference could not be resolved", strip_bad_references)

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
        elem.insert(1, BeautifulSoup(obj.reference_blurb).html.body.contents[0])


class ZoomingImageRefResolver(ReferenceResolver):
    klass = ZoomingImage

    def update_element(self, elem, obj):
        elem.attrs['src'] = obj.thumbnail.url
        elem.attrs['full-src'] = obj.image.url


class CapsuleRefResolver(ReferenceResolver):
    """A Capsule Unit has a header, an image URL, and HTML content."""
    klass = CapsuleUnit

    def update_element(self, elem, obj):
        elem.attrs['image'] = obj.image.url
        elem.attrs['header'] = obj.title
        elem.insert(1, BeautifulSoup(obj.content).html.body.contents[0])


REF_RESOLVERS = {
    'zooming-image': ZoomingImageRefResolver(),
    'lesson-ref': LessonRefResolver(),
    'capsule-unit': CapsuleRefResolver(),
}
