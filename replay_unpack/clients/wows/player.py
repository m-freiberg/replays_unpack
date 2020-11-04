# coding=utf-8
import logging
import struct
from io import BytesIO

from replay_unpack.core import (
    Entity
)
from replay_unpack.core.network.player import ControlledPlayerBase
from .helper import get_definitions, get_controller
from .network.packets import (
    Map,
    BasePlayerCreate,
    CellPlayerCreate,
    EntityCreate,
    Position,
    EntityMethod,
    EntityProperty,
    NestedProperty,
    EntityEnter,
    EntityLeave,
    PlayerPosition,
    PACKETS_MAPPING
)


class ReplayPlayer(ControlledPlayerBase):

    def _get_definitions(self, version):
        try:
            iter_version = '_'.join(version[:4])
            iter_version = iter_version[:5] + iter_version[-1]
            return get_definitions(iter_version)
        except RuntimeError:
            return get_definitions('_'.join(version[:3]))

    def _get_movements(self):
        return get_movements()

    def _get_health(self):
        return get_health()

    def _get_yaw(self):
        return get_yaw()

    def _get_pitch(self):
        return get_pitch()

    def _get_roll(self):
          return get_roll()

    def _get_gunShots(self):
          return get_gunShots(self)
    
    def _get_atbaGunShots(self):
          return get_atbaGunShots(self)

    def _get_controller(self, version):
        try:
            return get_controller('_'.join(version[:4]))
        except RuntimeError:
            return get_controller('_'.join(version[:3]))

    def _get_packets_mapping(self):
        return PACKETS_MAPPING

    def _process_packet(self, time, packet):
        if isinstance(packet, Map):
            logging.debug('Welcome to map %s: %s', packet.name, packet.arenaId)
            self._battle_controller.map = packet.name

        elif isinstance(packet, BasePlayerCreate):
            # I'm not sure what is the order of cell/base/client player creation
            if packet.entityId in self._battle_controller.entities:
                base_player = self._battle_controller.entities[packet.entityId]
            else:
                base_player = Entity(id_=packet.entityId,
                                     spec=self._definitions.get_entity_def_by_name('Avatar'))

            # base is internal, so props are stored in order of xml file
            io = BytesIO(packet.value.value)
            for index, prop in enumerate(base_player.base_properties):
                base_player.set_base_property(index, io)

            self._battle_controller.create_entity(base_player)
            self._battle_controller.on_player_enter_world(packet.entityId)

        elif isinstance(packet, CellPlayerCreate):
            # I'm not sure what is the order of cell/base/client player creation
            if packet.entityId in self._battle_controller.entities:
                cell_player = self._battle_controller.entities[packet.entityId]
            else:
                cell_player = Entity(id_=packet.entityId,
                                     spec=self._definitions.get_entity_def_by_name('Avatar'))

            # cell is internal, so props are stored in order of xml file
            io = packet.value.io()
            for index, prop in enumerate(cell_player.client_properties_internal):
                cell_player.set_client_property_internal(index, io)
            # TODO: why this assert fails?
            # assert io.read() == b''
            self._battle_controller.create_entity(cell_player)

        elif isinstance(packet, EntityEnter):
            self._battle_controller.entities[packet.entityId].is_in_aoi = True

        elif isinstance(packet, EntityLeave):
            self._battle_controller.entities[packet.entityId].is_in_aoi = False

        elif isinstance(packet, EntityCreate):
            entity = Entity(
                id_=packet.entityID,
                spec=self._definitions.get_entity_def_by_index(packet.type))

            values = packet.state.io()
            values_count, = struct.unpack('B', values.read(1))
            for i in range(values_count):
                k = values.read(1)
                idx, = struct.unpack('B', k)
                entity.set_client_property(idx, values)
            assert values.read() == b''
            self._battle_controller.create_entity(entity)

        elif isinstance(packet, PlayerPosition):
            # modified from https://github.com/Monstrofil/replays_unpack/pull/1/files#diff-ffa52a5cbf1afd02ee7ae0d63f281ccb
            try:
                if packet.entityId1 != (0,) and packet.entityId2 == (0,) and str(self._battle_controller.entities[packet.entityId1[0]])[0:7] == 'Vehicle':
                    if packet.entityId1[0] in self._movements: self._movements[packet.entityId1[0]].append((packet.position.x, packet.position.z, time))
                    else: self._movements[packet.entityId1[0]] = [(packet.position.x, packet.position.z, time)]         
            
                    if packet.entityId1[0] in self._health: self._health[packet.entityId1[0]].append(self._battle_controller.entities[packet.entityId1[0]].properties['client']['health'])
                    else: self._health[packet.entityId1[0]] = [self._battle_controller.entities[packet.entityId1[0]].properties['client']['health']]

                    # print(packet.rotation)
                    if packet.entityId1[0] in self._yaw: self._yaw[packet.entityId1[0]].append(packet.rotation.x)
                    else: self._yaw[packet.entityId1[0]] = [packet.rotation.x]
                        
                    if packet.entityId1[0] in self._roll: self._roll[packet.entityId1[0]].append(packet.rotation.z)
                    else: self._roll[packet.entityId1[0]] = [packet.rotation.z]

                    if packet.entityId1[0] in self._pitch: self._pitch[packet.entityId1[0]].append(packet.rotation.y)
                    else: self._pitch[packet.entityId1[0]] = [packet.rotation.y]            

            except KeyError as e:
                # entity not yet created
                pass
                
        elif isinstance(packet, Position):
            entity = self._battle_controller.entities[packet.entityId]
            try:
                if packet.entityId in self._movements: self._movements[packet.entityId].append((packet.position.x, packet.position.z, time))
                else: self._movements[packet.entityId] = [(packet.position.x, packet.position.z, time)]
            except:
                if packet.entityId in self._movements: self._movements[packet.entityId].append((packet.position[0], packet.position[2], time))
                else: self._movements[packet.entityId] = [(packet.position[0], packet.position[2], time)]

            if packet.entityId in self._health: self._health[packet.entityId].append(entity.properties['client']['health'])
            else: self._health[packet.entityId] = [entity.properties['client']['health']]
            
            if packet.entityId in self._yaw: self._yaw[packet.entityId].append(packet.yaw)
            else: self._yaw[packet.entityId] = [packet.yaw]

            if packet.entityId in self._roll: self._roll[packet.entityId].append(packet.roll)
            else: self._roll[packet.entityId] = [packet.roll]
            
            if packet.entityId in self._pitch: self._pitch[packet.entityId].append(packet.pitch)
            else: self._pitch[packet.entityId] = [packet.pitch]
            



            self._battle_controller.entities[packet.entityId].position = packet.position
            self._battle_controller.entities[packet.entityId].yaw = packet.yaw
            self._battle_controller.entities[packet.entityId].pitch = packet.pitch
            self._battle_controller.entities[packet.entityId].roll = packet.roll

        elif isinstance(packet, EntityMethod):
            entity = self._battle_controller.entities[packet.entityId]
            entity.call_client_method(packet.messageId, packet.data.io())

            if packet.messageId == 13:  #shootATBAGuns
              if packet.entityId in self._atbaGunShots: self._atbaGunShots[packet.entityId].append(time)
              else: self._atbaGunShots[packet.entityId] = [time]
            elif packet.messageId == 11:  # shootGuns
              if packet.entityId in self._gunShots: self._gunShots[packet.entityId].append(time)
              else: self._gunShots[packet.entityId] = [time]
              
            # print('{}: {}'.format(packet.messageId, entity._methods[packet.messageId]))

        elif isinstance(packet, EntityProperty):
            entity = self._battle_controller.entities[packet.objectID]
            entity.set_client_property(packet.messageId, packet.data.io())

        elif isinstance(packet, NestedProperty):
            e = self._battle_controller.entities[packet.entity_id]

            logging.debug('')
            logging.debug('nested property request for id=%s isSlice=%s packet=%s',
                          e.id, packet.is_slice, packet.payload.hex())
            packet.read_and_apply(e)
