# HTTP Request and Response Inspection on Loopback

**Level:** Intermediate  
**Estimated time:** 30-40 minutes  
**Focus:** HTTP methods, request targets, status codes, headers, response bodies, TCP stream reassembly

## 1. Learning objective

Create a small HTTP service on the local machine, send requests to it, and inspect the HTTP request and response in a packet capture. Identify how application-layer messages are carried over TCP and how status codes and headers describe the response.

The service binds only to loopback. This is a protocol-learning exercise, not a test of a public website.

## 2. Concepts to understand

- HTTP request line: method, request target, and protocol version.
- HTTP response status line: protocol version, status code, and reason phrase.
- Request and response headers.
- Message body and Content-Length.
- TCP stream reassembly.
- The difference between plain HTTP and HTTPS visibility.
- Why a successful HTTP status does not automatically mean an application behaved as intended.

## 3. Legal and safe scope

Run the server on `127.0.0.1` only. Do not bind it to `0.0.0.0`, expose it to a LAN, or forward the port. Use synthetic text only; do not include real customer information, credentials, cookies, or tokens.

Plain HTTP is used here only on loopback so the protocol structure is visible. Do not send sensitive information over unencrypted HTTP.

## 4. Required tools

- Python 3
- curl
- Wireshark or tcpdump
- Linux, macOS, or Windows with Python and a packet-capture interface

## 5. Practical investigation

### Step 1 - Create a local HTTP server

Create a working directory:

```bash
mkdir -p ~/http-loopback-lab
cd ~/http-loopback-lab
```

Create `server.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8000

class LabHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path == "/status":
            status = 200
            body = b"local lab: service is available\n"
        elif self.path == "/missing":
            status = 404
            body = b"local lab: resource not found\n"
        else:
            status = 200
            body = b"local lab: hello from the loopback server\n"

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        print("HTTP:", format_string % args)

server = HTTPServer((HOST, PORT), LabHandler)
print(f"Listening only on http://{HOST}:{PORT}")
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nStopping local lab server")
finally:
    server.server_close()
```

Start it:

```bash
python3 server.py
```

Expected startup message: `Listening only on http://127.0.0.1:8000`. This is expected output from the code, not an observation until you run it.

### Step 2 - Start a packet capture

On Linux, identify the loopback interface:

```bash
ip -brief link
```

Start a capture on `lo`:

```bash
sudo tcpdump -i lo -nn -s0 -w http-loopback.pcap 'tcp port 8000'
```

On other operating systems, select the loopback capture interface (for example, Npcap Loopback Adapter on Windows) in Wireshark and use the capture filter:

```text
tcp port 8000
```

Start the capture before sending requests. If the loopback interface is unavailable, record that limitation instead of capturing unrelated traffic.

### Step 3 - Send a normal GET request

In a second terminal:

```bash
curl -i http://127.0.0.1:8000/
```

The `-i` option displays response headers as well as the body.

Record the actual status line, headers, and response body. Do not copy expected values into the results table without running the command.

### Step 4 - Request a second resource and a missing resource

Run:

```bash
curl -i http://127.0.0.1:8000/status
curl -i http://127.0.0.1:8000/missing
```

Compare the response status codes and bodies. The server deliberately returns a different response for `/missing` so you can inspect a 404 response in a controlled setting.

### Step 5 - Inspect requests and responses in Wireshark

Stop the capture with Ctrl+C. Open `http-loopback.pcap` in Wireshark.

Useful display filters:

| Filter | Purpose |
|---|---|
| `tcp.port == 8000` | All TCP packets for the local service |
| `http` | Packets Wireshark decodes as HTTP |
| `http.request` | HTTP requests |
| `http.response` | HTTP responses |
| `http.request.method == "GET"` | GET requests |
| `http.response.code == 404` | 404 responses |

Select a request and expand the HTTP section. Record the method, request URI, version, Host header (if present), and any other relevant headers. Select the matching response and record its status code, Content-Type, Content-Length, and body.

If the HTTP fields do not appear, select a packet from the TCP flow and use **Analyze -> Decode As** to check whether port 8000 is decoded as HTTP. You can also use **Follow -> TCP Stream** to inspect the reassembled byte stream. Record any decoding limitation.

### Step 6 - Compare HTTP messages with TCP packets

One HTTP message does not necessarily correspond to one TCP packet. TCP transports a byte stream; a larger HTTP message may be split across multiple segments, and several writes may be coalesced.

Use Follow TCP Stream to inspect the request and response as reconstructed by Wireshark. Compare the message structure with the individual packets. Do not assume each line of HTTP headers has its own TCP packet.

### Step 7 - Stop the server

Return to the server terminal and press Ctrl+C. Confirm that the local service has stopped. Keep the capture private until it has been checked for sensitive information.

## 6. Observations to record

| Request | Actual status code | Content-Type | Content-Length | Body summary |
|---|---:|---|---:|---|
| `/` | | | | |
| `/status` | | | | |
| `/missing` | | | | |

Also record:

- Operating system and Python version.
- Capture interface and tool version.
- Whether all three requests were visible.
- Whether Wireshark decoded HTTP automatically.
- Whether each HTTP message occupied one or multiple TCP segments.
- Any errors or missing packets.

## 7. Analysis questions

