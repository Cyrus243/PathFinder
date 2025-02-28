import dbus

from .bluethooth.advertisement import Advertisement
from .bluethooth.service import Service, Characteristic, Descriptor
from scripts.core.motor_driver import MotorDriver
#from gpiozero import CPUTemperature  - il servira quand il faudra construire le dashboard
from constants import GATT_CHRC_IFACE, NOTIFY_TIMEOUT
from constants import JOYSTICK_COMMAND_ID
import math


class ControllerAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Controller")
        self.include_tx_power = True
        
class ControllerService(Service):
    CONTROLLER_SVC_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, index, motor_driver):
        Service.__init__(self, index, self.CONTROLLER_SVC_UUID, True)
        self.add_characteristic(ControllerCharacteristic(self, motor_driver))
 

class ControllerCharacteristic(Characteristic):
    CONTROLLER_CHARACTERISTIC_UUID = "00000002-710e-4a5b-8d75-3e5b444bc3cf"
    
    def __init__(self, service, motor_driver):
        Characteristic.__init__(self, self.CONTROLLER_CHARACTERISTIC_UUID,["read", "write"], service)
        self.add_descriptor(ControllerDescriptor(self))
        self.motor_driver = motor_driver
        
    def ReadValue(self, options):
        """Retourne l'état du moteur (ON ou OFF)"""
        
    def WriteValue(self, value, options):
        """Reçoit une commande en BLE et active/désactive le moteur après filtrage."""
        try:
            data = list(value)
            data = [int(byte) for byte in data]
            command_type = "".join(str(x) for x in data[1:5])

            if command_type == JOYSTICK_COMMAND_ID:
                angle = (data[6] >> 3)*15
                radius = data[6] & 0x07
                
                x_value = radius*(float(math.cos(float(angle*math.pi/180))))
                y_value = radius*(float(math.sin(float(angle*math.pi/180))))
                
                self.motor_driver.run(x_value, y_value)
            
        except Exception as e:
            print(f"interpreter exception: {e}")
            

        
class ControllerDescriptor(Descriptor):
    CONTROLLER_DESCRIPTOR_UUID = "2901"
    CONTROLLER_DESCRIPTOR_VALUE = "ROVER DVR CONTROL"
    
    def __init__(self, characteristic):
        Descriptor.__init__(self, self.CONTROLLER_DESCRIPTOR_UUID,["write"], characteristic)
        
    def ReadValue(self, options):
        value = []
        desc = self.CONTROLLER_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value