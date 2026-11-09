# SPLICE integration

Reference: [SPLICE iframe protocol specification](https://cssplice.org/slcp/iframe-protocol-specification.html) and [demonstrations](https://cssplice.org/slcp/iframe-protocol-demos.html).

## Try it locally

Start `python server.py`, then open http://127.0.0.1:5173 and click **SPLICE inspector**. Open an exercise, submit an answer, and watch the messages. Reopen a free-coding activity to test restoration of its draft; the checked score is recorded separately.

A direct content URL is:

```text
http://127.0.0.1:5173/activity.html?id=cpp23-v2-01-first-programs-free-coding&protocol=splice
```

Use the course's **Copy iframe** button to generate markup. To inspect messages with the official demo, add this local URL to its “Add Your Own” section if the browser permits that HTTPS page to embed local HTTP content. Browser mixed-content/local-network rules can block that combination; the local host is the reliable test harness. A real shared content deployment should serve HTTPS with its execution service in a separate security sandbox.

For activities installed on the lab server, the analogous native launch form is:

```text
https://adapt2.sis.pitt.edu/cupcake/#/activities/<repository>/<path>.yaml?protocol=splice
```

This is a launch pattern observed from the application code, **not a claim that this course is uploaded there**.

## Messages

| Message | Producer | Handling here |
| --- | --- | --- |
| `SPLICE.getState` | Native Cupcake and our adapter | Host returns saved state or null, with the same message_id |
| `SPLICE.getState.response` | Course host | Adapter checks parent source, origin, and correlation ID |
| `SPLICE.reportScoreAndState` | Native Cupcake | Host validates score in [0,1], stores last score and merged state |
| `SPLICE.sendEvent` | Native Cupcake and adapter | Host stores a bounded local message history |
| `lti.frameResize` | Native Cupcake and adapter | Host uses adapter document-height messages, including guidance; clamps iframe height |

Every message has a unique `message_id`. The adapter uses `domain_id: cupcake-cpp-studio` and a stable activity ID as content_id. The host answers using the identity of its current, source-checked iframe. Native Cupcake also sends its own getState request with activity IDs under data. These two requests are expected and receive separate correlated responses.

The host's `context_id` identifies a local demonstration, not an authenticated learner. It supplies no invented user_id or user_model. A host that cannot restore state should return null. The activity still loads if no compatible parent replies, after a short adapter timeout.

## Saved state

SPLICE intentionally leaves the contents of state to the application. Our host merges the native event-specific state with this adapter envelope:

```json
{
  "schemaVersion": 2,
  "activityId": "cpp23-v2-01-first-programs-free-coding",
  "score": 1,
  "submission": {"answers": ["    std::cout << n * n << '\\n';"]},
  "draft": {"answers": ["    std::cout << n * n << '\\n';"]},
  "eventName": "answerChecked"
}
```

The adapter emits `studio.submission` as a sendEvent when a learner runs code. The host retains that submission even when a later native score report contains a different state shape. On a new launch, the adapter inserts submitted free-coding answers as the editable placeholders before giving the YAML to the viewer. It does not alter the reference solution or calculate scores from the restored code. The learner can edit and submit again.

In the course host, native `codeEdited` events save each free-coding region after the viewer's debounce pause. Draft text is restored ahead of checked submission text. Editing does not change the last checked score. The server's pinned viewer compatibility adjustment permits rechecking restored code without a token edit. Standalone views save checked code only; they explain that difference. Completion selections and Parsons arrangements are retained as evidence but are not replayed into upstream controls. Random tracing begins a fresh variant. Native Cupcake's current getState response path alone does not implement full session restoration.

`studio.hintOpened` events identify which progressive hint was opened; hints carry no score penalty. Adapter resize messages add `studio_document: true` so the host includes the guidance outside the native custom element and avoids competing native height reports.

The first capstone has two editable regions, as does the final project; the same array-based restoration works for both. Rebuilding a course with materially changed editable regions can invalidate old answers. For such revisions, use a new activity ID/version or clear the corresponding saved record deliberately.

## Boundaries

- A host checks both `event.source === iframe.contentWindow` and the expected content origin. Messages from arbitrary windows are ignored.
- The adapter checks responses come from its parent and, when available, the parent origin derived from document.referrer.
- Score, state storage, and event logging are separate concerns. Worked-example self-review is host bookkeeping, not an invented native assessment grade.
- Time-on-task, retries, feedback, snippets, mouse events, and submitted source may appear in native event data. Inspect exported JSON before sharing it.
- A production host should choose canonical identities, store evidence server-side, apply appropriate consent/retention rules, and define application-specific event semantics.
- This implements the iframe protocol. It does not claim LTI registration, OAuth, LMS roster synchronization, grade passback, a ProgSnap2 export, or a universal learner model.

The upstream native implementation sends many messages with a wildcard target origin. It is unmodified here. This host still verifies the sender, and the adapter's own outbound messages target the referrer origin when available. Hardening upstream receive-side origin validation is separate maintenance work.
