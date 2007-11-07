"""In this module all the object that are used to compose a data-structure
reside.
"""

import thread


### -------------------- factory classes --------------------

class CombiningMeta (type):
    """This is a metaclass that creates classes with the desirable
    name and parentage"""

    def __init__(cls, name, bases, dict):
        super(CombiningMeta, cls).__init__(name, bases, dict)


    @classmethod
    def create_composite(cls, name, bases):
        x = CombiningMeta(name, bases, {})
        return x




### -------------------- data --------------------

class Data(object):
    """The ancestor of all the data."""

    _id_counter = 1
    _id_lock = thread.allocate_lock()
    
    def __init__(self, data_type):
        super(Data, self).__init__()
        self._data_type = data_type
        self._priority = data_type.default_priority()
        Data._id_lock.acquire()
        try:
            self._id = Data._id_counter
            Data._id_counter += 1
        finally:
            Data._id_lock.release()

    def id(self):
        return self._id

    def data_type(self):
        return self._data_type

    def priority(self):
        return self._priority

    def change_priority(self, priority):
        self._priority = priority

    def __str__(self):
        return "%s: type_id='%s', description='%s', priority=%d" % (self.__class__.__name__, self.data_type().id(), self.data_type().description(), self.priority())

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        return ""

    def descendant_generator(self):
        """this is a generator that yields all the child and deeper descendant objects of this object;
        this is useful to flatten the tree-like structure of data into a flat form, without
        the need to check for specific 'child' fields of different object"""
        if False:
            yield None
    

class MultiView(Data):
    """MultiView is an object that has multiple views that represent the structure from
    different points of view. (molecule may be viewed as a picture, MF, Complex structure
    based on parts, etc.)
    """

    def __init__(self, data_type):
        super(MultiView, self).__init__(data_type)
        self._views = []

    def views(self):
        p2v = [(v.priority(), v) for v in self._views]
        p2v.sort(reverse=True)
        vs = [v[1] for v in p2v]
        return vs

    def add_view(self, o):
        """adds a new view to the object"""
        self._views.append(o)

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        ret = []
        parent = super(MultiView, self).text_dump(recursive=recursive,_level=_level,_top_level=False)
        if _top_level:
            ret.append(_level*" "+str(self)+", id=%s" % self.id())
        if parent:
            ret.append(parent)
        if recursive:
            ret.append(_level*" "+" Views:")
            for view in self.views():
                ret.append(view.text_dump(recursive=recursive, _level=_level+2))
        return "\n".join(ret)

    def descendant_generator(self):
        """see the description in Data"""
        for ch in super(MultiView, self).descendant_generator():
            yield ch
        for view in self.views():
            yield view
            for ch in view.descendant_generator():
                yield ch


class Part (Data):
    """Part of some larger entity (see Complex). It provides links
    to other parts of the structure.
    """

    def __init__(self, data_type):
        super(Part, self).__init__(data_type)
        self._neighbors = []

    def add_neighbor(self, rel):
        """rel is the relation"""
        assert isinstance(rel, Relation)
        self._neighbors.append(rel)

    def neighbors(self):
        """returns all relations of this object."""
        return self._neighbors

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        ret = []
        parent = super(Part, self).text_dump(recursive=recursive,_level=_level,_top_level=False)
        if _top_level:
            ret.append(_level*" "+str(self)+", id=%s" % self.id())
        if parent:
            ret.append(parent)
        if recursive:
            ret.append(_level*" "+" Neighbors:")
            for n in self.neighbors():
                ret.append(n.text_dump(recursive=False,_level=_level+2))
                ret.append(n.target().text_dump(recursive=False,_level=_level+3))
        return "\n".join(ret)
    

## ------------------------------ Views ------------------------------

class Value(Data):
    """Simple value."""

    def __init__(self, data_type, value):
        super(Value, self).__init__(data_type)
        self._value = value

    def value(self):
        return self._value

    def __str__(self):
        return "%s: type_id='%s', description='%s', value=%s" % (self.__class__.__name__, self.data_type().id(), self.data_type().description(), self.value())

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        ret = []
        parent = super(Value, self).text_dump(recursive=recursive,_level=_level,_top_level=False)
        if parent:
            ret.append(parent)
        if _top_level:
            ret.append(_level*" "+str(self)+", id=%s" % self.id())
        return "\n".join(ret)



