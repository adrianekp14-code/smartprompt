# Notifications Log

Every prepared notification is listed here with its delivery status. "Delivered" is only written when the channel confirmed it.

| Date | Ticker | File | Research status | Channel | Delivery |
|---|---|---|---|---|---|
| 2026-11-08 | IESC | notifications/2026-11-08-IESC.md | Prepared; HELD pending FY26 10-K (send criteria in file) | — | NOT SENT (held by quality control) |

## Re-notification rule
A company is re-notified only if its research status changes materially (e.g., held → passed, thesis invalidated, or valuation moves through a scenario boundary).

## Delivery channels
- Scheduled cloud runs (Claude Code scheduled task) send a completion push notification to the account owner's Claude app when a run finishes with something noteworthy. Delivery of these pushes is not confirmed back to the session.
- Every notification is also committed to `research/notifications/` on branch `claude/equity-discovery-agent-z5gom2`.
- Email / Telegram: not configured (requires the owner's decision and, for Telegram, a bot token).
