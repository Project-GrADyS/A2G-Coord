from A2G_Coord_v1.air_protocol import AirProtocol as AirProtocolv1

from gradysim.protocol.messages.communication import BroadcastMessageCommand
from gradysim.protocol.messages.mobility import GotoCoordsMobilityCommand

from typing import List, Tuple, Dict
import random
import json
import math

class AirProtocol(AirProtocolv1):

    next_coordinate_index: int
    num_of_tentatives: int
    is_at_center: bool

    def initialize(self):
        self.num_of_tentatives = 2
        self.is_at_center = False
        self.provider.schedule_timer(
            "center",  
            self.provider.current_time() + 200
        )
        return super().initialize()
    
    def handle_timer(self, timer):
        if timer == "center":
            if not self.is_at_center:
                self.is_at_center = True
                self. next_coordinate_index = self.mission_plan.current_waypoint
                command = GotoCoordsMobilityCommand(0,0,0)
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
                    self.provider.current_time() + 5
                )
            else:
                self.mission_plan.set_current_waypoint(self.next_coordinate_index)
                self.num_of_tentatives = 2
                self.is_at_center = False
                self.provider.schedule_timer(
                    "center",  
                    self.provider.current_time() + 200
                )
        return super().handle_timer(timer)
    
    def handle_packet(self, message):
        msg = json.loads(message)
        if msg != '':
            if msg["type"] == "uav_rendezvous":
                self.num_of_tentatives = 0
                received_poi = msg["collected_poi"]
                # print("\n========UAV RENDEZVOUS=============")
                # print(self.poi_buffer)
                # print(msg["sender_id"])
                for p in received_poi:
                    self.check_duplicates(p[0], p[1])
                # print(self.poi_buffer)
        return super().handle_packet(message)
    
    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)
    
    def finish(self):
        print("=======================")
        print(self.id)
        print(self.poi_buffer)
        print("=======================\n")
        return super().finish()