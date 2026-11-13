#!/usr/bin/env python3
"""Summarise basic protocol counts from classic Ethernet PCAP files.

Supported: classic PCAP, Ethernet, IPv4, TCP, UDP, and ICMP.
Not supported: PCAPNG, IPv6, VLAN decoding, or packet reassembly.
"""

from __future__ import annotations

import argparse
import struct
from collections import Counter
from pathlib import Path


MAGIC_FORMATS = {
    b"\xd4\xc3\xb2\xa1": "<",  # little-endian, microsecond timestamps
    b"\xa1\xb2\xc3\xd4": ">",  # big-endian, microsecond timestamps
    b"\x4d\x3c\xb2\xa1": "<",  # little-endian, nanosecond timestamps
    b"\xa1\xb2\x3c\x4d": ">",  # big-endian, nanosecond timestamps
}

ETHERNET_IPV4 = 0x0800
IP_PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP"}


class PcapError(Exception):
    """Raised when a capture is invalid or unsupported."""


def parse_capture(path: Path) -> tuple[int, Counter[str]]:
    counts: Counter[str] = Counter()
    total = 0

    with path.open("rb") as capture:
        header = capture.read(24)
        if len(header) != 24:
            raise PcapError("File is too short to contain a PCAP header.")

        byte_order = MAGIC_FORMATS.get(header[:4])
        if byte_order is None:
            raise PcapError("Unknown PCAP magic. PCAPNG is not supported.")

        major, minor, _zone, _sigfigs, snaplen, linktype = struct.unpack(
            byte_order + "HHIIII", header[4:24]
        )

        if (major, minor) != (2, 4):
            raise PcapError(f"Unsupported PCAP version: {major}.{minor}.")
        if linktype != 1:
            raise PcapError(
                f"Unsupported link type {linktype}; expected Ethernet (1)."
            )
        if snaplen == 0:
            raise PcapError("Invalid snapshot length of zero.")

        while True:
            packet_header = capture.read(16)
            if not packet_header:
                break
            if len(packet_header) != 16:
                raise PcapError("Truncated packet record header.")

            _seconds, _fraction, included_len, original_len = struct.unpack(
                byte_order + "IIII", packet_header
            )
            if included_len > snaplen:
                raise PcapError("Packet length exceeds declared snapshot length.")
            if included_len > original_len:
                raise PcapError("Captured packet length exceeds original length.")

            packet = capture.read(included_len)
            if len(packet) != included_len:
                raise PcapError("Truncated packet data.")

            total += 1
            if len(packet) < 14:
                counts["TRUNCATED_ETHERNET"] += 1
                continue

            ether_type = struct.unpack("!H", packet[12:14])[0]
            if ether_type != ETHERNET_IPV4:
                counts["NON_IPV4_ETHERNET"] += 1
                continue

            if len(packet) < 34:
                counts["TRUNCATED_IPV4"] += 1
                continue

            ip_offset = 14
            version_ihl = packet[ip_offset]
            version = version_ihl >> 4
            ihl = (version_ihl & 0x0F) * 4

            if version != 4 or ihl < 20:
                counts["INVALID_IPV4"] += 1
                continue
            if len(packet) < ip_offset + ihl:
                counts["TRUNCATED_IPV4"] += 1
                continue

            protocol_number = packet[ip_offset + 9]
            protocol_name = IP_PROTOCOLS.get(
                protocol_number, f"IP_PROTOCOL_{protocol_number}"
            )
            counts[protocol_name] += 1

    return total, counts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count basic protocols in a classic Ethernet PCAP file."
    )
    parser.add_argument("capture", type=Path, help="Path to a classic .pcap file")
    args = parser.parse_args()

    try:
        total, counts = parse_capture(args.capture)
    except (OSError, PcapError) as error:
        parser.error(str(error))

    print(f"Capture: {args.capture}")
    print(f"Total packets: {total}")
    print("Packet classification:")
    for name, count in sorted(counts.items()):
        print(f"  {name:<24} {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
