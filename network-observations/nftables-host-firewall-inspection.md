# Linux Host Firewall Inspection with nftables

**Level:** Intermediate | **Estimated time:** 35-50 minutes  
**Focus:** Linux packet filtering, nftables rulesets, chains, hooks, policies, counters, defensive review

## 1. Learning objective

Inspect a Linux host firewall ruleset and explain how nftables tables, chains, hooks, priorities, policies, and rules influence packet handling. Use read-only commands and a controlled review process to identify what can and cannot be concluded from a ruleset.

This exercise does not change firewall configuration or attempt to bypass filtering.

## 2. Concepts

- nftables is the modern Linux packet-filtering framework.
- A table groups chains and related rules; it is not itself a firewall policy.
- A base chain is attached to a Netfilter hook such as input, output, or forward.
- Chain type and hook determine where packet processing occurs.
- A chain policy such as accept or drop applies when no rule gives a verdict in that base chain.
- Rules are evaluated in order within a chain.
- A rule can match interface, address, protocol, port, connection state, or other packet metadata.
- Counters can show packets and bytes matched since the counter was created or reset.
- An accept verdict in one chain does not necessarily mean no later hook or security control can affect the packet.
- Host firewall rules are only one part of a system's security posture.

## 3. Safe scope

Use a Linux system you own or are authorised to inspect. The lab is read-only: do not add, delete, flush, or reorder firewall rules. Do not run commands that disable the firewall or alter remote access. If you are connected to a remote machine, do not experiment with its firewall.

If nftables is unavailable, record that fact and inspect the firewall management method used by the distribution. Do not install or enable a firewall solely for this exercise.

## 4. Required tools

- Linux shell
- nftables command-line utility (`nft`), if installed
- Optional: `systemctl`, `iptables` compatibility inspection, and `ss`

## 5. Procedure

### Step 1 - Identify the environment

Run:

```bash
uname -a
nft --version
```

Record distribution/version and nftables version. If the command is unavailable, record it and do not treat that as evidence that the host has no firewall.

### Step 2 - Inspect service state without changing it

On systems using systemd, run:

```bash
systemctl is-active nftables
systemctl status nftables --no-pager
```

A service being inactive does not by itself prove that no nftables rules are loaded. Rules can be installed by other services or network-management components.

### Step 3 - Read the current ruleset

Run:

```bash
sudo nft list ruleset
```

This is a read-only listing operation. If permission is denied, record the error rather than trying to change privileges or policy beyond your normal authorised administration.

Review table names, chain names, chain types, hooks, priorities, policies, match conditions, verdicts, and counters. Do not publish the complete ruleset if it contains internal addresses or service details.

### Step 4 - Build a chain inventory

Create a small table from the ruleset:

| Table | Chain | Type | Hook | Policy | Purpose inferred from rules |
|---|---|---|---|---|---|
| | | | | | |

Do not infer a chain's purpose from its name alone. Use its hook, rules, and referenced sets to support the interpretation.

### Step 5 - Trace selected rule logic

Choose up to three rules and rewrite each in plain language. For each one, identify:
- Conditions that must match
- The packet direction or hook
- Any interface, protocol, address, or port constraints
- The resulting verdict (accept, drop, reject, jump, or goto)
- Whether a counter is present

Example of a generic rule interpretation: "For packets arriving on the external interface, if the protocol is TCP and the destination port is 22, apply the configured verdict." This is an explanation pattern, not a claim about the user's ruleset.

### Step 6 - Correlate with listening services

Run:

```bash
ss -lntup
```

Compare locally listening services with the firewall rules that appear relevant to inbound traffic. A listening socket does not prove that a remote host can reach it. Reachability can also depend on bind address, routing, firewall hooks, upstream filtering, and network topology.

Do not attempt connections from another device unless that device and the network are explicitly within your authorised lab scope.

### Step 7 - Optional counter review

If the ruleset already contains counters, record their displayed values and list the rules again after a normal, authorised local activity. Do not reset counters. Counter changes can help show that packets matched a rule, but they do not alone prove that a complete application connection succeeded or failed.

### Step 8 - Document limitations

Record whether the ruleset was complete, whether elevated read permission was available, whether another firewall manager may be involved, and whether container or virtualization rules may affect interpretation.

## 6. Observation table

| Item | Actual observation |
|---|---|
| Distribution/kernel | |
| nftables version | |
| nftables service state | |
| Ruleset readable? | |
| Tables present | |
| Input base-chain policy | |
| Output base-chain policy | |
| Forward base-chain policy | |
| Rules with counters | |
| Listening services reviewed | |
| Potentially relevant inbound rules | |
| Other firewall manager suspected? | |
| Evidence limitations | |

