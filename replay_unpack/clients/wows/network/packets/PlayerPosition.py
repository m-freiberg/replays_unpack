# modified from https://github.com/Monstrofil/replays_unpack/pull/1/files#diff-ffa52a5cbf1afd02ee7ae0d63f281ccb
#!/usr/bin/python
# coding=utf-8
import struct

from io import StringIO 

from replay_unpack.core.network.types import Vector3
from replay_unpack.core import PrettyPrintObjectMixin


__author__ = "Aleksandr Shyshatsky"


class PlayerPosition(PrettyPrintObjectMixin):
    def __init__(self, stream):
        # type: (StringIO) -> ()

        self.entityId1 = struct.unpack('i', stream.read(4))
        self.entityId2 = struct.unpack('i', stream.read(4))

        self.position = Vector3(stream)
        self.rotation = Vector3(stream)



        pass
