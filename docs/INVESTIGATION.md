# Cupcake authoring and web integration investigation

Observed 7 November 2026. Deployed applications can change; raw public responses, application bundles, and installed extension tutorials are retained under `research/`. Updated for the C++23 teaching revision; the separate v1 review records remain historical evidence.

## Authoring model

The installed extension is **moh70-pawslab-pitt.cupcake-vscode 0.1.4**. An older pawslab-pitt 0.0.1 installation is also present. This project uses the newer installation's schemas and browser bundle. Its README, tutorials, package metadata, and compiled authoring integration were inspected locally.

Cupcake is principally an authoring format and a collection of interactive activity viewers, with supporting execution, catalog, journey, authentication, and logging services. An activity is a YAML object with common metadata and type-specific interaction definitions. It can hold its program inline as a filename-to-content mapping. An external source path is also supported; it must travel with the YAML. Embedded sources are convenient for portable distribution. This course includes an embedded header example as well.

| Field | Meaning |
| --- | --- |
| `$schema` | Official activity schema URI, including version |
| `id`, `title`, `description`, `license`, `locale` | Activity identity and descriptive metadata |
| `authors` | Optional structured author records; we omit these rather than invent a person/email |
| `pedagogy` | Activity type, difficulty, prerequisites, and topics |
| `runtime` | Language identifier and version, here `cpp` and `23` |
| `source`, `includes` | External paths or embedded filename/content maps |
| `elements` | Snippet-located explanations, blanks, editable regions, movable blocks, or parameters |
| `executions` | Demonstration runs for worked examples |
| `testcases` | Expected outputs for assessed programming activities |

Locations use snippets, optional occurrence numbers and context, or patterns in the wider upstream format. Our adapter deliberately implements only the snippet/context/occurrence subset used by this course. Repeated and overlapping text needs careful location validation. Parsons blocks must cover complete lines; their solution indentation is recorded in spaces.

## Viewers and language coverage

| Activity identifier | Student interaction | How this course uses it |
| --- | --- | --- |
| `worked-example` | Click annotations and inspect authored runs | 20 examples |
| `code-completion` | Select code snippets for blanks | 20 exercises |
| `multiple-choice-question` | Choose a conceptual answer with explanations | 20 questions |
| `free-coding` | Edit permitted source regions and run tests | 20 exercises + 2 capstones |
| `parsons-puzzles` | Arrange movable blocks | 20 puzzles |
| `parameterized-code-tracing` | Predict output after parameter substitution | 20 exercises, 60 verified variants |
| `macro-visualization` | Step through authored JSVEE state actions | 20 C++ walkthroughs |

The extension lists Python, Java, C/C++, JavaScript/TypeScript, SQL, Rust, Go, C#, and R. The deployed public repository catalog additionally contains HTML and CSS samples. These facts support language breadth, but do not prove that an arbitrary new language automatically has an executable runner. Dart, for example, was not verified in the deployed runner. Source highlighting, GUI editing, execution, browser rendering, and visualization generation are separate capabilities. The extension's macro-generation instructions specifically restrict that pipeline to Python.

The browser build registers `cupcake-activity-viewer` and `cupcake-activity-editor` custom elements. The VS Code extension injects YAML into the former for local preview and forwards execution requests to an authenticated service. We reuse that viewer and provide a local compiler bridge with the same request shape. Vendored files remain intact; a pinned response-only adjustment enables checking unchanged/restored free code. C++ macro actions are authored manually rather than produced by the Python generator. Details are in `docs/CXX23-REVIEW.md`.

## Deployed Cupcake

