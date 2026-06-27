# Sample Q&A

Real output from `python rag.py` in **mock mode** (retrieval only, no API key).
With `--provider anthropic` or `openai`, the assistant synthesizes a concise answer from the same retrieved passages and cites them inline.

### Q: How do I reset my password?

Based on the knowledge base, the most relevant guidance is:

# Password Reset and Account Lockout
## Self-service password reset (preferred)
Users should reset their own password through the Microsoft self-service portal at the company SSPR link. They will verify identity with their registered MFA method (authenticator app or phone) and set a new password that meets the policy below. Self-service is available 24/7 and does not require contacting the service desk.
## Password policy
Passwords must be at least 14 characters and include three of: uppercase, lowercase, number, symbol. Passwords cannot reuse any of the last 10 passwords. Accounts lock for 15 minutes after 5 failed sign-in attempts.

(Sources: onboarding-new-user.md, password-reset.md, phishing-and-security.md)

**Retrieved sources:** password-reset.md (0.481), onboarding-new-user.md (0.146), phishing-and-security.md (0.097)

---

### Q: Why does my VPN keep disconnecting?

Based on the knowledge base, the most relevant guidance is:

# VPN Setup and Troubleshooting
## Connecting to the VPN
Install the company VPN client from the software portal. Sign in with your network credentials and approve the MFA prompt. Once connected, you will have access to internal file shares and line-of-business applications as if you were in the office.
## Common issue: VPN keeps disconnecting
Frequent disconnects are most often caused by an unstable home network or aggressive power management on the network adapter. First, test the connection over a wired Ethernet cable or move closer to the Wi-Fi router. Then, in Device Manager, open the network adapter properties and disable "Allow the computer to turn off this device to save power."

(Sources: m365-license-request.md, vpn-setup.md)

**Retrieved sources:** vpn-setup.md (0.251), vpn-setup.md (0.195), m365-license-request.md (0.093)

---

### Q: What do I need to onboard a new hire in AD and M365?

Based on the knowledge base, the most relevant guidance is:

# New Employee Onboarding (Active Directory + Microsoft 365)
## Overview
This runbook covers provisioning a new hire so they can work on day one: an Active Directory (AD) account, group membership, and a Microsoft 365 (M365) mailbox and license.
## Before the start date
Collect the new hire's full legal name, department, manager, job title, and start date from the HR ticket. Confirm which security groups and distribution lists the role requires by checking the role template for that department.

(Sources: onboarding-new-user.md, printer-troubleshooting.md)

**Retrieved sources:** onboarding-new-user.md (0.378), printer-troubleshooting.md (0.064), onboarding-new-user.md (0.046)

---

### Q: I clicked a phishing link and entered my password, what now?

Based on the knowledge base, the most relevant guidance is:

## What to do if you clicked a phishing link or entered credentials
Act immediately. Change your password right away using the self-service portal, and notify the security team so they can review account activity and revoke active sessions. If you entered credentials, the account is considered compromised until the security team confirms otherwise. Time matters, so report it even if you are not sure.
## Prevention
Multi-factor authentication (MFA) is required on all accounts and is the single most effective control against stolen passwords. Keep your authenticator app current, and never approve an MFA prompt you did not initiate.

(Sources: password-reset.md, phishing-and-security.md)

**Retrieved sources:** phishing-and-security.md (0.346), password-reset.md (0.182), phishing-and-security.md (0.179)

---

### Q: The shared printer shows offline for everyone, what should I do?

Based on the knowledge base, the most relevant guidance is:

# Printer Troubleshooting
## Printer shows offline
When a shared network printer shows "offline" for everyone, the print queue or the print server is usually the cause. First, check whether the printer has power and a network connection and can print a self-test page. Then restart the print spooler service on the print server and clear any stuck jobs in the queue.
## Printer shows offline for one user only
If only one user is affected, the issue is local. Remove and re-add the printer from the user's device using the correct print server path. Confirm the user is on the network or VPN, since mapped printers are not reachable off-network.

(Sources: m365-license-request.md, onboarding-new-user.md, printer-troubleshooting.md)

**Retrieved sources:** printer-troubleshooting.md (0.539), m365-license-request.md (0.092), onboarding-new-user.md (0.036)

---
