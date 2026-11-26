# NETWORK OBSERVATIONS

A practical notebook for understanding network traffic, protocols, and the behaviour of connected systems.

This project focuses on controlled experiments, packet-level inspection, and reproducible notes. All testing must be performed on systems you own or are explicitly authorised to assess.

## Contents

- [TCP/IP model](notes/tcp-ip-model.md)
- [DNS investigation](notes/dns-investigation.md)
- [DNS resolution mini lab - 20 minutes](dns-resolution-mini-lab.md)
- [DNS cache behaviour and TTL expiration](dns-cache-and-ttl.md)
- [DNS over TCP and message framing](dns-over-tcp-framing.md)
- [Packet capture basics](labs/packet-capture.md)
- [Lab 002 - TCP connection lifecycle and packet analysis](week-01-tcp-handshake-analysis.md)
- [TCP retransmission and acknowledgement analysis](tcp-retransmission-analysis.md)
- [HTTP request and response inspection on loopback](http-loopback-inspection.md)
- [Traceroute and ICMP path analysis](traceroute-icmp-path-analysis.md)
- [TLS handshake and certificate inspection](tls-handshake-certificate-inspection.md)
- [Linux routing and ARP neighbor analysis](linux-routing-arp-neighbour-analysis.md)
- [Linux host firewall inspection with nftables](nftables-host-firewall-inspection.md)
- [PCAP summary tool](tools/pcap-summary/README.md)
- [PCAP summary parser validation notes](tools/pcap-summary/validation-notes.md)

## Working method

Each investigation records its objective, scope, environment, method, observations, limitations, and references. Packet captures must be reviewed for credentials, personal data, and other sensitive information before publication.

The lab documents are procedures until the experiment is actually run. Results, command output, and conclusions are added only after collecting evidence. Expected observations are not presented as completed findings.

## Planned work

- Collect redacted packet-level evidence for the TCP connection lifecycle lab; its desk-based analysis is complete.
- Analyse an authorised capture for actual TCP retransmission and acknowledgement evidence; the desk-based analysis is complete.
- Collect actual local HTTP request/response and packet observations; desk-based protocol analysis is complete.
- Run traceroute twice and compare actual hop responses and RTTs; desk-based probe and interpretation analysis is complete.
- Inspect a TLS handshake and certificate verification result using a normal client connection.
- Inspect Linux routes, neighbor-cache state, and ARP resolution on an authorised local system.
- Perform live TLS handshake and certificate verification, recording actual negotiated parameters and packet observations.
- Perform live Linux route and neighbor-cache inspection, recording redacted command output and any observed ARP packets.
- Review nftables chains and rules using read-only commands, then correlate them with local listening sockets.
- Extend the PCAP summary tool with protocol and endpoint statistics, with tests for supported and unsupported formats.

## Status

Initial protocol notes, DNS investigation notes, DNS resolution and cache procedures, DNS-over-TCP framing, packet-capture basics, TCP connection lifecycle and retransmission exercises, local HTTP inspection with desk-based analysis, traceroute/ICMP with extended desk-based analysis, and TLS handshake/certificate inspection procedures, Linux routing/ARP and nftables firewall inspection procedures, and a small PCAP parsing utility with controlled synthetic-fixture validation notes.

The TLS handshake/certificate and Linux routing/ARP exercises have been reviewed and completed at the desk-based analysis level, with answers and evidence limitations documented. They do not claim live experiments were performed: user-device command output, packet captures, negotiated TLS parameters, certificate details, hop addresses, and RTT measurements remain uncollected. The TCP lifecycle and retransmission procedures still require real packet captures before packet numbers, timestamps, sequence/acknowledgement values, or retransmission findings can be recorded. The HTTP loopback procedure requires a local run and capture before actual response headers, body lengths, and packet segmentation can be recorded. The traceroute procedure requires two local traces before actual hop and RTT comparisons can be reported. The parser validation uses synthetic fixtures and does not represent a live capture or validation on the user's computer.
