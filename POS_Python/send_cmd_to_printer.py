import os
import sys




def send_command_to_printer(cmd):
    print(cmd)
    print(''.join(cmd[1:]))
    print(bytes(''.join(cmd[1:]), "ascii"))
    print(b'\x1d\x56\x66')

    print("echo -e '{}' > /dev/usb/lp0".format(bytes(''.join(cmd[1:]), 'ascii')))
                          
              
    


if __name__ == "__main__":
    send_command_to_printer(sys.argv)


