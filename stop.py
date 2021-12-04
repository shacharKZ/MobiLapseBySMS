import motor
import car_dir as dir
import video_dir as vid
import QTR_8RC as ir

motor.setup_motor()
dir.setup_direction()
vid.setup_vid()
vid.home_x_y()
motor.stop()
dir.home()
ir.setup_IR()
