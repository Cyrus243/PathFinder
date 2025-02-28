import lgpio

# Define GPIO pins for motor control
# PWM pins
DVR_1_MOTOR_PWM = 12  
DVR_2_MOTOR_PWM = 13

# Direction pins
# Those are on the driver 1 (left motors)
MOTOR_A_IN1 = 17  
MOTOR_A_IN2 = 27  
MOTOR_B_IN1 = 22
MOTOR_B_IN2 = 23

# Those are on the driver 2 (right motors)
MOTOR_C_IN1 = 24
MOTOR_C_IN2 = 25
MOTOR_D_IN1 = 26
MOTOR_D_IN2 = 16


PWM_FREQUENCY = 500  # 1 kHz PWM frequency

class MotorDriver():
    handle = None
    
    def __init__(self):
        self.setup_gpio()
    
    def setup_gpio(self):
        self.handle = lgpio.gpiochip_open(0)

        # Set DVRs PWM
        lgpio.gpio_claim_output(self.handle, DVR_1_MOTOR_PWM)
        lgpio.gpio_claim_output(self.handle, DVR_2_MOTOR_PWM)
        
        # Set driver 1 motors pins as output
        lgpio.gpio_claim_output(self.handle, MOTOR_A_IN1)
        lgpio.gpio_claim_output(self.handle, MOTOR_A_IN2)
        lgpio.gpio_claim_output(self.handle, MOTOR_B_IN1)
        lgpio.gpio_claim_output(self.handle, MOTOR_B_IN2)
        
        # Set driver 1 motors pins as output
        lgpio.gpio_claim_output(self.handle, MOTOR_C_IN1)
        lgpio.gpio_claim_output(self.handle, MOTOR_C_IN2)
        lgpio.gpio_claim_output(self.handle, MOTOR_D_IN1)
        lgpio.gpio_claim_output(self.handle, MOTOR_D_IN2)

        # Initialize motor state
        lgpio.tx_pwm(self.handle, DVR_1_MOTOR_PWM, PWM_FREQUENCY, 0)
        lgpio.tx_pwm(self.handle, DVR_2_MOTOR_PWM, PWM_FREQUENCY, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 0)
    
    def go_forward(self):
        #Note that front motors are positionned backward
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 1)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 1)
        
    def go_backward(self):
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 1)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 1)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 0)
    
    def stop(self):
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 0)
        
    def left_in_place_rotation(self):
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 1)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 1)
    
    def right_in_place_rotation(self):
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 1)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 1)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 1)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 0)
        
    def run(self, x, y):
        if (y > 0):
            self.go_forward()
        elif (y < 0):
            self.go_backward()
        else: 
            self.stop()
        self.set_motor_speed(x, y)
        
    def set_motor_speed(self, x, y):
        max_speed = 90
        max_xy = 7
        
        left_speed = (y/max_xy)*max_speed + (x/max_xy)*max_speed
        right_speed = (y/max_xy)*max_speed - (x/max_xy)*max_speed

        # Speed Normalisation
        max_val = max(abs(left_speed), abs(right_speed), max_speed)
        if max_val > max_speed:
            left_speed = (left_speed / max_val) * max_speed
            right_speed = (right_speed / max_val) * max_speed
        
        # Set PWM duty cycle (0 to 100)
        lgpio.tx_pwm(self.handle, DVR_1_MOTOR_PWM, PWM_FREQUENCY, abs(left_speed))
        lgpio.tx_pwm(self.handle, DVR_2_MOTOR_PWM, PWM_FREQUENCY, abs(right_speed))
        
    def cleanup_gpio(self):
        if not self.handle:
            print("The handle has not been detected")
            return
        
        lgpio.tx_pwm(self.handle, DVR_1_MOTOR_PWM, PWM_FREQUENCY, 0)
        lgpio.tx_pwm(self.handle, DVR_2_MOTOR_PWM, PWM_FREQUENCY, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_A_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_A_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_B_IN2, 0)
        
        lgpio.gpio_write(self.handle, MOTOR_C_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_C_IN2, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN1, 0)
        lgpio.gpio_write(self.handle, MOTOR_D_IN2, 0)
        
        lgpio.gpiochip_close(self.handle)