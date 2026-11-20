# Traceroute and ICMP Path Analysis

**Level:** Intermediate | **Estimated time:** 30-40 minutes  
**Focus:** IPv4 TTL, traceroute probes, ICMP Time Exceeded, hop count, round-trip time (RTT), path visibility

## 1. Learning objective

Use a standard traceroute utility to observe how packets with increasing IPv4 Time To Live (TTL) values reveal responding hops along a route. Correlate command output with ICMP messages in a packet capture and explain why traceroute is not necessarily a complete map of the network path.

This is a diagnostic exercise. It does not involve scanning port ranges, exploiting hosts, or changing network configurations.

## 2. Concepts

- The IPv4 TTL field limits how many router hops a packet can traverse.
- A router decrements TTL as it forwards an IPv4 packet.
- When TTL expires in transit, a router may return an ICMP Time Exceeded message.
- Traceroute increases the probe TTL to discover successive responding hops.
- RTT is the time between sending a probe and receiving its response.
- A `*` or timeout means no response arrived within the tool's wait period; it does not prove that the router or link is down.
- Implementations use different probe types and may show different paths.

## 3. Safe scope

Use a destination you are permitted to contact and keep the test to a small number of ordinary traceroute probes. This lab uses `example.com` as a demonstration target. If your network or organisation restricts diagnostic probes, use a local lab destination or obtain permission first.

Do not repeatedly run high-volume probes, use large packet sizes, or attempt to evade network controls. Do not publish your public IP address or unredacted route details.

## 4. Required tools

