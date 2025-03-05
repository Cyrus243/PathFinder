from scripts.core.camera import Camera
from scripts.services.streaming_service import StreamingService
from scripts.services.controller_tcp_service import ControllerWifiServer
from scripts.core.motor_driver import MotorDriver
from scripts.services.bluethooth.service import Application
from scripts.services.ble_service import ControllerService, ControllerAdvertisement

def launch_ble_server():
    gatt_server = Application()
    motor_driver = MotorDriver()
    gatt_server.add_service(ControllerWifiServer(0, motor_driver))
    gatt_server.register()
    
    advertiser = ControllerAdvertisement(0)
    advertiser.register()
    
    try:
        gatt_server.run()
    except KeyboardInterrupt:
        motor_driver.cleanup_gpio()
        gatt_server.quit()
     

def main():
    motor_driver = MotorDriver()
    controller_server = ControllerWifiServer(motor_driver)
    controller_server.run()
    
    motor_driver.cleanup_gpio()
    
    #camera = Camera()
    #networkService = NetworkService()
    #networkService.startSteaming(camera)
    
if __name__ == "__main__":
    main()