## 7. Analysis questions

1. What is the difference between a table and a base chain?
2. What does the input hook process compared with output and forward?
3. What happens when a packet reaches the end of a base chain without a matching verdict?
4. Why is a default accept policy not equivalent to "all services are reachable from the internet"?
5. Why does a listening socket not prove network reachability?
6. What is the difference between drop and reject?
7. Why should rule order be considered when interpreting a chain?
8. What can a rule counter establish, and what can it not establish?
9. Why might a host have firewall rules even when the nftables service appears inactive?
10. What additional evidence would be needed to assess whether a service is actually exposed?

## 8. Expected learning outcomes

You should be able to identify nftables tables and base chains, explain common hooks and policies, translate packet-match rules into plain language, and correlate firewall configuration with local listening sockets without overstating reachability.

## 9. Limitations and reporting standard

A ruleset listing is a snapshot. Rules may be managed by distribution tools, container runtimes, VPN software, or other services. Network namespaces can have separate rulesets. Firewall behavior can also depend on routing, connection tracking, interface configuration, upstream controls, and other security layers.

Do not infer internet exposure from a local ruleset alone. Do not change policy during this exercise. Keep internal IP addresses, interface names, and service details redacted in public notes where they could disclose sensitive infrastructure.

## 10. Suggested write-up

Record environment, exact read-only commands, chain inventory, interpretations of selected rules, socket correlation, limitations, and follow-up questions. Include only the minimum redacted rule excerpts needed to support the analysis.

## 11. Primary references

1. [Netfilter project - nftables documentation](https://www.netfilter.org/projects/nftables/)
2. [ nftables wiki - Quick reference](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes)
3. [Linux nft manual page](https://manpages.debian.org/bookworm/nftables/nft.8.en.html)
4. [Linux Netfilter hooks documentation](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks)
5. [Linux ss manual page](https://man7.org/linux/man-pages/man8/ss.8.html)

---

**Research standard:** A firewall ruleset describes configured packet-processing logic. It does not, on its own, prove end-to-end reachability or establish that a host is secure.

## 12. Completion notes - analysis and evidence status

**Completion type:** Desk-based configuration and protocol analysis.  
**Execution status:** No nftables ruleset, service status, or socket output from the user's Linux device was supplied. No host configuration or firewall result is claimed.

### Analysis answers

1. **What is the difference between a table and a base chain?**  
   A table is a container for chains, sets, and related objects. A base chain is attached to a Netfilter hook and participates in packet processing at that point.

2. **What do input, output, and forward hooks process?**  
   Input handles packets destined for the local host, output handles packets generated by the local host, and forward handles packets routed through the host.

3. **What happens at the end of a base chain without a matching verdict?**  
   The chain's policy applies. A policy is configured on a base chain and is commonly accept or drop.

4. **Why is default accept not the same as internet reachability?**  
   Reachability also depends on whether a service is listening, its bind address, routing, upstream firewalls, network address translation, and other controls.

5. **Why does a listening socket not prove network reachability?**  
   The socket may be bound only to loopback or a specific interface. Packets may also be filtered or lack a route to the host.

6. **What is the difference between drop and reject?**  
   Drop silently discards a packet. Reject discards it while sending an error response where supported, which can provide the sender with an explicit failure indication.

7. **Why consider rule order?**  
   Rules are evaluated sequentially. A verdict or jump can change whether later rules in that chain are reached, so the same match condition can have different effects depending on position and control flow.

8. **What can a rule counter establish?**  
   It can show that packets or bytes matched a rule during the counter's lifetime. It does not prove application success, identify every sender, or establish that all relevant traffic was captured.

9. **Why can rules exist while the nftables service is inactive?**  
   Rules can be loaded by another manager or service, and service state does not necessarily reflect the current kernel ruleset.

10. **What additional evidence is needed to assess exposure?**  
    Correlate the listening socket and bind address with the relevant ruleset, routing, interface configuration, upstream controls, and an authorised connectivity test from a known lab host.

### Evidence-based conclusion

nftables applies ordered rules at Netfilter hooks. Correct interpretation requires identifying the chain type, hook, policy, match conditions, and verdicts. Socket inspection adds context but does not prove remote reachability. No conclusion about the user's host firewall policy or exposed services is made because its ruleset and socket output were not supplied.

**Follow-up:** Inspect the local ruleset with read-only commands, redact sensitive details, and add the actual chain inventory and socket correlation before marking the live inspection as executed.
