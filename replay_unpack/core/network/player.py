#!/usr/bin/python
# coding=utf-8
import logging
from abc import ABC
from io import BytesIO

from .net_packet import NetPacket


class PlayerBase:
    def __init__(self, version: str):
        self._definitions = self._get_definitions(version)

        self._mapping = self._get_packets_mapping()

    def _get_definitions(self, version):
        raise NotImplementedError

    def _get_packets_mapping(self):
        raise NotImplementedError

    def _deserialize_packet(self, packet: NetPacket):
        if packet.type in self._mapping:
            return self._mapping[packet.type](packet.raw_data)
        logging.info('unknown packet %s', hex(packet.type))
        return None

    def _process_packet(self, time, packet):
        raise NotImplementedError

    def play(self, replay_data, strict_mode=False):
        io = BytesIO(replay_data)
        while io.tell() != len(replay_data):
            packet = NetPacket(io)
            try:
                self._process_packet(packet.time, self._deserialize_packet(packet))
            except Exception:
                logging.exception("Problem with packet %s:%s:%s",
                                  packet.time, packet.type, self._mapping.get(packet.type))
                if strict_mode:
                    raise


class ControlledPlayerBase(PlayerBase, ABC):
    def __init__(self, version: str):
        self._battle_controller = self._get_controller(version)
        self._movements = {}
        self._health = {}
        self._yaw = {}
        self._pitch = {}
        self._roll = {}
        self._gunShots = {}
        self._atbaGunShots = {}
        super(ControlledPlayerBase, self).__init__(version)

    def _get_controller(self, version):
        raise NotImplementedError

    def get_info(self):
        return self._battle_controller.get_info()

    def get_movements(self):
        return self._movements    
    
    def get_health(self):
        return self._health

    def get_yaw(self):
        return self._yaw

    def get_pitch(self):
        return self._pitch

    def get_roll(self):
        return self._roll

    def get_gunShots(self):
        return self._gunShots

    def get_atbaGunShots(self):
        return self._atbaGunShots
