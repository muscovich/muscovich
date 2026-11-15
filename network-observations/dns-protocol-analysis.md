# DNS Protocol Analysis and Python Packet Parsing

**Level:** Intermediate  
**Estimated time:** 40-50 minutes  
**Focus:** DNS, UDP, packet analysis, Linux networking, Python sockets

## 1. Learning objective

Build a small DNS client and responder using Python, exchange a DNS query over UDP on the local loopback interface, and inspect the request and response in Wireshark.

The aim is to understand DNS message structure and how application-layer messages are carried by UDP.

## 2. Concepts to understand

- DNS query and response structure
- DNS transaction IDs and header flags
- A and AAAA resource records
- UDP transport and port numbers
- DNS response codes (RCODE) and TTL
- Network byte order (big-endian)
- DNS name compression
- Python socket programming and binary data with `struct`

## 3. Legal and safe lab scope

Use only your own machine or a VM you control. The client and responder communicate over `127.0.0.1` using UDP port `53535`. No external DNS server or third-party system is involved.

The responder is a deliberately minimal teaching example. It is not a general-purpose DNS server and should not be exposed to a network.

## 4. Required tools

- Linux or a Linux VM
- Python 3
- Wireshark
- tcpdump

Check the tools:

```bash
python3 --version
tcpdump --version
```

## 5. Practical investigation

### Step 1 - Prepare the lab

```bash
mkdir -p ~/dns-research-lab
cd ~/dns-research-lab
```

### Step 2 - Create the local DNS responder

Create `dns_server.py`:

```python
import socket
import struct

HOST = "127.0.0.1"
PORT = 53535

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"DNS responder listening on {HOST}:{PORT}")

while True:
    data, address = sock.recvfrom(512)

    # This teaching responder accepts one-question DNS queries only.
    if len(data) < 17:
        continue

    transaction_id = data[:2]
    flags = struct.pack("!H", 0x8180)
    counts = struct.pack("!HHHH", 1, 1, 0, 0)

    # Preserve the query question section.
    question = data[12:]

    # Compression pointer to the QNAME at offset 12.
    answer_name = b"\xc0\x0c"

    # A / IN record, TTL 30 seconds, RDATA 127.0.0.1.
    answer_data = (
        answer_name
        + struct.pack("!HHIH", 1, 1, 30, 4)
        + socket.inet_aton("127.0.0.1")
    )

    response = transaction_id + flags + counts + question + answer_data
    sock.sendto(response, address)
    print(f"Replied to {address}")
```

The responder returns a fixed A record for the query name. It is intended only for the controlled client below; it does not validate arbitrary DNS input or implement the complete DNS protocol.

### Step 3 - Create the DNS client

Create `dns_client.py`:

```python
import random
import socket
import struct

SERVER = ("127.0.0.1", 53535)
DOMAIN = "lab.example"

transaction_id = random.randint(0, 65535)

header = struct.pack(
    "!HHHHHH",
    transaction_id,
    0x0100,  # Standard query with recursion desired.
    1, 0, 0, 0
)

qname = b""
for label in DOMAIN.split("."):
    encoded = label.encode("ascii")
    qname += bytes([len(encoded)]) + encoded
qname += b"\x00"

question = qname + struct.pack("!HH", 1, 1)  # QTYPE A, QCLASS IN.
packet = header + question

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(3)
    sock.sendto(packet, SERVER)
    response, _ = sock.recvfrom(512)

if len(response) < 12:
    raise ValueError("DNS response is shorter than its header")

dns_id, flags, qdcount, ancount, nscount, arcount = struct.unpack(
    "!HHHHHH", response[:12]
)

if dns_id != transaction_id:
    raise ValueError("Transaction ID does not match")
if not (flags & 0x8000):
    raise ValueError("Message is not marked as a DNS response")
if ancount < 1:
    raise ValueError("Response contains no answer")

# This lab responder echoes the original question without changing it.
answer_offset = 12 + len(question)
if len(response) < answer_offset + 16:
    raise ValueError("Response is too short for the expected A record")

# The answer begins with a 2-byte compression pointer, followed by
# TYPE (2), CLASS (2), TTL (4), RDLENGTH (2), and RDATA (4).
record_type, record_class, ttl, rdlength = struct.unpack(
    "!HHIH", response[answer_offset + 2:answer_offset + 12]
)
if record_type != 1 or record_class != 1 or rdlength != 4:
    raise ValueError("Unexpected answer record format")

ip_address = socket.inet_ntoa(
    response[answer_offset + 12:answer_offset + 16]
)

print("Transaction ID:", hex(dns_id))
print("Response flags:", hex(flags))
print("Questions:", qdcount)
print("Answers:", ancount)
print("Answer TTL:", ttl)
print("Resolved address:", ip_address)
```

The `!` prefix in the `struct` format strings means network byte order (big-endian).

### Step 4 - Start the responder

In terminal one:

```bash
cd ~/dns-research-lab
python3 dns_server.py
```

Expected observation: the responder reports that it is listening on `127.0.0.1:53535`. This is an expected behaviour, not a recorded result.

### Step 5 - Capture the DNS exchange

In terminal two:

```bash
sudo tcpdump -i lo -nn -s0 -w dns-investigation.pcap 'udp port 53535'
```

