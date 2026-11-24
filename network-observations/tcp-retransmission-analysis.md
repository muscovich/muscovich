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


---

## Desk-based analysis completion (2026-11-25)

**Status:** Conceptual analysis and a labelled synthetic sequence completed. No live or supplied PCAP was analysed for this completion.

### Analysis answers

1. **TCP sequence number:** A sequence number identifies the position of the first data byte carried in a TCP segment within that direction's byte stream. SYN consumes one sequence number before application data; FIN also consumes one.
2. **Acknowledgement number:** When ACK is set, the acknowledgement number normally identifies the next sequence number (byte) the receiver expects. It is cumulative: an ACK of 2001 indicates that bytes up to 2000 have been received in order.
3. **Duplicate ACKs and fast retransmission:** If later data arrives beyond a missing byte range, the receiver cannot advance its cumulative acknowledgement. It may send repeated ACKs for the next expected byte. Under the classic fast-retransmit rule, three duplicate ACKs can prompt the sender to retransmit the missing segment without waiting for the retransmission timer to expire. Modern TCP implementations can use additional loss-detection logic.
4. **Timeout versus fast retransmission:** Fast retransmission is triggered by evidence such as a sufficient run of duplicate ACKs. A retransmission timeout (RTO) occurs when the sender's retransmission timer expires without the required acknowledgement progress. RTO recovery generally indicates that the sender did not receive enough timely feedback to recover earlier.
5. **Why a Wireshark label is not proof of network loss:** Wireshark classifies packets using the sequence and acknowledgement history visible in the capture. A missing earlier packet could be due to actual network loss, capture loss, asymmetric routing, starting the capture late, or packet reordering. The label identifies a pattern in the capture, not the physical cause or location.
6. **Starting mid-connection:** If earlier sequence data is absent, Wireshark may not have enough context to know what the receiver has already seen. This can lead to misleading missing-segment or retransmission analysis, and the first visible packet may not be the beginning of the TCP connection.
7. **Evidence to distinguish causes:** Useful additional evidence includes a capture at the receiving endpoint, capture-drop counters, complete bidirectional visibility, TCP sequence ranges and timestamps, later cumulative ACKs, and a comparison with endpoint socket/application logs. Reordering can be suggested when the missing sequence range appears later and acknowledgements then advance; capture loss is more plausible if the capture tool reports drops. Neither conclusion should be made from one indicator alone.
8. **No retransmissions found:** The defensible conclusion is only that the selected capture and stream contained no packets identified by the chosen filters as retransmissions. It does not prove that the path had zero packet loss or that retransmissions did not occur outside the capture window.

### Synthetic sequence example - for interpretation only

The following is a deliberately constructed example to demonstrate cumulative acknowledgements. It is not a real capture and must not be entered as observed evidence.

Assume a sender begins application data at sequence number 1001 and sends four consecutive 1000-byte ranges:

| Illustrative event | Sequence range | Receiver response |
|---|---:|---|
| First segment is lost before reaching the receiver | 1001-2000 | No acknowledgement progress |
| Second segment arrives | 2001-3000 | Duplicate ACK 1001 |
| Third segment arrives | 3001-4000 | Duplicate ACK 1001 |
| Fourth segment arrives | 4001-5000 | Third duplicate ACK 1001 |
| Sender retransmits the missing first segment | 1001-2000 | Receiver can now acknowledge the contiguous data through 5000 with ACK 5001 |

The key point is that the receiver's cumulative ACK remains at 1001 while the initial byte range is missing, even though later ranges may have arrived and been buffered. Once the gap is filled, the acknowledgement can advance across the contiguous data already received.

Real captures may show different packet timing, ACK behaviour, window updates, SACK information, or recovery behaviour. Use the actual packet fields and TCP implementation context when analysing a real stream.

### Interpretation notes

- Compare both sequence number and payload length to establish the byte range represented by a segment.
- A repeated sequence range in the same direction is a useful retransmission candidate, but check timing, acknowledgements, and stream context.
- A duplicate ACK does not automatically mean a packet was lost; reordering and other conditions can produce similar observations.
- A capture with no retransmission indicators is still useful if its scope and limitations are documented.

### Evidence boundary and remaining work

- **Completed here:** Answers to all eight analysis questions, explanation of the main indicators, and a synthetic worked example.
- **Not completed:** Selection of an actual PCAP, stream number, Wireshark version, frame numbers, timestamps, measured sequence/ACK values, and TShark output.
- **Next step:** Run the filters against an authorised capture and replace the empty observation fields only with values verified from that capture.

No live retransmission, packet loss, duplicate ACK, or recovery event is claimed.
