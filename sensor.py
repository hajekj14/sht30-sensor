import logging
import smbus
import time
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def initialize_sht30():
    """Initialize the SHT30 sensor."""
    bus = smbus.SMBus(1)
    return bus

class SHT30Sensor(Entity):
    """Representation of an SHT30 Sensor."""

    def __init__(self, name, sht30, sensor_type):
        """Initialize the sensor."""
        self._name = name
        self._sht30 = sht30
        self._sensor_type = sensor_type
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._sensor_type == "Celsius":
            return "C"
        elif self._sensor_type == "Humidity":
            return "%"
        return None

    def update(self):
        """Fetch data from the sensor."""

        self._sht30.write_i2c_block_data(0x44, 0x2C, [0x06])
        time.sleep(0.5)
        data = self._sht30.read_i2c_block_data(0x44, 0x00, 6)

        try:
            if self._sensor_type == "Celsius":
                self._state = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
            elif self._sensor_type == "Humidity":
                self._state = 100 * (data[3] * 256 + data[4]) / 65535.0
        except Exception as e:
            _LOGGER.error(f"Error updating {self._name}: {e}")

def setup_platform(hass, config, add_entities, discovery_info=None):
    sht30 = initialize_sht30()
    entities = [
        SHT30Sensor("SHT30 Temperature", sht30, "Celsius"),
        SHT30Sensor("SHT30 Humidity", sht30, "Humidity")
    ]
    add_entities(entities)