The requested [Activities application](https://adapt2.sis.pitt.edu/cupcake/#/activities) is an Angular application. Read-only requests to its observed public APIs supplied a repository directory and activity descriptions:

- `GET /cupcake/api/v1/activities/` lists public repositories.
- `GET /cupcake/api/v1/activities/<repository>/<path>` returns a directory or `{isFile, content}` for a file.
- `GET /cupcake/api/v1/activities/all` returns a flat public activity listing.

The response included `cpp-sample` with six activity YAML files sharing a C++ source file, plus language sample repositories and migrated collections such as annex, quizjpet, jsparsons, jsvee, and webex. We inspected the C++ completion, free-coding, and tracing YAML directly. A sample is illustrative rather than guaranteed to satisfy the latest schema; our own packages are validated independently.

Observed runtime code uses `POST /api/v1/execution/run` for an in-memory YAML preview, and `POST /api/v1/activities/run` for server-held paths. Requests include selections or edited answers. Responses are execution arrays containing stdout, stderr, case titles, and pass information. The native free-coding viewer selects results with `type: testcase`; our adapter supplies this field.

The extension documentation requires sign-in for hosted generation and code execution. Editing and preview rendering do not require sign-in. We did not obtain a token, invoke hosted AI, or assume permission to write into the lab service.

## Lab SLC catalog

The requested [catalog-v2 application](https://adapt2.sis.pitt.edu/next.course-authoring/#/catalog-v2) is a second Angular application. Its deployed client uses `/next.course-authoring/api/slc-items` for the newer record model. An unauthenticated read returned HTTP 403, so we do not claim a complete authenticated v2 export.

The public legacy `/next.course-authoring/api/catalog/contents` endpoint returned **4,315 records**. Counts by provider include webex 835, pcex 786, pcex_ch 759, pcrs 475, JSVEE 331, quizjet 232, quizpet 215, and Cupcake 15, among others. These are endpoint snapshot counts, not necessarily the count currently displayed by v2 and not counts of unique learning objectives.

The 15 Cupcake records include modern Java tasks such as arrays of points and book searches. Historical records point to other viewers, including ACOS PCEX activities and older question, animation, Parsons, and SQL systems. A catalog record supplies discovery metadata and a launch URL; it does not by itself standardize the viewer's score model or interaction events.

This confirms the distinction between a catalog, an activity description, a viewer, an execution backend, and a host that collects learning evidence. Migration to Cupcake and support for SPLICE are related but distinct integration work.

## Logging and stored data

The extension exposes optional author editing-data consent. The deployed learner code supports general `/api/v1/log` and journey-specific `/api/v1/journeys/<id>/log` routes, and local storage/IndexedDB queueing. Event context includes activity identity/type, locale, difficulty, journey context, timestamps, and query parameters. Specific events can include answers, snippets, cursor/mouse interactions, and execution results. Research consent and deployment configuration affect what is sent or retained.

When embedded with SPLICE enabled, the viewer also emits standard protocol messages. This course host receives only its iframe's messages from the expected origin, stores last score/state in browser storage, and retains the latest 500 messages for export. It does not send them to the lab or claim a production analytics/gradebook service. Browser records are editable by the learner and may contain their submitted code; they are appropriate for demonstration and formative feedback.

## What SPLICE already supports, and the observed gap

The native service emits `SPLICE.getState`, `SPLICE.sendEvent`, `SPLICE.reportScoreAndState`, and `lti.frameResize`. It is enabled with `protocol=splice`. In the deployed route, that parameter can be in the hash route query; the custom element also accepts `protocol="splice"`.

The source inspected calls getState after loading the activity but does not apply the resolved state to child exercise controls. Its score report contains event-specific state, not a universal serialized learner session. Our adapter supplies an explicit state request and restores free-coding draft/submission text into editable placeholders. The course host saves drafts from debounced codeEdited events and preserves checked scores separately. Standalone views save checked code only. Choices, puzzle arrangements, randomized variants, and in-progress annotations are not replayed. These limits are explicit in the UI and protocol documentation.

SPLICE's [working group](https://cssplice.org/slcp/index.html), [specification](https://cssplice.org/slcp/iframe-protocol-specification.html), and [live demos](https://cssplice.org/slcp/iframe-protocol-demos.html) were inspected. The demos include CodeCheck, JSAV via an adapter, JS-Parsons, and an ACOS PCEX viewer, illustrating that the protocol is independent of Cupcake's YAML.

## Course scope and reuse

The 20-module sequence follows selected readings across chapters 0–28, with optional O and F topics. Adjacent advanced chapters are combined; there is not an exercise for every LearnCpp subsection. Each module's rewritten preparation notes distinguish the ideas used in its exercises from optional deeper reading, and objectives name the actual practice. Desktop debugger operation and real file-system projects remain outside the browser exercises. Every module now has all seven activity types; two integration projects bring the count to 142.

The original course materials use the MIT license. LearnCpp content is linked, not copied, and being free to read is not treated as an open reuse license. No affiliation or endorsement by LearnCpp or the PAWS Lab is implied.
