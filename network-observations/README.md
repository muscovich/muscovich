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
- [PCAP summary tool](tools/pcap-summary/README.md)
- [PCAP summary parser validation notes](tools/pcap-summary/validation-notes.md)

## Working method

Each investigation records its objective, scope, environment, method, observations, limitations, and references. Packet captures must be reviewed for credentials, personal data, and other sensitive information before publication.

The lab documents are procedures until the experiment is actually run. Results, command output, and conclusions are added only after collecting evidence. Expected observations are not presented as completed findings.

## Planned work

- Execute the TCP connection lifecycle lab and record a redacted packet sequence.
- Execute the TCP retransmission analysis using an authorised capture and record actual sequence/acknowledgement evidence.
- Run the local HTTP inspection and document actual request/response and packet observations.
- Extend the PCAP summary tool with protocol and endpoint statistics, with tests for supported and unsupported formats.

## Status

Initial protocol notes, DNS investigation notes, DNS resolution and cache procedures, DNS-over-TCP framing, packet-capture basics, a TCP connection lifecycle lab, new TCP retransmission and local HTTP inspection procedures, a small PCAP parsing utility, and a controlled synthetic-fixture validation record for the parser. The parser validation does not represent a live packet-capture experiment or validation on the user's computer. The presence of a lab procedure does not mean the experiment has been completed.
