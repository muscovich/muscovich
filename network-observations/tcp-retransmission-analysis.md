# TCP Retransmission and Acknowledgement Analysis

**Level:** Intermediate  
**Estimated time:** 35-45 minutes  
**Focus:** TCP sequence numbers, acknowledgements, retransmissions, duplicate ACKs, Wireshark

## 1. Learning objective

Investigate how TCP identifies missing data and how retransmission behaviour appears in a packet capture. Distinguish direct packet observations from Wireshark's analysis labels and from possible explanations such as packet loss, delay, reordering, or capture limitations.

This exercise builds on [Lab 002 - TCP connection lifecycle and packet analysis](./week-01-tcp-handshake-analysis.md). It does not require disrupting a live network or deliberately dropping traffic.

## 2. Concepts to understand

- TCP sequence numbers identify byte positions in a stream.
- Acknowledgement numbers indicate the next byte expected from the other endpoint.
- A retransmission sends data again when delivery is not sufficiently acknowledged.
- Duplicate ACKs can indicate that a receiver is still waiting for a missing segment.
- Fast retransmission and retransmission-timeout recovery are different mechanisms.
- Packet captures show traffic at one observation point, not necessarily the entire path.

## 3. Legal and safe scope

Use a PCAP you created on your own machine, a supplied training capture, or traffic from a system you are explicitly authorised to inspect. Do not capture unrelated users' traffic or intentionally degrade a shared network.

Do not publish raw captures. Review any evidence for IP addresses, hostnames, payloads, credentials, tokens, and personal data before including it in the archive.

## 4. Required tools

- Wireshark or TShark
- An authorised TCP PCAP containing a data transfer
- Optional: tcpdump for creating a short capture

A capture without retransmissions is still a valid result. Record that none were observed; do not manufacture a finding.

## 5. Procedure

### Step 1 - Select and document a capture

Use a capture from the previous local TCP lab or another authorised source. Record:

- Where the capture came from (for example, a local loopback experiment).
- Whether the connection was already established when capture began.
- Whether both traffic directions are visible.
- Whether the capture appears complete or has a known limitation.

If creating a new capture, use a controlled local service or a host you are authorised to test. Start capture before generating the traffic and stop it immediately afterwards.

### Step 2 - Identify one TCP stream

Open the capture in Wireshark and apply:

```text
tcp
```

Select a packet belonging to the data transfer, then use **Analyze -> Follow -> TCP Stream** (or the packet context menu). Note the stream number and isolate it:

```text
tcp.stream eq 0
```

Replace `0` with the stream number from your capture. Confirm the source and destination endpoints and which direction carries application data. Redact addresses in any public notes.

### Step 3 - Look for retransmission indicators

Apply these display filters one at a time:

| Filter | Purpose |
|---|---|
| `tcp.analysis.retransmission` | Packets Wireshark marks as suspected retransmissions |
| `tcp.analysis.fast_retransmission` | Suspected fast retransmissions |
| `tcp.analysis.spurious_retransmission` | Suspected spurious retransmissions |
| `tcp.analysis.duplicate_ack` | Duplicate acknowledgements |
| `tcp.analysis.out_of_order` | Suspected out-of-order segments |
| `tcp.analysis.lost_segment` | A previous segment was not present in the capture |

To limit a filter to the selected stream, combine it with the stream expression. For example:

```text
tcp.stream eq 0 && tcp.analysis.retransmission
```

Wireshark's labels are analysis heuristics based on the packets it has seen. Treat them as leads to investigate, not proof of where or why a packet was lost.

### Step 4 - Inspect a candidate retransmission

If Wireshark identifies one, select it and expand **Transmission Control Protocol** and **SEQ/ACK analysis**.

Compare the candidate with the earlier packet it appears to repeat. Record:

- Frame numbers and timestamps.
- Source and destination direction.
- TCP sequence number.
- Acknowledgement number, if present.
- TCP payload length.
- Time between the original and repeated segment.
- Relevant duplicate ACKs or later acknowledgements.

For a data segment, compare the sequence range and payload length rather than relying only on the packet's display label. Check whether the receiver later acknowledges the relevant byte range.

If there are no candidate packets, record the filters used and state that this capture contained no Wireshark-identified retransmissions. Continue with sequence and acknowledgement analysis on ordinary data segments.

### Step 5 - Build a packet timeline

Complete this table from the actual capture. Add rows as needed.

| Frame | Time | Direction | Seq | Ack | TCP payload length | Observation |
|---|---|---|---:|---:|---:|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

Explain the byte sequence progression. Remember that SYN and FIN each consume one sequence number, even though they do not carry application data.

### Step 6 - Optional command-line review

If TShark is installed, list retransmission-related packets:

```bash
tshark -r capture.pcapng -Y 'tcp.analysis.retransmission || tcp.analysis.fast_retransmission || tcp.analysis.duplicate_ack' -T fields -e frame.number -e frame.time_relative -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.seq -e tcp.ack -e tcp.len
```

Replace `capture.pcapng` with the path to your own capture. If the file is a PCAP rather than PCAPNG, use its actual filename. An empty result means the filter found no matching packets in that capture; it does not prove the network is loss-free.

## 6. Observations to record

| Observation | Your finding |
|---|---|
| Capture source and scope | |
| Wireshark/TShark version | |
| Stream number | |
| Retransmission indicators found? | |
| Candidate original frame(s) | |
| Candidate repeated frame(s) | |
| Sequence number comparison | |
| ACK behaviour | |
| Time between relevant frames | |
| Out-of-order or duplicate ACK indicators | |
| Capture limitations | |

## 7. Analysis questions

1. What does a TCP sequence number identify?
2. What does an acknowledgement number tell the sender?
3. How can duplicate ACKs contribute to fast retransmission?
4. How does a retransmission timeout differ from fast retransmission?
5. Why does a retransmission label not prove that a packet was lost somewhere on the network?
6. How could starting a capture mid-connection create misleading analysis labels?
7. What additional evidence would help distinguish packet loss from reordering or a capture drop?
8. If no retransmissions appear in the capture, what can you legitimately conclude?

## 8. Expected learning outcomes

You should be able to follow a TCP stream, compare sequence and acknowledgement fields, identify Wireshark retransmission indicators, and explain why packet-level evidence must be interpreted cautiously.

## 9. Limitations and reporting standard

A capture is limited to its capture point, interface, time window, snap length, and packet visibility. Wireshark may label a packet as a retransmission based on the sequence history available in the capture. Offloading, packet drops at the capture host, asymmetric visibility, and starting late can affect interpretation.

Separate:
- **Observation:** what the packet fields and timestamps show.
- **Analysis:** what those observations may indicate.
- **Conclusion:** what the evidence supports, including uncertainty.

Do not claim a retransmission occurred unless you have the packet evidence. Do not infer the physical location of packet loss from a single endpoint capture.

## 10. Suggested write-up

After completing the investigation, record the scope, environment, method, actual packet observations, analysis, limitations, and next question. Keep sensitive endpoint details redacted and do not commit raw captures.

## 11. Primary references

1. [Wireshark User's Guide - TCP Analysis](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html)
2. [Wireshark Display Filter Reference - TCP](https://www.wireshark.org/docs/dfref/t/tcp.html)
3. [RFC 9293 - Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293)
4. [TShark Manual](https://www.wireshark.org/docs/man-pages/tshark.html)

---

**Research standard:** A retransmission indicator is a starting point for analysis, not a complete diagnosis. Preserve the distinction between packet evidence, interpretation, and unverified cause.
