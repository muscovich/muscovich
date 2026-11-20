# TLS Handshake and Certificate Inspection

**Level:** Intermediate | **Estimated time:** 35-45 minutes  
**Focus:** TLS negotiation, ClientHello, ServerHello, SNI, ALPN, certificate chain, certificate verification, encrypted application data

## 1. Learning objective

Establish a normal TLS connection to a public test endpoint, inspect the negotiated protocol and certificate information, and identify which handshake details are visible in a packet capture. Understand the difference between observing a TLS handshake and decrypting application data.

This is a client-side protocol inspection exercise. It does not attempt to bypass certificate validation or intercept another user's traffic.

## 2. Concepts

- TLS protects application traffic using negotiated cryptographic parameters.
- ClientHello contains client-offered parameters and extensions.
- ServerHello indicates the server's selected parameters.
- A certificate authenticates the server identity when certificate-based authentication is used.
- Certificate validation checks trust and identity; merely receiving a certificate is not enough.
- ALPN (Application-Layer Protocol Negotiation) can negotiate an application protocol such as HTTP/2.
- SNI (Server Name Indication) can indicate the hostname requested by the client, unless privacy mechanisms such as Encrypted ClientHello are in use.
- In TLS 1.3, much of the handshake after ServerHello is encrypted. A passive capture may not expose certificate contents or all handshake details.
- Encrypted application data is not normally readable as HTTP text without appropriate session secrets and authorised decryption.

## 3. Safe scope

Use a normal client connection to `example.com:443`. This is an ordinary TLS client handshake, not a vulnerability scan. Do not disable certificate verification, install interception certificates, collect other users' traffic, or publish session secrets.

If your organisation or network has rules for external connections, follow them. Do not upload packet captures or TLS key logs containing sensitive session material.

## 4. Required tools

- OpenSSL with `s_client`, if installed
- curl
- Wireshark (optional but recommended)

## 5. Procedure

### Step 1 - Record your environment

Record operating system/version, OpenSSL version, curl version and TLS backend, Wireshark version (if used), date/time, and destination hostname.

```bash
openssl version
curl --version
```

On Windows, these commands work in PowerShell or Command Prompt if the tools are installed and on PATH. If OpenSSL is unavailable, continue with curl and Wireshark.

### Step 2 - Inspect a TLS connection with OpenSSL

Run:

```bash
openssl s_client -connect example.com:443 -servername example.com -verify_return_error -showcerts
```

The `-servername` option sends the intended hostname through SNI. `-verify_return_error` makes verification errors fail the connection rather than silently continuing. `-showcerts` displays the certificate list sent by the server.

Record whether the handshake completed, negotiated protocol version, cipher suite, verification result/errors, leaf certificate subject and issuer, validity dates, Subject Alternative Names (SANs), and whether intermediate certificates were sent.

Exit the interactive client with Ctrl+C after recording the output. Do not remove `-verify_return_error` to make an error disappear. Investigate the cause instead.

If the server, local trust store, or network prevents the connection, record the exact error and continue with the curl step. Do not claim successful verification if the tool did not report one.

### Step 3 - Inspect the connection with curl

Run:

```bash
curl -Iv https://example.com/
```

The `-I` option requests response headers only; `-v` prints connection and TLS diagnostic information. Keep certificate verification enabled (the default). Record TLS version/cipher details if reported, certificate verification outcome, negotiated HTTP protocol (if reported), and HTTP response status.

A successful HTTP response is not a complete security assessment. This step only confirms what this client observed for this connection.

### Step 4 - Capture the handshake (optional)

Start Wireshark on the active network interface, then run the OpenSSL or curl connection again. Stop the capture immediately after the handshake and response complete.

Useful display filters:

| Filter | Purpose |
|---|---|
| `tls` | TLS packets Wireshark identifies |
| `tls.handshake` | TLS handshake messages |
| `tls.handshake.type == 1` | ClientHello |
| `tls.handshake.type == 2` | ServerHello |
| `tcp.port == 443` | TCP traffic on the usual HTTPS port |

