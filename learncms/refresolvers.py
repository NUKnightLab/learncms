"""
Classes to help with the process of "filling-in" DOM elements which refer to model objects
with data from the referenced object, so that people don't have to copy.

For each new referenceable model type, add a resolve here and "register" it in REF_RESOLVERS.
"""
from .models import Lesson, ZoomingImage, CapsuleUnit, GlossaryTerm
from lxml.etree import Comment
from lxml.html import fromstring, tostring
from collections import defaultdict

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

    terms = defaultdict(list)
    defs = dict()
    for gt in element.findall('.//glossary-term'):
        lemma = gt.attrib.get('lemma',gt.text_content())
        if lemma:
            terms[lemma].append(gt)

    for defn in GlossaryTerm.objects.filter(lemma__in=terms):
        defs[defn.lemma] = defn
    # right now terms must be an exact match for what's in the DB
    # we could try harder to deal with case variations, but also the
    # lemma attribute provides a way to clue the system in.

    for lemma,gts in terms.items():
        try:
            defn = defs[lemma].definition
        except:
            if strip_bad_references:
                defn = None
            else:
                defn = "No definition for {}".format(lemma)
        for gt in gts:
            if defn:
                gt.attrib['definition'] = defn


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
        elem.attrib['title'] = obj.title
        elem.attrib['url'] = obj.get_absolute_url()
        elem.text = obj.reference_blurb

class ZoomingImageRefResolver(ReferenceResolver):
    klass = ZoomingImage

    def update_element(self, elem, obj):
        elem.attrib['src'] = obj.thumbnail.url
        elem.attrib['fullSrc'] = obj.image.url


class CapsuleRefResolver(ReferenceResolver):
    """A Capsule Unit has a title, an image URL, and HTML content."""
    klass = CapsuleUnit

    def update_element(self, elem, obj):
        elem.attrib['image'] = obj.image.url
        elem.attrib['title'] = obj.title
        elem.append(fromstring(obj.content))

REF_RESOLVERS = {
    'zooming-image': ZoomingImageRefResolver(),
    'lesson-ref': LessonRefResolver(),
    'capsule-unit': CapsuleRefResolver(),
}
