# DNS over TCP and Message Framing

**Level:** Intermediate  
**Estimated time:** 40-50 minutes  
**Focus:** DNS transport, TCP framing, socket programming, Wireshark analysis

## 1. Learning objective

Build a minimal DNS-over-TCP client and local responder. Capture the exchange and identify how DNS messages are framed inside a TCP byte stream.

This follows the earlier DNS-over-UDP exercise and demonstrates why TCP DNS messages require a two-byte length prefix.

## 2. Concepts to understand

- DNS over UDP versus DNS over TCP
- TCP connection establishment and teardown
- TCP as a byte stream
- DNS-over-TCP two-byte message-length prefix
- Network byte order
- Partial reads and message boundaries
- DNS transaction IDs and response flags

## 3. Legal and safe lab scope

Use only your own machine or a VM you control. Bind the test responder to `127.0.0.1:53536`. Do not connect to external DNS servers or test third-party systems.

The responder returns a basic NOERROR response with the original question and no answer records. It is a framing demonstration, not a general-purpose DNS server.

## 4. Required tools

- Linux or a Linux VM
- Python 3
- Wireshark or tcpdump

## 5. Practical investigation

### Step 1 - Prepare the lab

```bash
mkdir -p ~/dns-tcp-lab
cd ~/dns-tcp-lab
```

### Step 2 - Create the TCP responder

Create `dns_tcp_server.py`:

```python
import socket
import struct

HOST = "127.0.0.1"
PORT = 53536

def recv_exact(conn, length):
    chunks = []
    remaining = length
    while remaining:
        chunk = conn.recv(remaining)
        if not chunk:
            raise ConnectionError("Peer closed before full message arrived")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"DNS-over-TCP responder listening on {HOST}:{PORT}")

    while True:
        conn, address = server.accept()
        with conn:
            try:
                prefix = recv_exact(conn, 2)
                message_length = struct.unpack("!H", prefix)[0]
                if message_length < 17 or message_length > 512:
                    raise ValueError("Unexpected DNS message length")

                query = recv_exact(conn, message_length)
                if len(query) < 12:
                    raise ValueError("DNS message shorter than header")

                txid = query[:2]
                question_count = struct.unpack("!H", query[4:6])[0]
                if question_count != 1:
                    raise ValueError("Lab responder expects one question")

                # Standard response, recursion available, NOERROR,
                # one question and zero answer/authority/additional records.
                flags = struct.pack("!H", 0x8180)
                counts = struct.pack("!HHHH", 1, 0, 0, 0)
                response = txid + flags + counts + query[12:]

                framed_response = struct.pack("!H", len(response)) + response
                conn.sendall(framed_response)
                print(f"Handled one framed query from {address}")

            except (ConnectionError, ValueError) as error:
                print(f"Rejected incomplete or unsupported message: {error}")
```

The `recv_exact` helper matters because TCP does not preserve application message boundaries. A single `recv` call is not guaranteed to return all requested bytes.

### Step 3 - Create the TCP client

Create `dns_tcp_client.py`:

```python
import socket
import struct
import random

SERVER = ("127.0.0.1", 53536)
DOMAIN = "tcp-lab.example"

qname = b""
for label in DOMAIN.split("."):
    encoded = label.encode("ascii")
    qname += bytes([len(encoded)]) + encoded
qname += b"\x00"

question = qname + struct.pack("!HH", 1, 1)
txid = random.randrange(65536)

header = struct.pack("!HHHHHH", txid, 0x0100, 1, 0, 0, 0)
dns_query = header + question

# DNS over TCP: a two-byte unsigned length precedes the DNS message.
framed_query = struct.pack("!H", len(dns_query)) + dns_query

def recv_exact(sock, length):
    data = bytearray()
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed before full response")
        data.extend(chunk)
    return bytes(data)

with socket.create_connection(SERVER, timeout=3) as sock:
    sock.sendall(framed_query)

    response_length = struct.unpack("!H", recv_exact(sock, 2))[0]
    response = recv_exact(sock, response_length)

if len(response) < 12:
    raise ValueError("DNS response shorter than header")

response_id, flags, qdcount, ancount, nscount, arcount = struct.unpack(
    "!HHHHHH", response[:12]
)

if response_id != txid or not (flags & 0x8000):
    raise ValueError("Response ID mismatch or QR flag not set")

print("Transaction ID:", hex(response_id))
print("Response flags:", hex(flags))
print("Questions:", qdcount)
print("Answers:", ancount)
print("DNS message length:", response_length)
print("TCP framing length:", response_length)
```

### Step 4 - Start the responder

In terminal one:

```bash
python3 dns_tcp_server.py
```

Expected observation: the responder reports that it is listening on `127.0.0.1:53536`.

### Step 5 - Capture the TCP exchange

In terminal two:

```bash
sudo tcpdump -i lo -nn -s0 -w dns-over-tcp.pcap 'tcp port 53536'
```

### Step 6 - Send the DNS query

