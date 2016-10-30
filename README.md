# send-and-wait-protocol-emulator

Project contains implementation of a basic send-and-wait protocol simulator.
The protocol will be half-duplex and will use sliding windows to send multiple packets between two hosts on a LAN with an “unreliable network” between the two hosts.

**Model**:
```
  Transmitter --> Network Emulator  -->  Receiver	
  192.168.0.2 <--   192.168.0.3     <-- 192.168.0.1
```