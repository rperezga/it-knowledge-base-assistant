# New Employee Onboarding (Active Directory + Microsoft 365)

## Overview
This runbook covers provisioning a new hire so they can work on day one: an Active Directory (AD) account, group membership, and a Microsoft 365 (M365) mailbox and license.

## Before the start date
Collect the new hire's full legal name, department, manager, job title, and start date from the HR ticket. Confirm which security groups and distribution lists the role requires by checking the role template for that department.

## Create the Active Directory account
Create the user in the correct Organizational Unit (OU) for their department. Use the standard username format (first initial + last name). Set a temporary password and require a password change at first sign-in. Add the user to the role-based security groups defined in the department template, never by copying a random existing user.

## Assign Microsoft 365 license and mailbox
In the Microsoft 365 admin center, assign the license tier for the role (E3 for standard staff, E5 where advanced security is required). The Exchange Online mailbox is created automatically once the license is applied. Add the user to the relevant Teams and SharePoint sites and any shared mailboxes their role needs.

## Hardware and final steps
Submit the endpoint request so a laptop is imaged and shipped to arrive before the start date. Verify the user can sign in to M365 and that multi-factor authentication (MFA) enrollment is enforced. Close the onboarding ticket only after the manager confirms access on day one.
