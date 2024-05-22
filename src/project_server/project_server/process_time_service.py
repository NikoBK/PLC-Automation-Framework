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

        #TODO: Setup code to read excel file with processing time and save to array
        #time_tables = getDataFromExcel("pathToFile")
        #data = pd.read_excel(".xlsx")

        self.time_tables = []
        workstationID = 14

        with open('procssing_times_table.csv', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=';', quotechar='|')

            for row in data:
                self.time_tables.append(row[workstationID])  # Extract the 14th column (index 13)

        #print(time_tables_2)

        #Temporary solution idx = id-1
        #self.time_tables = [1618, 5428, 3236, 1296, 1542, 2774, 3710, 4230, 1910, 4620, 5437, 4127, 4989, 2529, 1820, 2111]

    def get_time_callback(self, request, response):

        response.time = int(self.time_tables[request.id])
        self.get_logger().info('Incoming request id\na: %d' % (request.id))

        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
