# Password Reset and Account Lockout

## Self-service password reset (preferred)
Users should reset their own password through the Microsoft self-service portal at the company SSPR link. They will verify identity with their registered MFA method (authenticator app or phone) and set a new password that meets the policy below. Self-service is available 24/7 and does not require contacting the service desk.

## Password policy
Passwords must be at least 14 characters and include three of: uppercase, lowercase, number, symbol. Passwords cannot reuse any of the last 10 passwords. Accounts lock for 15 minutes after 5 failed sign-in attempts.

## Account lockout
A locked account usually unlocks automatically after 15 minutes. If the user needs immediate access, a service desk analyst can unlock the account in Active Directory after verifying the user's identity using the standard identity-verification questions. Never unlock an account based on an email request alone.

## Escalation
If self-service reset fails repeatedly, confirm the user's MFA methods are still valid. Expired or lost MFA devices require re-registration, which must be done after identity verification. Repeated lockouts from one account may indicate a brute-force attempt and should be reported to the security team.
