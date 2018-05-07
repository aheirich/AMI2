# Protocol Handlers

Communication between clients and the system occurs through modular protocol handlers.
class ProtocolHandler is the base class.

## EPICS
<a href="https://epics.anl.gov">Experimental Physics and Industrial Control System</a> (EPICS) is a DOE supported protocol.
class EPICSProtocolHandler: supports EPICS


## TCP/IP
class TCPIPProtocolHandler: provides support for raw socket communication.

