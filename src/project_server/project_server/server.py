import sys
import socket

from project_communication.srv import GetProcessTime
import rclpy
from rclpy.node import Node
import xml.etree.ElementTree as ET
import time

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(GetProcessTime, 'get_process_time')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        self.req = GetProcessTime.Request()

        #Init TCP/IP connection
        # specify Host and Port 
        #Listen to all incoming requests by setting host to be empty
        HOST = '' 
        PORT = 33333

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # With the help of bind() function 
            # binding host and port
            soc.bind((HOST, PORT))
        
        except socket.error as message:
            
            # if any error occurs then with the 
            # help of sys.exit() exit from the program
            print('Bind failed. Error Code : '
                + str(message[0]) + ' Message '
                + message[1])
            sys.exit()

        # print if Socket binding operation completed    
        print('Socket binding operation completed')
        print('Now listening...')

        # With the help of listening () function
        # starts listening
        soc.listen(1)

        self.conn, address = soc.accept()

        # print the address of connection
        print('Connected with ' + address[0] + ':'+ str(address[1]))


    def send_request(self, a):
        self.req.id = a
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def getData(self):
        return self.conn.recv(2048).decode("utf-8")

    def sendData(self, response):
        time = f"{response}".encode("utf-8")

        self.conn.send(time)


def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()

    parser = ET.XMLParser(encoding="utf-8")

    while rclpy.ok():

        print("\nWaiting to receive Data")
        #Read the up to 32 bits of data, whivh maches the bytestream size from plc
        #uid = minimal_client.getData()
	
        #print("Carrier available")

        while True:
            data = minimal_client.getData()

            if data != '':
                size = int(data[:3])
                print(data)
                break

        
        print(f"\nData received: {data[0:size+3]}")
        
        

        #data = '<?xml version = "1.0"?><station_id><rfid_tag ID="14" /><time DT="DT#1970-01-01-00:00:00" /></station_id>'

        root = ET.fromstring(data[3:size+3], parser = parser)


        id_num = root.find("rfid_tag").get('ID')

        print()
        print(id_num)

        #TODO: Extract id from retrieved data
        #uid = 8
        #uid = extractID(data)

        #TODO: Save data to a log file

        response = minimal_client.send_request(int(id_num))     
        #print("before spin")
        #rclpy.spin_once(minimal_client) 
        #print("after spin")


        minimal_client.sendData(f"T#{response.time}ms") #response)

        #time.sleep(2)
        print(f"data sent: {response.time}")

        


    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
