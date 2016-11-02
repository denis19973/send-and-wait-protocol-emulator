# send-and-wait-protocol-emulator

Project contains implementation of a basic send-and-wait protocol simulator.
The protocol will be half-duplex and will use sliding windows to send multiple packets between two hosts on a LAN with an “unreliable network” between the two hosts.

**Model**:
```
  Transmitter --> Network Emulator  -->  Receiver	
  192.168.0.2 <--   192.168.0.3     <-- 192.168.0.1
```

**Note:** The arrows depict the data flow.

The protocol will also have an ARQ (Automatic Repeat Request) component to it where if a corrupt packet is detected, the receiver will automatically request the transmitter to resend the packet.

## Project Requirements

- Design an application layer protocol on top of either TCP or UDP. The protocol should be able to handle network errors such as packet loss and duplicate packets. Also implement timeouts and ACKs to handle retransmissions due to lost packets (ARQ).

- The network emulator will act as an unreliable channel over which the packets will be sent which means that the transmitter will send packets to the network emulator which in turn will forward them to the receiver. The receiver in turn will send ACKs back to the transmitter via the network emulator.

- The implementation of the network emulator should include a "noise" component which will randomly discard packets (and ACKs as well) to achieve a specified bit error rate.

- One side will be allowed to acquire the channel first and send all of its packets. An EOT (End Of Transmission) packet will indicate that it has completed sending all of its packets, after which the other side can start sending packets.

- A suggested packet format:

```python
#structure of packet
    packe_type
    seq_num
    ack_num
    window_size
    data
     

```

**packe_type** field indicates the type (numeric code) of the packet, i.e., ACK or Data or EOT.
    
**seq_num** field is a sequence number used to number data packets.
    
**ack_num** field is used to indicate the previous data packet being acknowledged and the next expected sequence number.
    
**window_size** field would typically be used at the start of the session to establish the number of packets that will be sent from the transmitter to the receiver.

- The basic protocol is Send-and-Wait (Stop-and-Wait), however it's a modified version in which:
    * the sliding window is used to send multiple frames rather than single frames, 
    * a timer either waits for ACKs or to initiate a retransmission in the case of no response for each frame in the window.

- The window will slide forward with each ACK received, until all of the frames in the current window have been ACK'd.

- Both the transmitter and the receiver should print out the ongoing session information containing the type of packet sent, type of packet received, status of the window, sequence numbers, etc. 

- Application has to manage a log file at both the transmitter and the receiver. [Can be used for troubleshooting and validation].

- Network module will take arguments such as the BER (Bit Error Rate), average delay per packet, and will also have a configuration file specifying IP addresses and port numbers for the transmitter and receiver.

- The test document should have screen shots validating all of the protocol characteristics (examples: successful transactions, retransmissions, timeouts etc.) that have been implemented. Maybe also add Wireshark captures!
