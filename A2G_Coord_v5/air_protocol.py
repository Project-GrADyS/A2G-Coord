from A2G_Coord_v3.air_protocol import AirProtocol as AirProtocolv3

from gradysim.protocol.messages.communication import BroadcastMessageCommand
from gradysim.protocol.messages.mobility import GotoCoordsMobilityCommand

from typing import List, Tuple, Dict
import random
import json
import math

class AirProtocol(AirProtocolv3):

    next_coordinate_index: int
    num_of_tentatives: int
    is_at_center: bool
    time_interval: int

    def initialize(self):
        self.time_interval = self.provider.get_kwargs().get("time_interval")
        self.encounter_position = [0,0,0]
        self.num_of_tentatives = 2
        self.is_at_center = False
        self.provider.schedule_timer(
            "center",  
            self.provider.current_time() + self.time_interval
        )
        return super().initialize()
    
    def get_encounter_position(self):
        return self.encounter_position[0], self.encounter_position[1], self.encounter_position[2]
    
    def handle_timer(self, timer):
        if timer == "center":
            if not self.is_at_center:
                self.is_at_center = True
                self. next_coordinate_index = self.mission_plan.current_waypoint
                x, y, z = self.get_encounter_position()
                command = GotoCoordsMobilityCommand(x, y, z)
                self.provider.send_mobility_command(command)
            if self.num_of_tentatives > 0:
                self.num_of_tentatives -= 1
                msg = {
                    "type": "uav_rendezvous",
                    "collected_poi": self.poi_buffer,
                    "sender_id": self.id
                }
                command = BroadcastMessageCommand(
                    message=json.dumps(msg)
                )
                self.provider.send_communication_command(command)
                self.provider.schedule_timer(
                    "center",  
                    self.provider.current_time() + 2
                )
            else:
                self.mission_plan.set_current_waypoint(self.next_coordinate_index)
                self.num_of_tentatives = 2
                self.is_at_center = False
                self.provider.schedule_timer(
                    "center",  
                    self.provider.current_time() + self.time_interval
                )
        return super().handle_timer(timer)
    
    def handle_packet(self, message):
        msg = json.loads(message)
        if msg != '':
            if msg["type"] == "uav_rendezvous":
                self.num_of_tentatives = 0
                received_poi = msg["collected_poi"]
                msg = {
                    "type": "uav_rendezvous_response",
                    "collected_poi": self.poi_buffer,
                    "sender_id": self.id
                }
                command = BroadcastMessageCommand(
                    message=json.dumps(msg)
                )
                self.provider.send_communication_command(command)
                for p in received_poi:
                    res = self.check_duplicates(p[0], p[1])
                    if not res:
                        self.sent_pois.append({"sent": False, "id": p[0], "position": p[1]})
            elif msg["type"] == "uav_rendezvous_response":
                received_poi = msg["collected_poi"]
                for p in received_poi:
                    res = self.check_duplicates(p[0], p[1])
                    if not res:
                        self.sent_pois.append({"sent": False, "id": p[0], "position": p[1]})
        return super().handle_packet(message)
    
    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)
    
    def finish(self):
        return super().finish()