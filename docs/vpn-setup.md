# VPN Setup and Troubleshooting

## Connecting to the VPN
Install the company VPN client from the software portal. Sign in with your network credentials and approve the MFA prompt. Once connected, you will have access to internal file shares and line-of-business applications as if you were in the office.

## Common issue: VPN keeps disconnecting
Frequent disconnects are most often caused by an unstable home network or aggressive power management on the network adapter. First, test the connection over a wired Ethernet cable or move closer to the Wi-Fi router. Then, in Device Manager, open the network adapter properties and disable "Allow the computer to turn off this device to save power."

## Common issue: cannot connect at all
Confirm the user can reach the internet without the VPN. Verify the VPN client is the current version and that the user's account is in the VPN-Users security group. If MFA prompts never arrive, check that the user's authenticator app is registered and time-synced.

## Split tunneling
The VPN uses split tunneling: only traffic to internal resources goes through the tunnel, while general internet traffic goes out directly. This is expected behavior and improves performance for cloud apps like Microsoft 365.
