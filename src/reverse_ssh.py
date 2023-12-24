import threading
import pexpect
import time

from loguru import logger

class ReverseSSH(threading.Thread):
    def __init__(self,service_name, source_server, source_port, remote_port, remote_server, remote_pw):
        threading.Thread.__init__(self)
        logger.info("Creating Tunnel...")
        self.service_name = service_name
        self.source_port = source_port
        self.source_server = source_server
        self.remote_port = remote_port
        self.remote_server = remote_server
        command = "autossh -o \"StrictHostKeyChecking=no\" -N -T -R {}:{}:{} {}".format(remote_port, source_server, source_port, remote_server)
        logger.info(command)
        self.ssh_tunnel = pexpect.spawn(command)

        patterns = [
            r".* password: $",
            pexpect.EOF,
            pexpect.TIMEOUT,
            ".*"
        ]

        try:
            self.ssh_tunnel.expect(r".* password: $", timeout=2)
            logger.info("Sending password")
            self.ssh_tunnel.sendline(remote_pw)
            # TODO: Handle wrong password etc

        except pexpect.TIMEOUT:
            logger.error("No password prompted")

        except pexpect.EOF:
            logger.error("Process terminated")

        time.sleep(0.1)
        

    
    def run(self):
        
        while True:
            alive = self.ssh_tunnel.isalive()
            # Handle unexpected errors
            if not alive:
                logger.error(f"{self.service_name} is terminating!")
                break
            time.sleep(10)
