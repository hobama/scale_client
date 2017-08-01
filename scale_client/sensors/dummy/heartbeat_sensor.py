from scale_client.sensors.virtual_sensor import VirtualSensor

import logging
log = logging.getLogger(__name__)


class HeartbeatSensor(VirtualSensor):
    """
    This sensor simply publishes a heartbeat event every sample_interval seconds, which is
    useful for ensuring a remote client is alive and connected to the data exchange.
    """

    def __init__(self, broker, interval=1, **kwargs):
        super(HeartbeatSensor, self).__init__(broker=broker, interval=interval, **kwargs)

    def get_type(self):
        return "heartbeat"

    DEFAULT_PRIORITY = 10

    def read_raw(self):
        return "heartbeat"