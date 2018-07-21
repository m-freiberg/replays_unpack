#      DO NOT CHANGE THIS FILE     #
# FILE WAS GENERATED AUTOMATICALLY #

from def_generator.events import EventHook
from operator import itemgetter

from def_generator.decorators import unpack_func_args, unpack_variables


try:
    from interfaces.ArtilleryController import ArtilleryController
except:
    from ArtilleryController import ArtilleryController

try:
    from interfaces.BomberController import BomberController
except:
    from BomberController import BomberController

try:
    from interfaces.ProjectileController import ProjectileController
except:
    from ProjectileController import ProjectileController



class AreaDestructibles(ArtilleryController, BomberController, ProjectileController):
    
    def __init__(self):
        self.id = None
        self.position = None


        self._destroyedModules = None

        self._destroyedFragiles = None

        self._fallenColumns = None

        self._fallenTrees = None


        # MRO fix

        ArtilleryController.__init__(self)

        BomberController.__init__(self)

        ProjectileController.__init__(self)

        self._properties = getattr(self, '_properties', [])
        self._properties.extend([
            (10000000000, 'destroyedModules'),
            (10000000000, 'destroyedFragiles'),
            (10000000000, 'fallenColumns'),
            (10000000000, 'fallenTrees'),
            
        ])
        # sort properties by size
        self._properties.sort(key=itemgetter(0))

        self._methods = getattr(self, '_methods', [])
        self._methods.extend([
            
        ])
        # sort methods by size
        self._methods.sort(key=itemgetter(0))
        return

    @property
    def attributesMap(self):
        d = {}
        for i, (_, name) in enumerate(self._properties):
            d[i] = name
        return d

    @property
    def methodsMap(self):
        d = {}
        for i, (_, name) in enumerate(self._methods):
            d[i] = name
        return d

    ####################################
    #      METHODS
    ####################################



    ####################################
    #       PROPERTIES
    ####################################


    # property size: 10000000000
    @property
    def destroyedModules(self):
        return self._destroyedModules

    @destroyedModules.setter
    def destroyedModules(self, value):
        self._destroyedModules, = unpack_variables(value, [['ARRAY', ['ARRAY', 'UINT8', 3]]])

    # property size: 10000000000
    @property
    def destroyedFragiles(self):
        return self._destroyedFragiles

    @destroyedFragiles.setter
    def destroyedFragiles(self, value):
        self._destroyedFragiles, = unpack_variables(value, [['ARRAY', ['ARRAY', 'UINT8', 3]]])

    # property size: 10000000000
    @property
    def fallenColumns(self):
        return self._fallenColumns

    @fallenColumns.setter
    def fallenColumns(self, value):
        self._fallenColumns, = unpack_variables(value, [['ARRAY', ['ARRAY', 'UINT8', 3]]])

    # property size: 10000000000
    @property
    def fallenTrees(self):
        return self._fallenTrees

    @fallenTrees.setter
    def fallenTrees(self, value):
        self._fallenTrees, = unpack_variables(value, [['ARRAY', ['ARRAY', 'UINT8', 5]]])


    def __repr__(self):
        d = {}
        for _, p in self._properties:
            d[p] = getattr(self, p)
        return "<{}> {}".format(self.__class__.__name__, d)