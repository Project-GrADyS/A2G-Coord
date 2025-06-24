import logging
import random

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.communication import BroadcastMessageCommand
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.simulator.extension.communication_controller import CommunicationController

from typing import List, Tuple, Dict
import json


class BaseStationProtocol(IProtocol):
    id: int
    msg_timer: int
    base_station_buffer: List[Tuple]

    def initialize(self):
        self.base_station_buffer = []
        self.msg_timer = 1
        CommunicationController(self).set_transmission_range(3.0)
        self.id = self.provider.get_id()
        
        self.provider.schedule_timer(
            "message",  
            self.provider.current_time() + self.msg_timer
        )

    def handle_timer(self, timer: str):
        if timer == "message":
            msg = {
                "type": "base_station_message",
                "id": self.id,
            }
            command = BroadcastMessageCommand(
                message=json.dumps(msg)
            )
            self.provider.send_communication_command(command)
            self.provider.schedule_timer(
                "message",
                self.provider.current_time() + self.msg_timer
            )
        elif timer == "interval":
            self.msg_timer = 1

    def handle_packet(self, message: str):
        msg = json.loads(message)
        if msg == '':
            return
        if msg["type"] == "base_station_response":
            self.msg_timer = 10
            self.provider.schedule_timer(
                "interval",
                self.provider.current_time() + 5
            )

    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        pass
