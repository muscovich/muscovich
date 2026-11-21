# Linux Routing and ARP Neighbor Analysis

**Level:** Intermediate | **Estimated time:** 35-50 minutes  
**Focus:** Linux interfaces, routing tables, default gateways, ARP, neighbor cache, packet inspection

## 1. Learning objective

Map the local Linux network configuration to the kernel routing table and neighbor cache. Observe how a host decides where to send an IPv4 packet and how it resolves a next-hop MAC address on the local link.

The exercise uses read-only inspection commands and a small number of ordinary connections. It does not require changing routes, spoofing addresses, or scanning other devices.

## 2. Concepts

- A network interface provides a host with a connection to a network.
- An IP address and prefix length define the local IPv4 subnet.
- The routing table selects an outgoing interface and next hop.
- A default route is used when no more specific route matches.
- For an on-link IPv4 destination, the host resolves the destination's MAC address with ARP.
- For an off-link IPv4 destination, the host normally resolves the gateway's MAC address, not the remote server's MAC address.
- ARP maps IPv4 addresses to link-layer addresses on a local broadcast domain.
- The neighbor cache stores recently learned link-layer mappings and their states.
- IPv6 uses Neighbor Discovery (NDP), not ARP.

## 3. Safe scope

Run the commands on your own Linux computer or an authorised lab VM. Use the local routing table and, optionally, a normal connection to a destination you are permitted to contact. Do not alter routes or neighbor entries. Do not perform ARP spoofing, poisoning, or active discovery of devices on networks you do not administer.

Redact public addresses, MAC addresses, SSIDs, and private network details before publishing output.

## 4. Required tools

- Linux shell
- `iproute2` (`ip` command)
- Optional: Wireshark or TShark
- Optional: `ping` and `curl`

## 5. Procedure

### Step 1 - Identify interfaces and addresses

Run:

```bash
ip -br link
ip -br addr
```

Record interface names, link state, IPv4 address/prefix, and whether loopback is present. Do not assume that an interface marked UP necessarily has working external connectivity.

### Step 2 - Inspect routes

Run:

```bash
ip -4 route show
ip -6 route show
ip route get 1.1.1.1
```

The final command asks the kernel which route it would use for that destination; it does not send a packet. Record the selected interface, source address, gateway (if present), and route scope.

If you prefer not to query a public address, use an address belonging to a network you are authorised to inspect.

### Step 3 - Inspect the neighbor cache

Run:

```bash
ip neigh show
ip -6 neigh show
```

Record any entries, their interface, address family, link-layer address (keep private), and state such as REACHABLE, STALE, DELAY, or INCOMPLETE.

An empty cache is a valid observation. It may simply mean there has been no recent traffic requiring neighbor resolution.

### Step 4 - Generate one ordinary local-network connection

Identify the default gateway from your route table. If permitted, send one ping to that gateway:

```bash
ping -c 1 <gateway-ip>
```

Replace the placeholder with the gateway actually shown by your route table. If ICMP is blocked, do not treat the lack of a reply as proof that the gateway is unavailable.

Recheck:

```bash
ip neigh show
```

Compare the neighbor entry before and after the test. The entry may already have existed, or it may not remain visible long enough to observe.

### Step 5 - Optional packet capture

Start a capture on the relevant physical or virtual interface before repeating the single gateway ping. Use these Wireshark display filters:

| Filter | Purpose |
|---|---|
| `arp` | ARP packets |
| `arp.opcode == 1` | ARP requests |
| `arp.opcode == 2` | ARP replies |
| `icmp` | IPv4 ICMP |
| `icmpv6` | IPv6 ICMP, including NDP messages |

Inspect an ARP request and reply if they are present. Record sender/target protocol addresses and the operation type. Do not publish unredacted hardware addresses.

If the gateway mapping was already cached, a new ARP exchange may not occur. Do not flush the neighbor cache merely to force a packet; the exercise is designed to remain read-only.

### Step 6 - Explain next-hop selection

Compare the route lookup and neighbor table. Explain whether the host sends directly to an on-link destination or sends the packet to a gateway. For an off-link destination, the Ethernet destination MAC is normally the gateway's MAC, while the IP destination remains the remote host's IP address.

## 6. Observation table

| Item | Actual observation |
|---|---|
| Linux distribution/version | |
| Interface used | |
| Interface state | |
| Local IPv4 address/prefix (redacted) | |
| Default route (redacted) | |
| Route lookup result | |
| Neighbor entry before test | |
| Neighbor entry after test | |
| ARP request/reply captured? | |
| ICMP response received? | |
| Capture limitations | |

## 7. Analysis questions

