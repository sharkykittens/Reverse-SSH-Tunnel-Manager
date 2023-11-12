
import time
import threading
import pexpect
import pywebio
import pywebio.output as webout
import pywebio.input as webin
import pywebio.session as websession
import pywebio.pin as webpin

from dotenv import load_dotenv
from pywebio.platform.fastapi import start_server
from reverse_ssh import ReverseSSH

class Webapp:

    def __init__(self):
        load_dotenv()
        self.create_tunnel_scope = "create_tunnel"
        self.display_tunnels_scope = "display_tunnel"
        self.tunnels = []

    
    def start_app(self, port):

        start_server(self.main_page, port=port)


    def refresh_list(self):
        
        while True:
            time.sleep(5)

            #self.tunnels = [tunnel for tunnel in self.tunnels if tunnel.is_alive()]

            # Display the tunnels
            table_content = [[f"{tunnel.service_name}",
                              f"{tunnel.source_server}:{tunnel.source_port}",
                              f"{tunnel.remote_server}:{tunnel.remote_port}"] for tunnel in self.tunnels]
            
            with webout.use_scope(self.display_tunnels_scope):
                webout.clear(self.display_tunnels_scope)
                webout.put_table(header=["Service Name","Forwarding Service","Forwarded To"],tdata=table_content)
                

    def main_page(self):
        
        webout.put_scope(self.display_tunnels_scope)

        with webout.use_scope(self.display_tunnels_scope):
            webout.put_table(header=["Service Name","Forwarding Service","Forwarded To"],tdata=[])

        refresh_thread = threading.Thread(target=self.refresh_list)
        pywebio.session.register_thread(refresh_thread)
        refresh_thread.start()

        webout.put_scope(self.create_tunnel_scope)

        with webout.use_scope(self.create_tunnel_scope):

            def create_tunnel():

                tunnel = ReverseSSH(
                    service_name=webpin.pin.service_name,
                    source_server=webpin.pin.source_server,
                    source_port=webpin.pin.source_port,
                    remote_server=webpin.pin.target_server,
                    remote_port=webpin.pin.target_port,
                    remote_pw=webpin.pin.target_password
                )
                tunnel.daemon = True
                tunnel.start()
                
                self.tunnels.append(tunnel)


            webout.put_text("Create New Reverse Tunnel")
            webpin.put_input(name="service_name", label="Service Name")
            webpin.put_input(name="source_server",label="Source Server")
            webpin.put_input(name="source_port",type="number", label="Source Port")
            webpin.put_input(name="target_server", label="Target Server", help_text="The target server to forward to, eg: user@1.2.3.4")
            webpin.put_input(name="target_port",type="number",label="Target Port")
            webpin.put_input(name="target_password",type="password", label="Target Password")
            webout.put_button("Create",onclick=create_tunnel)





if __name__=="__main__":

    app = Webapp()
    app.start_app(15000)