In terminal three:

```bash
python3 dns_tcp_client.py
```

Record the actual output. Stop tcpdump with Ctrl+C, then stop the responder with Ctrl+C.

### Step 7 - Inspect the capture

Open `dns-over-tcp.pcap` in Wireshark.

Useful display filters:

| Investigation | Display filter |
|---|---|
| TCP lab traffic | `tcp.port == 53536` |
| DNS decoded over TCP | `dns && tcp.port == 53536` |
| SYN packets | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| SYN-ACK packets | `tcp.flags.syn == 1 && tcp.flags.ack == 1` |
| FIN packets | `tcp.flags.fin == 1` |
| TCP stream | `tcp.stream eq 0` |

Inspect the TCP handshake, the DNS query and response, and the connection close. Expand the DNS section and compare the DNS message length with the two-byte prefix carried before the DNS message.

If Wireshark does not automatically decode the traffic as DNS, use Decode As on the TCP port and select DNS over TCP, where available. Record that limitation rather than assuming the packet was decoded.

### Step 8 - Compare with the earlier UDP exercise

Compare the DNS-over-TCP capture with your DNS-over-UDP capture.

Record which transport protocol was used, whether a TCP handshake was present, how the message length was represented, and how the connection ended.

## 6. Observations to record

| Observation | Your actual finding |
|---|---|
| Local server address and port | |
| TCP handshake visible | |
| DNS query transaction ID | |
| DNS response transaction ID | |
| DNS question count | |
| DNS answer count | |
| Two-byte length prefix | |
| DNS message length | |
| Connection termination | |
| Wireshark DNS decoding successful | |

Also record packet numbers for the handshake, query, response, and close.

## 7. Knowledge assessment

1. Why does DNS over TCP use a two-byte length prefix?
2. Why is TCP described as a byte stream rather than a message-oriented transport?
3. Why can one `recv` call return fewer bytes than requested?
4. What is the purpose of `sendall`?
5. How does the TCP handshake differ from the DNS request/response exchange?
6. Why might DNS use TCP in addition to UDP?
7. What is the difference between the DNS message length and the TCP segment payload length?
8. Why should an implementation validate the length prefix before reading the message?
9. What does a zero-answer NOERROR response mean in this deliberately minimal lab?

## 8. Expected learning outcomes

You should be able to explain DNS-over-TCP framing, distinguish TCP transport setup from DNS message exchange, implement exact-length reads, and identify the DNS message inside a TCP stream in Wireshark.

## 9. GitHub research archive

Create:

`network-observations/dns-over-tcp-framing.md`

Include the lab topology, client and responder code, commands, actual packet observations, comparison with DNS over UDP, assessment answers, and implementation limitations. Do not publish unverified findings or sensitive captures.

## 10. Primary references

1. [RFC 1035 - Domain Names: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035) - DNS message format and TCP message framing.
2. [RFC 7766 - DNS Transport over TCP](https://www.rfc-editor.org/rfc/rfc7766) - DNS over TCP requirements and operational guidance.
3. [Python socket documentation](https://docs.python.org/3/library/socket.html) - TCP sockets, `recv`, and `sendall`.
4. [Python struct documentation](https://docs.python.org/3/library/struct.html) - Encoding and decoding network-order integers.
5. [Wireshark DNS display filter reference](https://www.wireshark.org/docs/dfref/d/dns.html) - DNS display filters.

---

**Research standard:** Explain both layers independently: what TCP does to deliver a byte stream, and what DNS means inside that stream. Do not confuse TCP segments with DNS messages.


## 11. Execution record - independent sandbox validation

**Status:** DNS-over-TCP framing and response assertions passed in an independent Linux execution container. This is not a run on the repository owner's machine.

**Environment:** Linux x86_64, Python 3.13.5. The client and responder used a real TCP loopback connection on port 53536. tcpdump/Wireshark were unavailable and raw packet capture was not permitted, so no PCAP or Wireshark packet-number observations are claimed.

**Code correction:** The QNAME terminator in the Python client must be the actual zero byte escape, with one backslash before x. The earlier repository version contained a doubled backslash, which would encode literal characters instead of the DNS root-label terminator. That source literal has been corrected above.

**Observed result from this run:**

- TCP connection established to 127.0.0.1:53536 and the framed DNS query was exchanged successfully.
- Transaction ID: 0xf5d5 (randomly generated for this run).
- Response flags: 0x8180; question count: 1; answer count: 0.
- The responder returned a deliberate NOERROR response with no answer records.
- DNS message length: 33 bytes; two-byte TCP length prefix decoded to 33.
- Python assertions confirmed the transaction ID, response flag, section counts, and exact length-prefix/message-length match.

**Capture limitation:** The TCP SYN/SYN-ACK/ACK handshake, TCP segment layout, DNS decode, and FIN teardown still need visual confirmation in Wireshark on a host with capture tools. The socket-level exchange and framing checks passed; no PCAP is claimed.
