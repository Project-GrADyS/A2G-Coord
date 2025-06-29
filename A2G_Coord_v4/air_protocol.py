'''
from A2G_Coord_v1.air_protocol import AirProtocol as AirProtocolv1

from gradysim.protocol.messages.communication import BroadcastMessageCommand

from typing import List, Tuple, Dict
import json
import math
from itertools import groupby

class AirProtocol(AirProtocolv1):

    sent_pois: List[Dict]
    sent_pois_grouped: List[Dict]
    section: int

    def initialize(self):
        self.sent_pois = []
        self.sent_pois_grouped = []
        self.section = 0
        return super().initialize()
    
    def handle_timer(self, timer):
        return super().handle_timer(timer)
    
    def handle_packet(self, message):
        msg = json.loads(message)
        if msg != '':
            if msg["type"] == "poi_message":
                pos = self.position
                section = self.section
                res = self.check_duplicates(msg["id"], pos)
                if not res:
                    self.sent_pois.append({"sent": False, "id": msg["id"], "position": pos, "section": section})
                    self.sent_pois.sort(key=lambda x: x['section'])
                    self.sent_pois_grouped = groupby(self.sent_pois, key=lambda x: x['section'])
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
            elif "base_station_message":
                self.section += 1
    
    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)
    
    def finish(self):
        return super().finish()
'''

from A2G_Coord_v1.air_protocol import AirProtocol as AirProtocolv1
from gradysim.protocol.messages.communication import BroadcastMessageCommand
from typing import List, Tuple, Dict
import json
import math
from itertools import groupby

class AirProtocol(AirProtocolv1):

    sent_pois: List[Dict]
    sent_sections: List[int]
    section: int

    def initialize(self):
        self.sent_pois = []
        self.sent_sections = [] 
        self.grouped_pois_section = {}
        self.section = 0
        return super().initialize()

    def handle_timer(self, timer):
        return super().handle_timer(timer)

    def handle_packet(self, message):
        msg = json.loads(message)
        if msg == '':
            return

        if msg["type"] == "poi_message":
            pos = self.position
            section = self.section
            if not self.check_duplicates(msg["id"], pos):
                poi = {"sent": False, "id": msg["id"], "position": pos, "section": section}
                self.sent_pois.append(poi)
                self.sent_pois.sort(key=lambda x: x['section'])
                if section not in self.grouped_pois_section:
                    self.grouped_pois_section[section] = []
                self.grouped_pois_section[section].append(poi)
                print(self.grouped_pois_section)
                print('\n')
            self.received_poi += 1

        elif msg["type"] == "uav_message":
            if self.sent_pois:
                section_to_pois = {
                    section: [poi for poi in pois if not poi["sent"]]
                    for section, pois in self.grouped_pois_section.items()
                    if section not in self.sent_sections
                }

                section_to_pois = {k: v for k, v in section_to_pois.items() if v}

                if section_to_pois:
                    uav_pos = self.position
                    closest_section = None
                    min_dist = float("inf")

                    for section, pois in section_to_pois.items():
                        if section in self.sent_sections:
                            continue
                        ref_point = pois[0]["position"]
                        dist = self.calculate_distance(uav_pos, ref_point)
                        if dist < min_dist:
                            min_dist = dist
                            closest_section = section

                    if closest_section is not None:
                        selected_pois = section_to_pois[closest_section]
                        pos_list = []
                        uav_x, uav_y = uav_pos[0], uav_pos[1]

                        for s in selected_pois:
                            s["sent"] = True
                            sx, sy, sz = s["position"]
                            pos = self.calculate_direction(sx, sy, sz, self.length, uav_x, uav_y)
                            uav_x, uav_y = pos[0], pos[1]
                            pos_list.append([s["id"], pos])

                        self.sent_sections.append(closest_section)
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
        elif msg["type"] == "base_station_message":
                self.section += 1
                reply_msg = {
                    "type": "base_station_response",
                    "id": self.id
                }
                command = BroadcastMessageCommand(
                    message=json.dumps(reply_msg)
                )
                self.provider.send_communication_command(command)

    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)

    def finish(self):
        return super().finish()

    def calculate_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def check_duplicates(self, poi_id, pos):
        return any(poi for poi in self.sent_pois if poi["id"] == poi_id)
