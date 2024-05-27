#Import service description from another ros package
from project_communication.srv import GetProcessTime

import rclpy
import csv
import pandas as pd
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(GetProcessTime, 'get_process_time', self.get_time_callback)
        self.get_logger().info('Service started. Now listening...')

        self.time_tables = []
        workstationID = 14

        #Retrieve process times from the csv file and save as a python list
        with open('procssing_times_table.csv', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=';', quotechar='|')

            for row in data:
                self.time_tables.append(row[workstationID])  # Extract the 14th column (index 13)


    def get_time_callback(self, request, response):
        #Set time attribute according to carrier ID
        response.time = int(self.time_tables[request.id])
        self.get_logger().info('Incoming request id\na: %d' % (request.id))

        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    #Ensures that the minimal service keeps listening to incoming requests
    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
