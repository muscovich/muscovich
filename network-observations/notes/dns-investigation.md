# DNS INVESTIGATION

## Objective

Understand how a DNS client resolves a name and how queries and responses appear in a packet capture.

## Core concepts

The Domain Name System maps names to records. Common record types include:

| Record | Purpose |
|---|---|
| A | Maps a name to an IPv4 address |
| AAAA | Maps a name to an IPv6 address |
| CNAME | Provides an alias to another name |
| MX | Identifies mail exchangers |
| NS | Identifies authoritative name servers |
| TXT | Stores text data used by services and domain configuration |
| PTR | Supports reverse lookups |

DNS commonly uses UDP port 53. TCP port 53 is also used, including for some large responses and zone-transfer operations. Encrypted DNS transports include DNS over TLS and DNS over HTTPS.

## Query and response

A basic lookup usually involves:

1. A client asks a configured resolver for a record.
2. The resolver answers from cache or performs additional lookups.
3. The client receives a response containing the requested record or an error status.

A packet capture may show the queried name, record type, response code, and returned records. It may not reveal the full resolution path if caching or encrypted DNS is involved.

## Controlled exercise

Use a system and resolver you are authorised to use.

1. Record the operating system and resolver configuration.
2. Query a test domain with a command-line DNS client.
3. Capture traffic on the relevant interface.
4. Identify the DNS query and matching response.
5. Record the transaction ID, query name, query type, response code, and answer.
6. Repeat the lookup and compare the result. Consider whether caching affected the second query.

Example commands:

```bash
nslookup example.com
```

or:

```bash
dig example.com A
```

## Analysis questions

- Was the query sent over UDP or TCP?
- Which resolver received the request?
- Was the response successful?
- Did the answer contain an A record, a CNAME, or both?
- Does the capture show the full resolution path?
- Could caching or encrypted DNS explain missing packets?

## Safety and privacy

Do not publish captures containing internal hostnames, private infrastructure details, user identifiers, or unrelated DNS activity without permission. Redact sensitive data before sharing.

## References

- RFC 1034 - Domain Names: Concepts and Facilities: https://www.rfc-editor.org/rfc/rfc1034
- RFC 1035 - Domain Names: Implementation and Specification: https://www.rfc-editor.org/rfc/rfc1035
- RFC 8484 - DNS Queries over HTTPS: https://www.rfc-editor.org/rfc/rfc8484
