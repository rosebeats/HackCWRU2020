import requests
import time
import control

URL = 'https://botcontroller-267620.appspot.com/commands/'
UUID = "2adb80d2-5e2d-4c8f-9558-2aeb8f307077"

robot = control.get_robot(control.LEFT_DIR, control.RIGHT_DIR, control.LEFT_PWM, control.RIGHT_PWM)

if __name__=="__main__":
    requests.delete(URL + UUID)
    sequence_counter = 0
    while True:
        cmd_response = requests.get(URL + UUID)
        if cmd_response.ok:
            cmd_str = cmd_response.text
            cmds = [cmd.split(",") for cmd in cmd_str.split("\n")][:-1]
            
            last_seq_num = int(cmds[-1][0])
            if last_seq_num > sequence_counter:
                new_cmds = cmds[sequence_counter - last_seq_num : ]
                print(new_cmds)
                for cmd in new_cmds:
                    control.exec_command(cmd[1], robot)
                sequence_counter = last_seq_num

        time.sleep(.05)