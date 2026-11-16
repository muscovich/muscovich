# MINI LAB - DNS RESOLUTION AND SYSTEM NAME LOOKUPS

**Status:** Procedure documented; experiment results not yet recorded  
**Duration:** 20 minutes  
**Level:** Intermediate  
**Focus:** DNS, Linux networking, resolver behaviour, and Python

## Research question

What information can be observed when a system resolves a domain name, and why might a DNS command-line client and a Python application return different results?

## Objective

Use `dig` and Python's standard-library `socket` module to compare A and AAAA lookups, inspect TTL values, identify the configured resolver where possible, and compare the addresses returned by the operating system's name-resolution interface.

## Scope and safety

- Query a public test name such as `example.com` from your own computer.
- Use your own Linux system, WSL instance, or authorised lab VM.
- This exercise sends ordinary DNS queries; it does not scan or test third-party services.
- Do not publish internal resolver addresses, private hostnames, or unrelated packet-capture data without checking for sensitive information.
- Do not assume that a changed TTL proves which cache answered the query.

## Requirements and environment (2 minutes)

Requirements: Linux, WSL, or a Linux VM; Python 3; and `dig` from the `dnsutils` package (Debian/Ubuntu).

If `dig` is unavailable on Debian or Ubuntu:

```bash
sudo apt update
sudo apt install dnsutils
```

Record the environment:

```bash
date -Is
uname -a
python3 --version
dig -v
```

If `dig -v` is not recognised, install the package above. On Windows without WSL, use `Resolve-DnsName example.com -Type A` in PowerShell for the command-line comparison; the Python section works with Python installed on Windows too.

## Procedure

### Task 1 - Identify the local resolver (3 minutes)

On Linux, inspect resolver configuration:

```bash
cat /etc/resolv.conf
resolvectl status
```

If `resolvectl` is unavailable, record that and use the first command.

- A `nameserver` line identifies a resolver address configured for applications using this file.
- `resolvectl status` may show per-interface DNS servers and routing domains.
- A local stub address such as `127.0.0.53` is a local resolver listener, not necessarily the upstream DNS server.
- Containers, VPNs, WSL, NetworkManager, and other resolver managers can change what these commands show.

Record which command you used and what resolver information it exposed. Redact private addresses before publishing if they reveal internal network details.

### Task 2 - Query A and AAAA records (5 minutes)

Run:

```bash
dig example.com A
dig example.com AAAA
dig +noall +answer example.com A
```

Inspect:

- `status` in the header comments: DNS response code, commonly `NOERROR` for a successful response.
- `QUESTION SECTION`: requested name and record type.
- `ANSWER SECTION`: records returned.
- `TTL`: remaining cache lifetime reported by the responding resolver.
- `SERVER`: server that answered this query.
- `Query time`: time reported by `dig`.

An A query requests IPv4 records. An AAAA query requests IPv6 records. An empty AAAA answer does not by itself indicate DNS failure; check the response status and requested record type. The final command suppresses most output and displays only answer records. Record the actual output, including an empty answer if that is what you receive.

### Task 3 - Compare two lookups (4 minutes)

Run this command twice, with a short pause between runs:

```bash
dig +noall +answer example.com A
sleep 2
dig +noall +answer example.com A
```

Compare the address and TTL. A resolver cache may return a record with a lower remaining TTL on a later query. However, TTL behaviour alone does not prove that a particular cache was used: the resolver may refresh its cache, the answer may change, or requests may be handled by different resolver infrastructure. Query time is also affected by network conditions and resolver load.

Record both outputs exactly. If the TTL or address does not change, record that rather than treating it as an error.

### Task 4 - Compare with Python name resolution (5 minutes)

Create `dns_check.py`:

```bash
nano dns_check.py
```

Paste:

```python
import socket

domain = "example.com"
print(f"Resolving: {domain}")

try:
    results = socket.getaddrinfo(
        domain,
        None,
        type=socket.SOCK_STREAM
    )

    addresses = set()

    for family, socktype, proto, canonname, sockaddr in results:
        address = sockaddr[0]

        if family == socket.AF_INET:
            version = "IPv4"
        elif family == socket.AF_INET6:
            version = "IPv6"
        else:
            version = f"Address family {family}"

        addresses.add((version, address))

    for version, address in sorted(addresses):
        print(f"{version}: {address}")

    if not addresses:
        print("No addresses returned.")

except socket.gaierror as error:
    print(f"Name resolution failed: {error}")
```

Save and run:

```bash
python3 dns_check.py
```

How it works:

- `socket.getaddrinfo()` asks the operating system's name-resolution interface for address information suitable for a stream socket.
- `type=socket.SOCK_STREAM` limits returned socket information to stream sockets, commonly used with TCP.
- The first tuple field identifies the address family: `AF_INET` is IPv4 and `AF_INET6` is IPv6.
- `sockaddr[0]` contains the address string for either family.
- A set removes duplicate family/address pairs.
- `socket.gaierror` handles name-resolution errors.

Compare Python addresses with the A and AAAA results from `dig`. Do not expect identical output in every environment. `dig` performs DNS queries through its DNS client behaviour, while `getaddrinfo()` uses the operating system's name-resolution interface. That interface may consider local host files, resolver configuration, caches, address-family policy, and platform-specific behaviour. Python's result does not expose DNS TTL values.

### Task 5 - Record and interpret (1 minute)

Complete the worksheet using your actual results. If a command is unavailable or fails, record the error and environment rather than inventing an answer.

## Observation worksheet

