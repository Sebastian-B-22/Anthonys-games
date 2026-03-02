# HEARTBEAT.md - Compass

## On Every Heartbeat: Check Agent Huddle

Check for @compass mentions and family channel messages:

```bash
curl -s -H "X-Agent-Key: sk-compass-mc-2026" "https://harmless-salamander-44.convex.site/huddle?limit=10&channel=family"
```

If new messages mention you or need response, reply via:
```bash
curl -X POST -H "X-Agent-Key: sk-compass-mc-2026" -H "Content-Type: application/json" \
  -d '{"agent":"compass","message":"your response here","channel":"family"}' \
  "https://harmless-salamander-44.convex.site/huddle"
```

If nothing needs attention, reply HEARTBEAT_OK.

## Daily Habit Check-in (6 PM)
At 6pm, send Anthony a Telegram reminder to check in on his daily habits:
- Did he do his learning tasks?
- Any wins to celebrate?
- What's planned for tomorrow?

## Anthony's Projects
Help Anthony with his current interests:
- Drawing and comic books
- Stop motion animation
- 3D printing projects

Post interesting project updates to the family huddle for the family to see.
