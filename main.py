from scripts.core.camera import Camera
from scripts.services.network_service import NetworkService
from scripts.core.motor_driver import MotorDriver
from scripts.services.bluethooth.service import Application
from scripts.services.ble_service import ControllerService, ControllerAdvertisement
     

def main():
    gatt_server = Application()
    motor_driver = MotorDriver()
    gatt_server.add_service(ControllerService(0, motor_driver))
    gatt_server.register()
    
    advertiser = ControllerAdvertisement(0)
    advertiser.register()
    
    try:
        gatt_server.run()
    except KeyboardInterrupt:
        motor_driver.cleanup_gpio()
        gatt_server.quit()
    
    #camera = Camera()
    #networkService = NetworkService()
    #networkService.startSteaming(camera)
    
if __name__ == "__main__":
    main()
