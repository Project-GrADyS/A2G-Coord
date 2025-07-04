from A2G_Coord_v1.air_protocol import AirProtocol as AirProtocolv1

from gradysim.protocol.messages.communication import BroadcastMessageCommand

from typing import List, Tuple, Dict
import json
import math

class AirProtocol(AirProtocolv1):

    sent_pois: List[Dict]

    def initialize(self):
        self.sent_pois = []
        return super().initialize()
    
    def handle_timer(self, timer):
        return super().handle_timer(timer)
    
    def handle_packet(self, message):
        msg = json.loads(message)
        if msg != '':
            if msg["type"] == "poi_message":
                pos = self.position
                res = self.check_duplicates(msg["id"], pos)
                if not res:
                    self.sent_pois.append({"sent": False, "id": msg["id"], "position": pos})
                self.received_poi += 1
            elif msg["type"] == "uav_message":
                if self.sent_pois != []:
                    pos_list = []
                    uav_x = self.position[0]
                    uav_y = self.position[1]

                    for s in self.sent_pois:
                        if not s["sent"]:
                            s["sent"] = True
                            sx, sy, sz = s["position"]
                            pos = self.calculate_direction(sx, sy, sz, self.length, uav_x, uav_y)
                            uav_x = pos[0]
                            uav_y = pos[1]
                            pos_list.append([s["id"], pos])
                    pos_list.append([-1, (0,0,7)])
                    self.received_ugv += 1
                    reply_msg = {
                        "type": "poi_direction",
                        "directions": pos_list,
                    }
                    command = BroadcastMessageCommand(
                        message=json.dumps(reply_msg)
                    )
                    self.provider.send_communication_command(command)
                    self.ugv_db.append(msg["id"])
    
    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)
    
    def finish(self):
        return super().finish()