1. What are the three components of an HTTP request line?
2. What is the difference between a request header and a response header?
3. What does the 200 status code indicate in this lab?
4. What does the 404 status code indicate?
5. Why is Content-Length useful to the receiver?
6. Why might one HTTP response be carried in multiple TCP segments?
7. What does Follow TCP Stream show that the packet list alone may not make obvious?
8. Why should this plain HTTP lab remain on loopback?
9. Would the same HTTP headers normally be readable in a capture of HTTPS traffic without TLS decryption? Explain.
10. Why is a 200 response not, by itself, proof that a website or application is secure?

## 8. Expected learning outcomes

You should be able to identify an HTTP request and response, interpret common status codes and headers, correlate messages with a TCP stream, and explain why application messages and TCP packet boundaries are different.

## 9. Limitations and reporting standard

This lab uses a minimal Python HTTP/1.1 server and a small number of synthetic GET requests. It does not model authentication, sessions, cookies, concurrent production traffic, reverse proxies, HTTP/2, HTTP/3, TLS, or application security.

A loopback capture shows traffic visible to the local capture interface. It does not establish how a remote production service behaves. Record actual output and distinguish it from the expected behaviour described in this procedure.

Do not publish raw captures, cookies, tokens, or personal data. Redact local identifiers if necessary.

## 10. Suggested write-up

After running the exercise, document the objective, scope, environment, commands, actual responses, packet observations, analysis, limitations, and one follow-up question. Do not state that the exercise was completed until you have performed it and recorded evidence.

## 11. Primary references

1. [RFC 9110 - HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
2. [RFC 9112 - HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112)
3. [Python http.server documentation](https://docs.python.org/3/library/http.server.html)
4. [curl man page](https://curl.se/docs/manpage.html)
5. [Wireshark User's Guide - Following Protocol Streams](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html)

---

**Research standard:** Record the exact request and response evidence. Keep protocol observations separate from assumptions about the application or the security of a service.


---

## 12. Analysis completion - protocol interpretation (2026-11-25)

**Completion type:** Desk-based analysis of the documented loopback procedure.  
**Execution status:** No local server output, curl response, or PCAP from the user's computer was supplied. The observation table remains unfilled.

### Analysis answers

1. **Three components of an HTTP request line:** The method, request target, and HTTP version. For example, a request line may use `GET` as the method, `/status` as the target, and `HTTP/1.1` as the version. The example describes the protocol format, not a recorded request.
2. **Request header versus response header:** Request headers provide context about the client's request, such as the host or accepted content types. Response headers describe the returned representation or response handling, such as content type, content length, and connection behaviour.
3. **Meaning of 200 in this lab:** The local handler selected its normal success response for the requested path. It means the server reports that the request was successfully handled; it does not independently validate the correctness, safety, or usefulness of the application.
4. **Meaning of 404:** The server reports that it has no resource matching the requested target. In this lab, the handler deliberately maps `/missing` to a 404 response with a synthetic text body.
5. **Purpose of Content-Length:** It gives the message-body size in octets. In this server, the value is calculated from the byte string written as the body. Correct message framing matters because HTTP/1.1 carries messages over a persistent byte-stream transport.
6. **Why a response may span multiple TCP segments:** TCP transports an ordered byte stream, not application message boundaries. A response may be larger than the amount of data carried in one segment, and the operating system may split or combine writes according to buffering, segmentation, and network conditions.
7. **What Follow TCP Stream adds:** It reconstructs the stream's application bytes in sequence, making the full request and response easier to read. The packet list shows individual packets and timing; the reassembled stream shows how those packets contribute to the byte stream.
8. **Why plain HTTP stays on loopback:** Plain HTTP does not encrypt its contents. Loopback keeps this synthetic exercise on the same machine and avoids exposing the test messages to a LAN or the public network. No real credentials, tokens, or personal data should be sent.
9. **HTTPS visibility without TLS decryption:** A normal capture can still show network and transport metadata such as IP addresses, ports, packet sizes, and timing. Depending on the TLS version and handshake, some setup metadata may be visible, but the protected HTTP headers and body are encrypted and are not ordinarily readable as plain HTTP.
10. **Why 200 does not prove security:** A status code reports the outcome represented by the server's response. It does not test authentication, authorisation, input validation, confidentiality, integrity, dependency safety, or whether the application returned the right data.

### Expected response matrix - derived from the lab code, not observed output

| Request target | Handler branch | Status selected by code | Synthetic body |
|---|---|---:|---|
| `/` | Default branch | 200 | `local lab: hello from the loopback server\n` |
| `/status` | Status branch | 200 | `local lab: service is available\n` |
| `/missing` | Missing-resource branch | 404 | `local lab: resource not found\n` |

The table describes what the supplied handler is written to return. Actual client output, response headers, and packet segmentation must still be collected by running it.

### Implementation detail and interpretation

The handler sets `Content-Type: text/plain; charset=utf-8`, calculates `Content-Length` from the byte body, and sets `Connection: close`. Therefore, each curl invocation is expected to receive a response whose body length is based on the exact bytes emitted by the handler. The explicit close header means the server does not intend to keep that HTTP/1.1 connection open for another request.

The server uses Python's basic `HTTPServer`, which handles requests synchronously. This is sufficient for a small loopback protocol demonstration, but it is not a production server and does not model concurrent request handling or hardened deployment.

### Evidence boundary and remaining work

- **Completed here:** Answers to all ten analysis questions, code-derived response mapping, and implementation limitations.
- **Not completed:** Server startup on the user's device, actual curl output, capture interface confirmation, Wireshark decoding, frame numbers, TCP segment counts, and measured Content-Length values.
- **Next step:** Run the procedure locally, compare actual responses against the code-derived matrix, and add only verified values to the observation table.

No live HTTP exchange or packet capture is claimed.
