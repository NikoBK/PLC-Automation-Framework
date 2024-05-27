import sys
import socket

from project_communication.srv import GetProcessTime
import rclpy
from rclpy.node import Node
import xml.etree.ElementTree as ET
import time


class MinimalClientAsync(Node):

    def __init__(self):
        #Initialise ROS and create the node
        super().__init__('minimal_client_async')

        #Initialise the client object, which call the service with process times
        self.cli = self.create_client(GetProcessTime, 'get_process_time')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        #Create service variable type
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
        # starts listening to incoming connections
        soc.listen(1)

        #Accept the incoming request
        self.conn, address = soc.accept()

        # print the address of connection
        print('Connected with ' + address[0] + ':'+ str(address[1]))


    def send_request(self, a):
        self.req.id = a

        #Sends request to service
        self.future = self.cli.call_async(self.req)

        #Update the values
        rclpy.spin_until_future_complete(self, self.future)

        return self.future.result()

    #Receive data from socket connection
    def getData(self):
        return self.conn.recv(2048).decode("utf-8")

    #Send data through socket connection
    def sendData(self, response):
        time = f"{response}".encode("utf-8")

        self.conn.send(time)


def main(args=None):
    rclpy.init(args=args)

    #Create client object
    minimal_client = MinimalClientAsync()

    #Create XML parser object
    parser = ET.XMLParser(encoding="utf-8")

    while rclpy.ok():

        print("\nWaiting to receive Data")

        #Loop until valid data is received
        while True:
            data = minimal_client.getData()

            if data != '':
                #Read the size of the incoming message
                size = int(data[:3])
                print(data)
                break

        
        print(f"\nData received: {data[0:size+3]}")
        
        #Expected data format to receive from PLC
        #data = '<?xml version = "1.0"?><station_id><rfid_tag ID="14" /><time DT="DT#1970-01-01-00:00:00" /></station_id>'

        #Create XML string parser object
        root = ET.fromstring(data[3:size+3], parser = parser)

        #Search XML string for the RFID tag
        id_num = root.find("rfid_tag").get('ID')

        print()
        print(id_num)

        #Request service to to give process time for given tag number
        response = minimal_client.send_request(int(id_num))    

        #Send the process time to the PLC
        minimal_client.sendData(f"T#{response.time}ms") #response)

        print(f"data sent: {response.time}")

        

    #Close the program
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
