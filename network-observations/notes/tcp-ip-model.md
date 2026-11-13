# TCP/IP MODEL

## Purpose

The TCP/IP model describes how data moves between applications across interconnected networks. It is useful when interpreting packet captures because each layer adds information needed by the next stage of communication.

## The four layers

| Layer | Main responsibility | Examples |
|---|---|---|
| Application | Defines protocols used by applications | HTTP, DNS, SSH, SMTP |
| Transport | Provides process-to-process communication | TCP, UDP |
| Internet | Addresses and routes packets between networks | IPv4, IPv6, ICMP |
| Link | Moves frames across a local network segment | Ethernet, Wi-Fi |

Some references use a five-layer teaching model by separating the physical layer from the link layer. The underlying concepts are compatible; the number of layers depends on the model being used.

## Encapsulation

When an application sends data, each layer adds its own header information.

A simplified TCP over IPv4 over Ethernet frame looks like this:

```text
+-------------------+
| Ethernet header   |
+-------------------+
| IPv4 header       |
+-------------------+
| TCP header        |
+-------------------+
| Application data  |
+-------------------+
```

At the receiving host, the headers are examined in reverse order. This process is called decapsulation.

## TCP and UDP

TCP provides a reliable, ordered byte stream. It uses sequence numbers, acknowledgements, retransmission, and flow control.

UDP sends independent datagrams without providing delivery guarantees, ordering, or retransmission at the transport layer.

Neither protocol is universally better. The correct choice depends on the application's requirements.

## Ports

A port identifies an application endpoint on a host. A transport flow is commonly identified by the protocol and the source and destination IP addresses and ports.

A port number alone does not prove which application is running. Services can use non-standard ports, and traffic can be tunnelled or proxied.

## Questions for packet analysis

1. Which layer does each visible header belong to?
2. What addresses and ports identify the flow?
3. Is the transport protocol TCP or UDP?
4. For TCP, what sequence and acknowledgement behaviour is visible?
5. What can be concluded from the capture, and what remains unknown?

## References

- RFC 9293 - Transmission Control Protocol: https://www.rfc-editor.org/rfc/rfc9293
- RFC 768 - User Datagram Protocol: https://www.rfc-editor.org/rfc/rfc768
- RFC 791 - Internet Protocol: https://www.rfc-editor.org/rfc/rfc791
