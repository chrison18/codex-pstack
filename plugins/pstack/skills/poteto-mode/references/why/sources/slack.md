# Slack Conversations

Codex adapter: examples below describe evidence and search intent. Use only tools and schemas actually exposed in this session, within the user's source scope; do not assume the named vendor or operations are available. Keep all access read-only and record gaps.

## How to search it

Chat connector tools vary. Inspect actual available search/read tool schemas and use existing scoped access. Do not assume an authentication tool exists. If access fails, report the gap; do not reconfigure authentication or post messages.

1. **Author-bounded search.** Messages from the PR author around the PR merge date. Limits scope dramatically and often hits gold.
3. **PR URL search.** Slack often links PRs when they're reviewed or discussed. Search for the PR URL (or just `/pull/<number>`).
4. **Error string search.** If the code handles a specific error, search for the error string. Incident threads often surface.

## Common pitfalls

- **Channel archaeology limits.** Very old messages may be gone due to retention policies. If you can't find anything before a certain date, note the retention cliff.
- **Unsearched DMs.** Many decisions happen in DMs that aren't searchable. You'll miss them. That's a known limitation.
- **Speculative jokes as "decisions."** Slack is casual. "Lol just do the thing" isn't a decision, even if it preceded the commit. Look for considered discussion.
- **Context collapse in single messages.** Without the thread, a single message often reads differently than in context. Always fetch threads.
- **Auth failures.** If the MCP isn't authenticated, stop. Don't make up findings. Report that Slack wasn't searchable.
