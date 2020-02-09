import requests
import time

URL = 'https://botcontroller-267620.appspot.com/commands/'
UUID = "something"

if __name__=="__main__":
    sequence_counter = 0
    while True:
        cmd_str = requests.get(URL + UUID)
        cmds = [cmd.split(",") for cmd in cmd_str.split("\n")]
        
        last_seq_num = int(cmds[-1][0])
        if last_seq_num > sequence_counter:
            new_cmds = cmds[sequence_counter - last_seq_num : ]
            sequence_counter = last_seq_num


        time.sleep(.05)