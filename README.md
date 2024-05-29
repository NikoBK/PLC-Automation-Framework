# PLC Networking
This repository is a mini project from Software & Automation Frameworks on Aalborg University's robottechnology bachelor, fourth semester.

## Scope & Requirements
The requirements for this repository and the project in general is as to write:
- A PLC program (TCP client) that controls the physical system
- A PC program (TCP server) that monitors the behavior of the physical system.

A free selection of programming language is given for this project.
The code that is to be written for this project must be able to:

- Read the pallet RFID tag when a pallet moves to the module you are working on
- Send the RFID info to a PC via TCP/IP as an XML-encoded string
- The PC program shall decode the information and display the relevant information on
screen during program execution. NOTE: The visualization shall be done by a ROS2 Node!
- The PC program shall return an estimated processing time to the PLC via TCP/IP
- The PLC shall simulate the physical processing time by letting the pallet wait for the
returned time.
- The decoded data shall be stored in a file on the PC, so that it can be analyzed later.

## Authors
This repository was written by group 463 on AAU robotics, on the fourth semester in spring, class of 2024.
