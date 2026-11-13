"""Unit tests for pcap_summary.py using synthetic packet records."""

import struct
import tempfile
import unittest
from pathlib import Path

from pcap_summary import PcapError, parse_capture


def make_ipv4_packet(protocol: int) -> bytes:
    ethernet = b"\x00" * 12 + struct.pack("!H", 0x0800)
    ipv4 = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0, 20, 1, 0, 64, protocol, 0,
        b"\xc0\x00\x02\x01", b"\xc0\x00\x02\x02",
    )
    return ethernet + ipv4


def write_pcap(path: Path, packets: list[bytes]) -> None:
    with path.open("wb") as capture:
        capture.write(b"\xd4\xc3\xb2\xa1")
        capture.write(struct.pack("<HHIIII", 2, 4, 0, 0, 65535, 1))
        for packet in packets:
            capture.write(struct.pack("<IIII", 0, 0, len(packet), len(packet)))
            capture.write(packet)


class PcapSummaryTests(unittest.TestCase):
    def test_counts_supported_ipv4_protocols(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.pcap"
            packets = [
                make_ipv4_packet(6),
                make_ipv4_packet(17),
                make_ipv4_packet(1),
                make_ipv4_packet(99),
            ]
            write_pcap(path, packets)

            total, counts = parse_capture(path)

            self.assertEqual(total, 4)
            self.assertEqual(counts["TCP"], 1)
            self.assertEqual(counts["UDP"], 1)
            self.assertEqual(counts["ICMP"], 1)
            self.assertEqual(counts["IP_PROTOCOL_99"], 1)

    def test_rejects_unknown_file_format(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.pcap"
            path.write_bytes(b"not a pcap file")

            with self.assertRaises(PcapError):
                parse_capture(path)

    def test_rejects_truncated_packet_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "truncated.pcap"
            with path.open("wb") as capture:
                capture.write(b"\xd4\xc3\xb2\xa1")
                capture.write(struct.pack("<HHIIII", 2, 4, 0, 0, 65535, 1))
                capture.write(b"\x00\x00")

            with self.assertRaises(PcapError):
                parse_capture(path)


if __name__ == "__main__":
    unittest.main()
