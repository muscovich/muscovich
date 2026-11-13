# Research archive

A structured index for practical cybersecurity and systems study.

## Project areas

| Area | Scope | Suggested evidence |
|---|---|---|
| Network analysis | TCP/IP, DNS, HTTP, packet inspection | Redacted captures, diagrams, annotated observations |
| Linux systems | Processes, permissions, services, filesystems | Commands, scripts, configuration notes |
| Security labs | Defensive testing in isolated environments | Scope, setup, steps, results, remediation |
| Cryptography | Hashing, encryption concepts, key handling | Small implementations, test vectors, references |
| Digital forensics | Metadata, hashing, evidence handling | Reproducible workflows and integrity checks |
| Automation | Small Python and shell utilities | Source, usage examples, tests |

## Suggested repository roadmap

Create separate repositories as each area gains real content:

- `network-observations`
- `system-notes`
- `cryptographic-studies`
- `digital-forensics`
- `security-labs`
- `recon-toolkit`

These are planned project names, not claims that completed projects already exist.

## Standard experiment record

For every investigation, document:

1. **Objective** - what question is being tested?
2. **Scope** - which systems and data are authorised?
3. **Environment** - OS, versions, tools, and configuration.
4. **Method** - exact steps needed to reproduce the work.
5. **Observations** - what happened, including unexpected results.
6. **Conclusion** - what the evidence supports and what it does not.
7. **References** - primary documentation and relevant sources.

## Handling rules

- Use isolated labs, intentionally vulnerable targets, or explicitly authorised systems.
- Redact IP addresses, tokens, credentials, personal data, and identifying metadata where appropriate.
- Do not commit secrets, private keys, raw sensitive captures, or exploit data from third-party systems.
- Keep claims proportional to the evidence.