Leave the capture running.

### Step 6 - Send a query

In terminal three:

```bash
cd ~/dns-research-lab
python3 dns_client.py
```

Expected behaviour: the client sends one DNS query, receives the responder's reply, validates the transaction ID and response flag, and prints the answer details. Record the actual output; do not assume it succeeded.

Stop tcpdump with Ctrl+C. Stop the responder with Ctrl+C.

### Step 7 - Inspect the capture

Open the capture:

```bash
wireshark ~/dns-research-lab/dns-investigation.pcap
```

Useful display filters:

| Investigation | Wireshark filter |
|---|---|
| DNS packets | `dns` |
| DNS queries | `dns.flags.response == 0` |
| DNS responses | `dns.flags.response == 1` |
| A-record questions | `dns.qry.type == 1` |
| Successful DNS responses | `dns.flags.rcode == 0` |
| Lab UDP port | `udp.port == 53535` |

Inspect the transaction ID, flags, question count, answer count, query name, query type, TTL, and returned address. Confirm whether Wireshark decodes the packets as DNS.

### Step 8 - Change the query name

Change `DOMAIN` in the client to `research.example`, restart the responder and capture, then run the client again. Compare the question sections in the two captures.

Do not change the responder's fixed answer address; the experiment is about the DNS question and response structure, not real public name resolution.

## 6. Observations to record

Fill this table using your own capture and terminal output:

| Field | Actual observation |
|---|---|
| DNS server address | |
| UDP destination port | |
| Transaction ID | |
| Query domain | |
| Query type | |
| Response code | |
| Question count | |
| Answer count | |
| Returned IPv4 address | |
| TTL | |
| QR flag in query and response | |

Also record the packet numbers for the query and response, and note any unexpected behaviour or decoding limitations.

## 7. Knowledge assessment

Answer in your own words:

1. Why do many DNS queries use UDP?
2. What is the purpose of the DNS transaction ID?
3. What is the difference between A and AAAA records?
4. What does the QR bit indicate?
5. Why should a response match the query's transaction ID?
6. What does a resource record's TTL control?
7. Why does network byte order matter when constructing a packet?
8. What does the compression pointer `0xc00c` refer to in this example?
9. What could a mismatched transaction ID indicate?
10. Why might one application action generate multiple DNS queries?

## 8. Expected learning outcomes

After completing the lab, you should be able to:

- Explain the basic DNS message header and question/answer sections.
- Identify DNS over UDP in a packet capture.
- Explain transaction IDs, flags, record types, and TTL.
- Construct and parse basic binary protocol fields in Python.
- Relate Python socket operations to packets visible in Wireshark.
- Describe the limitations of a minimal protocol implementation.

## 9. GitHub research archive

Suggested destination:

`network-observations/dns-protocol-analysis.md`

Include:

- Objective and lab architecture
- Environment and commands
- Client and responder implementation
- Wireshark filters
- Actual packet observations
- DNS header analysis
- Knowledge assessment answers
- Limitations and lessons learned

Only publish observations you verified. Do not upload captures containing sensitive information; a sanitised packet summary is sufficient.

## 10. Primary references

1. [RFC 1035 - Domain Names: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035) - DNS message format and protocol behaviour.
2. [RFC 7766 - DNS Transport over TCP](https://www.rfc-editor.org/rfc/rfc7766) - DNS transport requirements for TCP.
3. [Python socket documentation](https://docs.python.org/3/library/socket.html) - UDP socket programming.
4. [Python struct documentation](https://docs.python.org/3/library/struct.html) - Binary data and network byte order.
5. [Wireshark DNS display filter reference](https://www.wireshark.org/docs/dfref/d/dns.html) - DNS packet display filters.

---

**Research standard:** Explain what the captured bytes demonstrate. Do not rely solely on automated protocol summaries, and do not report a packet or finding unless you observed it.


## 11. Execution record - independent sandbox validation

**Status:** Python protocol exchange and assertions passed in an independent Linux execution container. This is not a run on the repository owner's machine.

**Environment:** Linux x86_64, Python 3.13.5. The container did not provide tcpdump or Wireshark, and raw packet capture was not permitted. Therefore, no PCAP file or Wireshark packet-number observations are claimed. UDP/TCP exchanges were exercised through real loopback sockets and the received DNS message bytes were parsed and checked by Python assertions.

**Code correction:** The byte-string terminator and DNS compression pointer must be actual Python byte escapes, with one backslash before x in each escape. The earlier repository version contained doubled backslashes, which encode literal backslash characters instead of the intended DNS bytes. Those source literals have been corrected above.

**Observed result from this run:**

- Client and responder exchanged one DNS query and response over UDP loopback port 53535.
- Transaction ID: 0x97ff (randomly generated for this run).
- Response flags: 0x8180 (QR=1, standard response, RCODE=0).
- Question count: 1; answer count: 1.
- Answer: A / IN, TTL 30 seconds, address 127.0.0.1.
- Python assertions for the transaction ID, flags, counts, record fields, TTL, and address passed.

**Capture limitation:** Wireshark display-filter and PCAP inspection steps remain to be performed on a host with tcpdump/Wireshark. The values above are from the actual loopback socket exchange, not from a fabricated packet capture.
