# Printer Troubleshooting

## Printer shows offline
When a shared network printer shows "offline" for everyone, the print queue or the print server is usually the cause. First, check whether the printer has power and a network connection and can print a self-test page. Then restart the print spooler service on the print server and clear any stuck jobs in the queue.

## Printer shows offline for one user only
If only one user is affected, the issue is local. Remove and re-add the printer from the user's device using the correct print server path. Confirm the user is on the network or VPN, since mapped printers are not reachable off-network.

## Cannot print / jobs stuck in queue
Stuck jobs block everything behind them. Cancel all documents in the queue, then restart the Print Spooler service. If jobs reappear immediately, a corrupt job may need to be cleared from the spooler folder on the server.

## Toner and hardware
Low-toner and paper-jam messages are handled by the facilities team, not IT. For repeated hardware faults, log the device serial number and open a vendor service ticket.