Select ClientHello and inspect supported versions, cipher suites, extensions, SNI (if present), and ALPN protocols (if offered). Select ServerHello and inspect the selected version and cipher suite where Wireshark exposes them.

With TLS 1.3, do not expect a passive capture to reveal every later handshake message. After ServerHello, handshake messages such as EncryptedExtensions and Certificate are encrypted. A visible TLS record or encrypted application-data label does not reveal the underlying HTTP content.

### Step 5 - Inspect certificate identity and trust

Use the OpenSSL output to compare the hostname you connected to, certificate Subject Alternative Name entries, issuer and certificate chain, verification result, and certificate validity period.

A certificate's Common Name alone is not a sufficient modern hostname check; inspect SAN entries. A chain can be present but still fail verification. A certificate within its validity dates can still be untrusted or issued for a different hostname.

### Step 6 - Optional TShark summary

If TShark is installed and you saved a capture, list visible TLS handshake fields:

```bash
tshark -r tls-handshake.pcapng -Y 'tls.handshake' -T fields -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.type -e tls.handshake.version
```

Replace the filename with your capture's actual name. Field availability depends on TShark version and what Wireshark can dissect from the capture. An empty field is not proof that a value was absent from the actual connection.

## 6. Observation table

| Item | Actual observation |
|---|---|
| TLS connection completed? | |
| Negotiated TLS version | |
| Cipher suite | |
| ALPN result | |
| SNI visible in capture? | |
| ClientHello visible? | |
| ServerHello visible? | |
| Certificate details available in OpenSSL? | |
| Certificate verification result | |
| Certificate hostname matches target? | |
| HTTP protocol/status from curl | |
| Capture limitations | |

## 7. Analysis questions

1. What is the purpose of the TLS ClientHello?
2. What information does the ServerHello establish?
3. What is the role of SNI?
4. What does ALPN negotiate?
5. Why is receiving a certificate different from successfully verifying it?
6. Why should the certificate SAN be checked against the requested hostname?
7. Why might a passive TLS 1.3 capture show ClientHello and ServerHello but not readable certificate details?
8. What is the difference between TLS encryption and certificate-based authentication?
9. Why should certificate verification not be disabled simply to make a connection succeed?
10. What can you legitimately conclude from a successful TLS handshake, and what remains outside the scope of this test?

## 8. Expected learning outcomes

You should be able to identify key TLS handshake messages, interpret negotiated connection parameters, explain certificate identity and trust checks, and describe the visibility limits of a passive TLS 1.3 capture.

## 9. Limitations and reporting standard

This exercise tests one client connection to one public endpoint at one point in time. Server configuration, DNS resolution, network middleboxes, local trust stores, OpenSSL/curl versions, and TLS resumption can affect the observed result. A resumed session may not show the same full handshake as a new connection.

Do not claim that a service is secure based only on a successful handshake. This lab does not test application vulnerabilities, server hardening, certificate lifecycle management, key compromise, or every client/server configuration.

Do not publish private keys, session secrets, TLS key-log files, or unredacted captures. Keep certificate observations to the minimum required for the write-up.

## 10. Suggested write-up

Document destination and scope, tool versions, exact commands, negotiated TLS details, certificate verification outcome, packet observations, analysis, limitations, and one follow-up question. Record only results you actually observed.

## 11. Primary references

1. [RFC 8446 - The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)
2. [OpenSSL - s_client documentation](https://docs.openssl.org/master/man1/openssl-s_client/)
3. [Wireshark Display Filter Reference - TLS](https://www.wireshark.org/docs/dfref/t/tls.html)
4. [RFC 6066 - TLS Extensions: Server Name Indication](https://www.rfc-editor.org/rfc/rfc6066)
5. [RFC 7301 - ALPN Extension](https://www.rfc-editor.org/rfc/rfc7301)

---

**Research standard:** A visible TLS handshake provides evidence about negotiation and authentication for one connection. It does not, by itself, establish the overall security of the endpoint or application.