class LanguageDependentValue(Data):
    """Stores localized values for one data_type"""

    # the language codes are taken from the ISO-639-1 standard (published as part of the ISO-639-2 documentation
    # http://www.loc.gov/standards/iso639-2/ISO-639-2_values_8bits-utf-8.txt
    allowed_language_codes = ["aa","ab","af","ak","sq","am","ar","an","hy","as","av","ae","ay","az","ba","bm","eu","be","bn","bh","bi","bs","br","bg","my","ca","ch","ce","zh","cu","cv","kw","co","cr","cs","da","dv","nl","dz","en","eo","et","ee","fo","fj","fi","fr","fy","ff","ka","de","gd","ga","gl","gv","el","gn","gu","ht","ha","he","hz","hi","ho","hu","ig","is","io","ii","iu","ie","ia","id","ik","it","jv","ja","kl","kn","ks","kr","kk","km","ki","rw","ky","kv","kg","ko","kj","ku","lo","la","lv","li","ln","lt","lb","lu","lg","mk","mh","ml","mi","mr","ms","mg","mt","mo","mn","na","nv","nr","nd","ng","ne","nn","nb","no","ny","oc","oj","or","om","os","pa","fa","pi","pl","pt","ps","qu","rm","ro","rn","ru","sg","sa","sr","hr","si","sk","sl","se","sm","sn","sd","so","st","es","sc","ss","su","sw","sv","ty","ta","tt","te","tg","tl","th","bo","ti","to","tn","ts","tk","tr","tw","ug","uk","ur","uz","ve","vi","vo","cy","wa","wo","xh","yi","yo","za","zu"]

    def __init__(self, data_type, value):
        super(LanguageDependentValue, self).__init__(data_type)
        if not type(value) == type({}):
            raise ValueError( "The value of a LanguageDependentValue must be a dictinary mapping from language to value")
        self._check_languages(value)
        self._value = value

    def value(self, lang="en"):
        # return the requested value
        if lang in self._value:
            return (lang, self._value[lang])
        # return english version if localized version is not available
        if "en" in self._value:
            return ("en", self._value['en'])
        # if only one mutation is available, return it
        if len(self._value) == 1:
            lang, val = self._value.items()[0]
            return lang, val
        # if all above has failed, return (None, None)
        return (None, None)

    def available_languages(self):
        return self._value.keys()

    def _check_languages(self, dict):
        """checks if a dictionary contains only allowed language codes"""
        for lang, val in dict.iteritems():
            if lang not in self.allowed_language_codes:
                raise ValueError("Invalid language code %s" % lang)

    def __str__(self):
        return "%s: type_id='%s', description='%s', value=%s" % (self.__class__.__name__, self.data_type().id(), self.data_type().description(), self._value)

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        ret = []
        parent = super(LanguageDependentValue, self).text_dump(recursive=recursive,_level=_level,_top_level=False)
        if parent:
            ret.append(parent)
        if _top_level:
            ret.append(_level*" "+str(self)+", id=%s" % self.id())
        return "\n".join(ret)



class Complex (Data):
    """Complex is a structure that consists of smaller parts (see Part).
    It provides links to the parts.
    It is intended to be used as a View.
    """

    def __init__(self, data_type):
        super(Complex, self).__init__(data_type)
        self._parts = []

    def add_part(self, rel):
        """rel is the relation, if not given a default Relation is created"""
        assert isinstance(rel, Relation)
        self._parts.append(rel)

    def parts(self):
        """returns a list of parts - as relations"""
        return self._parts

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        ret = []
        parent = super(Complex, self).text_dump(recursive=recursive,_level=_level,_top_level=False)
        if _top_level:
            ret.append(_level*" "+str(self)+", id=%s" % self.id())
        if parent:
            ret.append(parent)
        if recursive:
            ret.append(_level*" "+" Parts:")
            for p in self.parts():
                ret.append(p.text_dump(recursive=recursive,_level=_level+2))
        return "\n".join(ret)

    def descendant_generator(self):
        """see the description in Data"""
        for ch in super(Complex, self).descendant_generator():
            yield ch
        for part in self.parts():
            yield part
            for ch in part.descendant_generator():
                yield ch


### -------------------- relation types --------------------

class Relation (Data):
    """this class is used to express relations between other Data-based classes,
    such as between Parts.
    It consists of its data_type and target.
    Uses might be - in math relation will express the operation between two subexpressions,
                  - in chemistry it might describe bond between atoms etc.
    """
    def __init__(self, data_type, target):
        super(Relation, self).__init__(data_type)
        self._target = target

    def target(self):
        return self._target

    def text_dump(self, recursive=False, _level=0, _top_level=True):
        ret = []
        parent = super(Relation, self).text_dump(recursive=recursive,_level=_level,_top_level=False)
        if _top_level:
            ret.append(_level*" "+str(self)+", id=%s" % self.id())
        if parent:
            ret.append(parent)
        if recursive:
            ret.append(self.target().text_dump(recursive=recursive,_level=_level+1))
        return "\n".join(ret)


### derived classes, they have to be here explicitly because Pyro can't handle them
###    otherwise

PartMultiView = CombiningMeta.create_composite("PartMultiView", (Part, MultiView))
ValuePart = CombiningMeta.create_composite("ValuePart", (Value, Part))
#LanguageDependentValuePart = CombiningMeta.create_composite("LanguageDependentValuePart", (LanguageDependentValue, Part))