1. What information does an interface address and prefix provide?
2. How does the kernel choose between a connected route and a default route?
3. What is the difference between a destination IP address and a next-hop MAC address?
4. Why does a host normally ARP for its gateway when contacting an off-link IPv4 destination?
5. Why might a neighbor entry be STALE rather than REACHABLE?
6. What does an INCOMPLETE neighbor state suggest?
7. Why might no ARP packet appear during a capture even though a connection succeeds?
8. How does IPv6 Neighbor Discovery differ from IPv4 ARP?
9. Why is an unexpected IP-to-MAC mapping worth investigating but not sufficient by itself to prove an attack?
10. What additional evidence would help distinguish normal address changes from suspicious ARP behavior?

## 8. Expected learning outcomes

You should be able to read Linux interface and route information, explain next-hop selection, interpret common neighbor states, and correlate routing decisions with ARP packet fields. You should also understand why an IP route and a layer-2 neighbor mapping describe different parts of packet delivery.

## 9. Limitations and reporting standard

The routing table and neighbor cache are snapshots and can change as interfaces, leases, routes, and traffic change. A packet capture may start after a mapping has already been learned. Virtual interfaces, VPNs, containers, Wi-Fi client isolation, and network policy can change what is visible.

Separate actual command output from interpretation. Do not claim that a particular gateway, MAC address, or ARP exchange was observed unless it was recorded. Keep sensitive network identifiers out of public commits.

## 10. Suggested write-up

Record the commands, environment, interface and route summary, neighbor states, any packet evidence, next-hop explanation, limitations, and one follow-up question. Redact identifying network details.

## 11. Primary references

1. [Linux ip-address manual](https://man7.org/linux/man-pages/man8/ip-address.8.html)
2. [Linux ip-route manual](https://man7.org/linux/man-pages/man8/ip-route.8.html)
3. [Linux ip-neighbour manual](https://man7.org/linux/man-pages/man8/ip-neighbour.8.html)
4. [RFC 826 - An Ethernet Address Resolution Protocol](https://www.rfc-editor.org/rfc/rfc826)
5. [RFC 4861 - Neighbor Discovery for IP version 6](https://www.rfc-editor.org/rfc/rfc4861)
6. [Wireshark ARP display filter reference](https://www.wireshark.org/docs/dfref/a/arp.html)

---

**Research standard:** A route lookup identifies the selected path and next hop; ARP resolves a local IPv4 next-hop address to a link-layer address. Do not confuse the remote IP destination with the Ethernet destination.

## 12. Completion notes - analysis and evidence status

**Completion type:** Desk-based protocol and command analysis.  
**Execution status:** No Linux command output or packet capture from the user's device was supplied. The environment, routes, neighbor entries, and observed ARP packets remain uncollected.

### Analysis answers

1. **What does an interface address and prefix provide?**  
   The address identifies the host on the IP network. The prefix length identifies the network portion used to determine which destinations are considered on-link.

2. **How does the kernel choose between connected and default routes?**  
   The kernel selects the best matching route, generally preferring the most specific prefix. A default route is the fallback when no more specific route matches.

3. **What is the difference between destination IP and next-hop MAC?**  
   The IP destination identifies the endpoint at the network layer. The next-hop MAC identifies the local link-layer recipient for the current Ethernet frame.

4. **Why ARP for the gateway for an off-link destination?**  
   The local host cannot deliver an Ethernet frame directly to a remote network's host. It sends the frame to the local router, while retaining the remote host's IP as the packet destination.

5. **Why might an entry be STALE?**  
   The mapping is known but has not recently been confirmed as reachable. The kernel can validate it when traffic next uses the entry.

6. **What does INCOMPLETE suggest?**  
   Neighbor resolution is in progress and a usable link-layer address has not yet been confirmed. It may resolve successfully or fail after retries.

7. **Why might no ARP appear when a connection succeeds?**  
   The mapping may already be cached, the capture may have started too late, or the traffic may use a different interface or link-layer mechanism.

8. **How does IPv6 Neighbor Discovery differ from ARP?**  
   NDP uses ICMPv6 messages and provides functions beyond address-to-link-layer resolution, including router discovery and neighbor reachability detection.

9. **Why is an unexpected mapping not proof of an attack?**  
   Legitimate causes include DHCP changes, interface replacement, virtual machines, failover, and stale cache entries. The mapping needs corroboration and context.

10. **What evidence helps distinguish normal changes from suspicious ARP behavior?**  
    Compare timestamps, DHCP lease records, switch or access-point logs where authorised, known device inventory, repeated packet observations, and whether conflicting mappings persist.

### Evidence-based conclusion

Linux routing and neighbor discovery work together but answer different questions. The routing table selects an outgoing path and next hop; ARP resolves an IPv4 next hop on the local link. Neighbor-cache state is time-dependent, and a missing ARP capture does not establish that resolution did not occur. No specific interface, gateway, MAC address, or packet sequence is claimed without device evidence.

**Follow-up:** Run the read-only commands locally and add redacted outputs and packet observations before marking the live experiment as executed.
