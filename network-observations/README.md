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
- [PCAP summary tool](tools/pcap-summary/README.md)
- [PCAP summary parser validation notes](tools/pcap-summary/validation-notes.md)

## Working method

Each investigation records its objective, scope, environment, method, observations, limitations, and references. Packet captures must be reviewed for credentials, personal data, and other sensitive information before publication.

The lab documents are procedures until the experiment is actually run. Results, command output, and conclusions are added only after collecting evidence. Expected observations are not presented as completed findings.

## Planned work

- Execute the TCP connection lifecycle lab and record a redacted packet sequence.
- Execute the TCP retransmission analysis using an authorised capture and record actual sequence/acknowledgement evidence.
- Run the local HTTP inspection and document actual request/response and packet observations.
- Run traceroute and compare hop responses and RTTs across two limited traces.
- Inspect a TLS handshake and certificate verification result using a normal client connection.
- Extend the PCAP summary tool with protocol and endpoint statistics, with tests for supported and unsupported formats.

## Status

Initial protocol notes, DNS investigation notes, DNS resolution and cache procedures, DNS-over-TCP framing, packet-capture basics, TCP connection lifecycle and retransmission exercises, local HTTP inspection, traceroute/ICMP and TLS handshake/certificate inspection procedures, and a small PCAP parsing utility with controlled synthetic-fixture validation notes.

The traceroute and TLS documents now include desk-based completion notes and answers to their analysis questions. They do not claim live experiments were performed: user-device command output, packet captures, negotiated TLS parameters, certificate details, hop addresses, and RTT measurements remain uncollected. The parser validation uses synthetic fixtures and does not represent a live capture or validation on the user's computer.
