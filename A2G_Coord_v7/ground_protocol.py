from A2G_Coord_v3.ground_protocol import GroundProtocol as GroundProtocolv3

class GroundProtocol(GroundProtocolv3):

    def initialize(self):
        return super().initialize()
    
    def handle_timer(self, timer):
        return super().handle_timer(timer)
    
    def handle_packet(self, message):
        return super().handle_packet(message)
    
    def handle_telemetry(self, telemetry):
        return super().handle_telemetry(telemetry)
    
    def finish(self):
        return super().finish()