- Windows: `tracert`
- Linux: `traceroute` (install from your distribution's trusted package manager if needed)
- macOS: `traceroute`
- Optional: Wireshark

## 5. Procedure

### Step 1 - Record your environment

Record operating system/version, network connection type, traceroute implementation, date/time, and destination hostname. Do not put your home/public IP address in a public write-up.

### Step 2 - Run a limited trace

Windows PowerShell or Command Prompt:

```powershell
tracert -d -h 12 -w 1500 example.com
```

Linux:

```bash
traceroute -n -m 12 -w 1 example.com
```

macOS:

```bash
traceroute -n -m 12 -w 1 example.com
```

These commands limit the trace to 12 hops and use numeric addresses to avoid reverse-DNS lookup delays. Windows `tracert` normally sends ICMP Echo probes; common Unix traceroute implementations often use UDP probes by default. Record which implementation you used.

If the destination does not resolve, record the DNS error separately. Do not interpret a name-resolution failure as a routing failure.

### Step 3 - Read the output

For each hop, record the hop number, responding address (if shown), each RTT measurement, whether a probe timed out, and whether the destination was reached.

A hop may show multiple RTTs because the tool sends multiple probes at that TTL. The address shown is the source address of the response; it may not identify every interface or physical device involved in forwarding.

### Step 4 - Capture the probe traffic (optional)

Start Wireshark on the active network interface before running the trace again. Use:

```text
icmp
```

For Windows `tracert`, look for ICMP Echo Requests and ICMP Time Exceeded responses. For UDP-based traceroute, look for UDP probes and ICMP Time Exceeded responses. The final response can vary with the probe method and destination.

Useful display filters:

| Filter | Purpose |
|---|---|
| `icmp` | All decoded IPv4 ICMP |
| `icmp.type == 8` | IPv4 Echo Request |
| `icmp.type == 0` | IPv4 Echo Reply |
| `icmp.type == 11` | IPv4 Time Exceeded |
| `udp` | UDP probes, where used |

Select a Time Exceeded packet and inspect its ICMP type/code and the quoted original IP header. Compare the original probe TTL with the responding hop where the fields are available.

### Step 5 - Compare repeated traces

Run the same limited trace once more after a short pause. Compare responding hop addresses, RTT values, timeouts, and whether the route appears to differ.

Do not assume a difference proves a fault. Load balancing, changing routes, ICMP rate limiting, and response filtering can affect results.

## 6. Observation table

| Hop | Responding address (redacted) | RTT 1 | RTT 2 | RTT 3 | Result / note |
|---:|---|---:|---:|---:|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

Also record:

| Measurement | Finding |
|---|---|
| Destination | |
| OS and traceroute command | |
| Probe method (ICMP or UDP) | |
| Maximum hops configured | |
| Destination reached? | |
| Timeouts observed? | |
| Differences in second trace | |
| Capture limitations | |

## 7. Analysis questions

1. What does the IPv4 TTL field limit?
2. Why does traceroute begin with a small TTL and increase it?
3. What does ICMP Time Exceeded (Type 11, Code 0) communicate?
4. Why might a hop display `*` even though later hops respond?
5. Why can Windows `tracert` and Linux `traceroute` show different results?
6. What does RTT measure, and why is it not necessarily the router's processing time?
7. Why might two traces to the same destination show different responding hops?
8. What can you conclude if the final destination is not reached within the configured hop limit?
9. Why is traceroute not proof of the complete physical route taken by packets?

## 8. Expected learning outcomes

You should be able to explain TTL-based hop discovery, identify ICMP Time Exceeded messages, interpret RTT measurements, and describe common causes of missing or variable hop responses.

## 9. Limitations and reporting standard

Traceroute observes responses to probes from one source at one point in time. Routers and firewalls may filter, rate-limit, or deprioritise diagnostic messages. Return traffic can follow a different route from outbound probes. Load balancing can distribute probes across paths. A timeout is not proof of packet loss affecting ordinary application traffic.

Separate **observation** (the output and packet fields actually recorded), **analysis** (a possible explanation), and **conclusion** (what the trace supports and what remains unknown). Redact addresses and avoid publishing details that reveal a private network topology.

## 10. Suggested write-up

Document destination, scope, OS, traceroute implementation, exact command, observed hop/RTT table, packet evidence (if captured), analysis, limitations, and one follow-up question. Do not claim the trace was completed until you have run it and recorded the output.

## 11. Primary references

1. [Cisco - Use the Traceroute Command on Operating Systems](https://www.cisco.com/c/en/us/support/docs/ip/ip-routed-protocols/22826-traceroute.html)
2. [RFC 1812 - Requirements for IPv4 Routers](https://www.rfc-editor.org/rfc/rfc1812)
3. [RFC 792 - Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792)
4. [Linux traceroute manual](https://man.archlinux.org/man/traceroute.8)

---

**Research standard:** A traceroute shows responding hops, not necessarily every router or the physical route. Treat missing responses as unknown until corroborated by other evidence.


## 12. Completion notes - analysis and evidence status

**Completion type:** Desk-based analysis of the procedure and protocol questions.  
**Execution status:** No traceroute output or packet capture from the user's computer was supplied. The live observation fields below are intentionally not invented.

### Environment and execution record

| Item | Record |
|---|---|
| Target in procedure | `example.com` |
| User operating system | Not confirmed in this write-up |
| Command executed on user's device | Not supplied |
| Actual responding hops | Not collected |
| Actual RTT measurements | Not collected |
| Wireshark capture | Not supplied |
| Evidence status | Requires local execution |

### Analysis answers

1. **What does IPv4 TTL limit?**  
   It limits how many router hops an IPv4 packet can pass through before it is discarded. Each forwarding router decrements the TTL.

2. **Why does traceroute start with a small TTL and increase it?**  
   The first probe expires near the source, then each later probe is allowed one more hop. This makes successive routers reveal themselves through Time Exceeded responses.

3. **What does ICMP Time Exceeded (Type 11, Code 0) communicate?**  
   It indicates that a packet's TTL expired in transit. A router commonly sends this response to the source and includes part of the original packet so the probe can be identified.

4. **Why might a hop display `*` even though later hops respond?**  
   That router may filter, rate-limit, or deprioritise diagnostic responses. A later router can still return a response. The asterisk is a missing probe response, not proof that forwarding stopped.

5. **Why can Windows `tracert` and Linux `traceroute` show different results?**  
   Windows `tracert` normally uses ICMP Echo probes, while common Linux traceroute defaults to UDP probes. Routers and firewalls may treat these probe types differently. Options and timing can also differ.

6. **What does RTT measure, and why is it not necessarily router processing time?**  
   RTT measures elapsed time from sending a probe until its response returns. It includes forward-path delay, router handling, return-path delay, queuing, and scheduling, not just time spent processing at the router.

7. **Why might two traces show different responding hops?**  
   Routes can change, load balancing can select different paths, and ICMP responses can be filtered or rate-limited. Different probe timing can also affect which responses arrive.

8. **What can be concluded if the destination is not reached within the hop limit?**  
   Only that the trace did not receive a destination response within the configured limit. It does not establish that the destination is offline or unreachable by every application.

9. **Why is traceroute not proof of the complete physical route?**  
   It shows devices that respond to the probes. Some routers remain silent, return paths may differ, and the reported addresses do not reveal physical links or every forwarding device.

### Evidence-based conclusion

Traceroute uses increasing TTL values to prompt intermediate routers to return ICMP Time Exceeded messages. Its output is useful for identifying responding hops and measuring probe RTT, but missing responses and changing paths must be interpreted cautiously. No claim about a particular route, hop count, or latency is made here because the user's command output and packet capture were not available.

**Follow-up:** Run the command from the target machine twice, save the output privately, and replace the uncollected fields with the observed hop addresses (redacted), RTTs, and timeouts.