| Field | Actual observation |
|---|---|
| Date and time | |
| Operating system / environment | |
| Python version | |
| `dig` version | |
| Resolver information observed | |
| A query response status | |
| A record address(es) and TTL | |
| AAAA query response status | |
| AAAA answer or empty answer | |
| First A lookup output | |
| Second A lookup output | |
| Python IPv4 address(es) | |
| Python IPv6 address(es) | |
| Errors or differences | |

## Analysis questions

1. What is the difference between an A record and an AAAA record?
2. Which resolver address did `dig` report, and is it necessarily the upstream resolver?
3. Did the TTL change between the two A lookups? What can and cannot be concluded?
4. Did Python return the same addresses as `dig`? If not, what operating-system or resolver behaviour might explain the difference?
5. Why can `getaddrinfo()` not be used to inspect the DNS TTL?
6. What evidence would be needed before concluding that a DNS cache caused a faster second lookup?

## Expected learning outcomes

After completing the procedure, you should be able to distinguish A and AAAA records, read resolver and response fields in `dig`, explain TTL limitations, and compare DNS answers with addresses returned by Python without assuming differences indicate a fault. These are expected outcomes, not claims that the experiment has been completed.

## Limitations

- A public domain can return different addresses depending on geography, resolver, load balancing, and time.
- TTL values are observations from the responding resolver and can change between queries.
- `getaddrinfo()` does not expose DNS transaction IDs, response codes, DNS answer sections, or TTL values.
- The exact resolver path depends on the operating system and local configuration.
- This exercise does not capture packets or prove whether an upstream recursive resolver used its cache.

## Suggested report format

When recording completed work, use: objective; scope; environment; method; observations; interpretation; limitations; references. Include commands and actual output, redacting private resolver details where necessary. Do not write in the first person as though commands have already been run. This file documents a procedure until genuine observations are added.

## References

- RFC 1034 - Domain Names: Concepts and Facilities: https://www.rfc-editor.org/rfc/rfc1034
- RFC 1035 - Domain Names: Implementation and Specification: https://www.rfc-editor.org/rfc/rfc1035
- Python socket documentation: https://docs.python.org/3/library/socket.html
- BIND 9 manual pages (including `dig`): https://bind9.readthedocs.io/en/latest/manpages.html
- systemd-resolved documentation: https://www.freedesktop.org/software/systemd/man/latest/resolved.conf.html

---
## Execution record - controlled sandbox attempt

**Validation status:** Attempted; external name resolution was unavailable in the isolated sandbox.

This is a record of commands and tests run in an isolated Linux environment. It is not a record of DNS behaviour on my personal computer or home network.

### Environment

- Date/time: 2026-11-16 09:16 UTC
- Operating system: Linux x86_64
- Kernel: 6.18.57
- Python: 3.13.5
- `dig`: not installed
- `nslookup`: not installed

### Task 1 - Identify the local resolver

The resolver configuration was not copied into this report because it can contain environment-specific infrastructure addresses. No upstream resolver identity was independently established during this attempt.

### Task 2 - Query A and AAAA records

The required `dig` client was unavailable. I therefore could not collect an A response, an AAAA response, DNS status codes, answer records, TTLs, resolver identity, or query times.

### Task 3 - Compare two lookups

This comparison could not be performed because the command-line DNS client was unavailable and the environment could not resolve the test name through the operating system resolver. No TTL values were observed.

### Task 4 - Compare with Python name resolution

The Python test used the lab's `socket.getaddrinfo()` approach against `example.com`. The call failed with:

```text
socket.gaierror: [Errno -3] Temporary failure in name resolution
```

This is the actual error returned by the sandbox. It means the name-resolution attempt failed in this environment. It does not establish whether the domain itself was unavailable, whether a resolver was reachable, or whether the user's computer would experience the same result.

### Observation worksheet

| Field | Actual observation |
| --- | --- |
| Date and time | 2026-11-16 09:16 UTC |
| Operating system / environment | Linux x86_64, isolated sandbox |
| Python version | 3.13.5 |
| `dig` version | Not installed |
| Resolver information observed | No upstream resolver independently identified |
| A query response status | Not observed |
| A record address(es) and TTL | Not observed |
| AAAA query response status | Not observed |
| AAAA answer or empty answer | Not observed |
| First A lookup output | Not run; `dig` unavailable |
| Second A lookup output | Not run |
| Python IPv4 address(es) | None returned; lookup failed |
| Python IPv6 address(es) | None returned; lookup failed |
| Errors or differences | `socket.gaierror: [Errno -3] Temporary failure in name resolution` |

### Analysis

1. An A record contains an IPv4 address. An AAAA record contains an IPv6 address.
2. The answering resolver could not be identified from a successful `dig` response because `dig` was unavailable and no successful lookup was obtained.
3. No TTL comparison is possible. A TTL comparison requires actual DNS answer records from both queries.
4. Python returned no addresses because `getaddrinfo()` failed. This is not a meaningful comparison with `dig`, since no successful `dig` answer was collected.
5. `getaddrinfo()` returns socket address information rather than the DNS answer section. Its result does not expose DNS record TTLs.
6. A faster second lookup alone would not prove caching. Stronger evidence would include repeated controlled queries, observed DNS packets, the same resolver path, and TTL behaviour consistent with a cached answer.

### Conclusion and limitations

The Python resolver call failed in this sandbox, and the DNS command-line utilities were not installed. Consequently, the A/AAAA comparison, TTL experiment, and successful resolver comparison remain unverified. I have not substituted expected public DNS answers for observations.

To complete the experiment on the user's computer, install the DNS utilities, run the A and AAAA commands, repeat the A query after the pause, and run `dns_check.py`. Record the actual outputs and local resolver context. The results may differ from this sandbox because DNS configuration and network access are environment-dependent.

**Evidence boundary:** This is a documented failed attempt, not a completed successful DNS-resolution experiment.
