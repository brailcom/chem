"""In this module all the object that are used to compose a data-structure
reside.
"""


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

    def __init__(self, data_type):
        super(Data, self).__init__()
        self._data_type = data_type

    def data_type(self):
        return self._data_type

    def __str__(self):
        return "%s: type_id='%s', description='%s'" % (self.__class__.__name__, self.data_type().id(), self.data_type().description())



class MultiView(Data):
    """MultiView is an object that has multiple views that represent the structure from
    different points of view. (molecule may be view as a picture, MF, Complex structure
    based on parts, etc.)
    """

    def __init__(self, data_type):
        super(MultiView, self).__init__(data_type)
        self._views = []

    def views(self):
        return self._views

    def add_view(self, o):
        """adds a new view to the object"""
        self._views.append(o)


class Part (Data):
    """Part of some larger entity (see Complex). It provides links
    to other parts of the structure.
    """

    def __init__(self, data_type):
        super(Part, self).__init__(data_type)
        self._neighbors = []


    def add_neighbor(self, rel):
        """rel is the relation, if not given a default Relation is created"""
        assert isinstance(rel, Relation)
        self._neighbors.append(rel)


    def neighbors(self):
        """returns all relations of this object."""
        return self._neighbors
    

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


### derived classes, they have to be here explicitly because Pyro can't handle them
###    otherwise

PartMultiView = CombiningMeta.create_composite("PartMultiView", (Part, MultiView))
ValuePart = CombiningMeta.create_composite("ValuePart", (Value, Part))

