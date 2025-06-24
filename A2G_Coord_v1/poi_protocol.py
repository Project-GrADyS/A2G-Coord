import logging
import random

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.communication import BroadcastMessageCommand, SendMessageCommand
from gradysim.protocol.messages.mobility import GotoCoordsMobilityCommand
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.plugin.random_mobility import RandomMobilityPlugin, RandomMobilityConfig
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration, LoopMission
from gradysim.simulator.extension.communication_controller import CommunicationController

from typing import List, Tuple, Dict
import json


class PoIProtocol(IProtocol):
    sent: int
    id: int

    def initialize(self):
        CommunicationController(self).set_transmission_range(3.0)
        self.sent = 0
        self.id = self.provider.get_id()
        
        self.provider.schedule_timer(
            "message",  
            self.provider.current_time() + 0.5
        )

    def handle_timer(self, timer: str):
        if timer == "message":
            self.sent += 1
            msg = {
                "type": "poi_message",
                "id": self.id
            }
            command = BroadcastMessageCommand(
                message=json.dumps(msg)
            )

            self.provider.send_communication_command(command)

            self.provider.schedule_timer(
                "message",
                self.provider.current_time() + 0.5
            )

    def handle_packet(self, message: str):
        pass

    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        pass
