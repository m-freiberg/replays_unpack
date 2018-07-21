#      DO NOT CHANGE THIS FILE     #
# FILE WAS GENERATED AUTOMATICALLY #

from def_generator.events import EventHook
from operator import itemgetter

from def_generator.decorators import unpack_func_args, unpack_variables




class RespawnController_Avatar(object):
    
    g_redrawVehicleOnRespawn = EventHook()
    
    g_explodeVehicleBeforeRespawn = EventHook()
    
    g_updateRespawnVehicles = EventHook()
    
    g_updateRespawnCooldowns = EventHook()
    
    g_updateRespawnInfo = EventHook()
    
    g_updateVehicleLimits = EventHook()
    
    g_updatePlayerLives = EventHook()
    
    g_onTeamLivesRestored = EventHook()
    
    def __init__(self):
        self.id = None
        self.position = None



        # MRO fix

        self._properties = getattr(self, '_properties', [])
        self._properties.extend([
            
        ])
        # sort properties by size
        self._properties.sort(key=itemgetter(0))

        self._methods = getattr(self, '_methods', [])
        self._methods.extend([
            (10000000000, 'redrawVehicleOnRespawn'),
            (32, 'explodeVehicleBeforeRespawn'),
            (10000000000, 'updateRespawnVehicles'),
            (10000000000, 'updateRespawnCooldowns'),
            (10000000000, 'updateRespawnInfo'),
            (10000000000, 'updateVehicleLimits'),
            (8, 'updatePlayerLives'),
            (10000000000, 'onTeamLivesRestored'),
            
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


    # method size: 10000000000
    @unpack_func_args(['OBJECT_ID', 'STRING', 'STRING'])
    def redrawVehicleOnRespawn(self, arg1, arg2, arg3):
        self.g_redrawVehicleOnRespawn.fire(self, arg1, arg2, arg3)

    # method size: 32
    @unpack_func_args(['OBJECT_ID'])
    def explodeVehicleBeforeRespawn(self, arg1):
        self.g_explodeVehicleBeforeRespawn.fire(self, arg1)

    # method size: 10000000000
    @unpack_func_args([['ARRAY', 'RESPAWN_AVAILABLE_VEHICLE']])
    def updateRespawnVehicles(self, arg1):
        self.g_updateRespawnVehicles.fire(self, arg1)

    # method size: 10000000000
    @unpack_func_args([['ARRAY', 'RESPAWN_COOLDOWN_ITEM']])
    def updateRespawnCooldowns(self, arg1):
        self.g_updateRespawnCooldowns.fire(self, arg1)

    # method size: 10000000000
    @unpack_func_args(['RESPAWN_INFO'])
    def updateRespawnInfo(self, arg1):
        self.g_updateRespawnInfo.fire(self, arg1)

    # method size: 10000000000
    @unpack_func_args([['ARRAY', 'RESPAWN_LIMITED_VEHICLES']])
    def updateVehicleLimits(self, arg1):
        self.g_updateVehicleLimits.fire(self, arg1)

    # method size: 8
    @unpack_func_args(['UINT8'])
    def updatePlayerLives(self, arg1):
        self.g_updatePlayerLives.fire(self, arg1)

    # method size: 10000000000
    @unpack_func_args([['ARRAY', 'UINT8']])
    def onTeamLivesRestored(self, arg1):
        self.g_onTeamLivesRestored.fire(self, arg1)


    ####################################
    #       PROPERTIES
    ####################################



    def __repr__(self):
        d = {}
        for _, p in self._properties:
            d[p] = getattr(self, p)
        return "<{}> {}".format(self.__class__.__name__, d)