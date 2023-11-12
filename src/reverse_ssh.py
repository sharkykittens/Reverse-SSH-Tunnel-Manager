import threading
import pexpect
import time



class ReverseSSH(threading.Thread):
    def __init__(self,service_name, source_server, source_port, remote_port, remote_server, remote_pw):
        threading.Thread.__init__(self)
        self.service_name = service_name
        self.source_port = source_port
        self.source_server = source_server
        self.remote_port = remote_port
        self.remote_server = remote_server
        self.ssh_tunnel = pexpect.spawn("ssh -N -T -R {}:{}:{} {}".format(source_port, source_server, remote_port, remote_server))

        try:
            self.ssh_tunnel.expect("{}'s password: ".format(remote_server), timeout=2)
            self.ssh_tunnel.sendline(remote_pw)
        except pexpect.TIMEOUT:
            print("No password prompted")

        except pexpect.EOF:
            print("Process terminated")

        time.sleep(0.1)
        

    
    def run(self):
        
        while True:
            alive = self.ssh_tunnel.isalive()
            # Handle unexpected errors
            if not alive:
                print(f"{self.service_name} is terminating!")
                break
            time.sleep(10)
