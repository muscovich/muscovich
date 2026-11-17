# PCAP Summary Parser - Controlled Fixture Validation

**Status:** Parser function exercised against synthetic fixtures in an isolated analysis environment  
**Date:** 2026-11-17 UTC  
**Scope:** Local parser validation only; no live traffic or user capture was used.

## Objective

Check whether the existing `pcap_summary.py` parser correctly classifies supported Ethernet/IPv4 protocol values and rejects several unsupported or malformed capture inputs.

The repository tool documents support for classic PCAP version 2.4, Ethernet link type 1, IPv4, TCP, UDP, and ICMP. It explicitly excludes PCAPNG, IPv6, VLAN decoding, and packet reassembly.

## Scope and safety

All packet records used in this validation were synthetic byte sequences created locally for testing. No network interface was opened, no traffic was generated, and no real PCAP or personal network data was read.

This validation does not establish behaviour on the user's computer or validate captures produced by a particular network interface.

## Environment

- Date/time: 2026-11-17 15:09 UTC
- Runtime: isolated Linux analysis environment
- Platform: Linux x86_64, glibc 2.41
- Kernel: 6.18.57
- Python: 3.13.5
- External packet tools: not required for these parser-function tests

## Method

The current `pcap_summary.py` source was fetched from the repository and exercised as a Python module. Temporary fixture files were created outside the repository.

The valid fixture builder wrote a classic PCAP global header and packet record headers, followed by minimal Ethernet frames containing IPv4 headers. The IPv4 protocol field was set to TCP (6), UDP (17), or ICMP (1). A separate Ethernet frame used EtherType 0x86DD to test non-IPv4 classification.

The parser function was called directly:

```python
total, counts = parse_capture(path)
```

The following cases were tested:

1. Little-endian, microsecond classic PCAP containing one TCP, one UDP, one ICMP, and one non-IPv4 Ethernet frame.
2. Big-endian, microsecond classic PCAP containing one TCP frame.
3. Little-endian, nanosecond classic PCAP containing one UDP frame.
4. A short invalid file.
5. A file beginning with the PCAPNG section-header magic.
6. A classic PCAP header declaring link type 101 rather than Ethernet.
7. A packet record whose declared captured length exceeded the bytes actually present.

## Observations

### Valid protocol classification

Actual parser output:

```text
VALID_FIXTURE 4 {'TCP': 1, 'UDP': 1, 'ICMP': 1, 'NON_IPV4_ETHERNET': 1}
```

The parser counted four packet records. Three were classified by their IPv4 protocol number, and the IPv6-EtherType frame was counted as non-IPv4 Ethernet.

### Endianness and timestamp variants

Actual parser output:

```text
BIG_ENDIAN 1 {'TCP': 1}
NANOSECOND 1 {'UDP': 1}
```

The tested big-endian microsecond fixture and little-endian nanosecond fixture were accepted and classified as expected for their constructed packet contents.

### Unsupported and malformed inputs

Actual parser output:

```text
ERROR_TEST unknown.pcap File is too short to contain a PCAP header. PASS
ERROR_TEST pcapng.pcap Unknown PCAP magic. PCAPNG is not supported. PASS
UNSUPPORTED_LINKTYPE Unsupported link type 101; expected Ethernet (1).
TRUNCATED_RECORD Truncated packet data.
```

The short-file and PCAPNG cases returned the expected `PcapError` messages. The unsupported link type and truncated packet-data cases also raised the expected parser exception category.

## Interpretation

The tests provide limited evidence that the parser:

- Reads the tested classic PCAP 2.4 global-header variants.
- Uses the global-header byte order when reading packet record lengths.
- Accepts the tested microsecond and nanosecond magic values.
- Classifies IPv4 protocol numbers 1, 6, and 17 as ICMP, TCP, and UDP.
- Counts a non-IPv4 Ethernet frame separately.
- Rejects PCAPNG input, an unsupported link type, and a truncated packet record.

These tests validate only the exercised code paths. They do not establish complete conformance to the PCAP specification or correctness against arbitrary real-world captures.

## Limitations and follow-up

- The fixtures are synthetic and deliberately small.
- The parser function was exercised directly; the command-line interface and its exit codes were not separately tested.
- IPv6, VLAN-tagged Ethernet, PCAPNG, packet fragmentation, and stream reassembly remain outside the documented scope.
- The current parser reads the IPv4 protocol field but does not interpret TCP/UDP headers, ports, checksums, or fragment offsets.
- No comparison against Wireshark or tshark was performed.
- No performance or large-file test was performed.

Suggested next tests:

1. Add repeatable automated unit tests for each supported header variant and error condition.
2. Add a test for a truncated Ethernet frame and a truncated IPv4 header.
3. Add a test for an IPv4 header with options (IHL greater than 5).
4. Compare parser totals against a known-good tool using a synthetic fixture that both tools can read.
5. Decide whether fragmented IPv4 packets should be counted by protocol number or reported separately.

## References

- Wireshark libpcap file format reference: https://wiki.wireshark.org/Development/LibpcapFileFormat
- Wireshark capture file documentation: https://www.wireshark.org/docs/wsug_html_chunked/ChIOOpenSection
- Python struct documentation: https://docs.python.org/3/library/struct.html
- Existing parser: ../tools/pcap-summary/pcap_summary.py

---

**Evidence boundary:** This is a real parser-function test performed in an isolated analysis environment using synthetic PCAP fixtures. It is not a live packet-capture exercise, a test on the user's Windows computer, or evidence that the user personally ran the experiment.
