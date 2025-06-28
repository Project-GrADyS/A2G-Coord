from A2G_Coord_v3.air_protocol import AirProtocol as AirProtocolv3

from gradysim.protocol.messages.communication import BroadcastMessageCommand
from gradysim.protocol.messages.mobility import GotoCoordsMobilityCommand

from typing import List, Tuple, Dict
import random
import json
import math

class AirProtocol(AirProtocolv3):

    def initialize(self):
        return super().initialize()
    
    def handle_timer(self, timer):
        return super().handle_timer(timer)
    
    def handle_packet(self, message):
        msg = json.loads(message)
        if msg != '':
            if msg["type"] == "base_station_message":
                received_poi = msg["base_station_buffer"]
                reply_msg = {
                    "type": "base_station_response",
                    "collected_poi": self.poi_buffer,
                    "sender_id": self.id
                }
                command = BroadcastMessageCommand(
                    message=json.dumps(reply_msg)
                )
                self.provider.send_communication_command(command)
                for p in received_poi:
                    res = self.check_duplicates(p[0], p[1])
                    if not res:
                        self.sent_pois.append({"sent": False, "id": p[0], "position": p[1]})
        return super().handle_packet(message)
    
    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)
    
    def finish(self):
        return super().finish()