# NETWORK OBSERVATIONS

A practical notebook for understanding network traffic, protocols, and the behaviour of connected systems.

This project focuses on controlled experiments, packet-level inspection, and reproducible notes. All testing must be performed on systems you own or are explicitly authorised to assess.

## Contents

- [TCP/IP model](notes/tcp-ip-model.md)
- [DNS investigation](notes/dns-investigation.md)
- [Packet capture basics](labs/packet-capture.md)
- [Lab 002 - TCP connection lifecycle and packet analysis](week-01-tcp-handshake-analysis.md)
- [PCAP summary tool](tools/pcap-summary/README.md)

## Working method

Each investigation records its objective, scope, environment, method, observations, limitations, and references. Packet captures must be reviewed for credentials, personal data, and other sensitive information before publication.

The lab documents are procedures until the experiment is actually run. Results, command output, and conclusions are added only after collecting evidence. Expected observations are not presented as completed findings.

## Planned work

- Execute the TCP connection lifecycle lab and record a redacted packet sequence.
- Compare DNS queries and responses, including the effect of resolver caching.
- Inspect HTTP request and response structure in a controlled local environment.
- Extend the PCAP summary tool with protocol and endpoint statistics, with tests for supported and unsupported formats.

## Status

Initial protocol notes, a packet-capture procedure, a TCP analysis lab, and a small PCAP parsing utility. The presence of a lab procedure does not mean the experiment has been completed.
