# PCAP SUMMARY

A small standard-library Python utility that reads classic PCAP files and counts basic packet types.

## Supported input

- Classic PCAP files with microsecond or nanosecond timestamps.
- Ethernet link-layer captures.
- IPv4 packets.
- TCP, UDP, and ICMP protocol counts.

PCAPNG, IPv6, VLAN tag decoding, reassembly, and application protocol parsing are not currently supported.

## Usage

```bash
python pcap_summary.py capture.pcap
```

The tool prints packet totals and basic protocol counts. It does not export packet contents.

## Privacy

A packet capture can contain personal information, internal addresses, cookies, tokens, and other sensitive material. Use captures from your own lab and review them before sharing. This tool is for local analysis and does not transmit data.

## Limitations

This is an educational parser, not a replacement for Wireshark, tshark, or a forensic packet-analysis suite. Counts reflect packets that match the supported formats and protocols.
