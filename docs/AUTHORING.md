# Authoring and deploying this course

## In the VS Code instance already open

Open any file under `D:\Cupcake\course\activities`, for example `01-first-programs\free-coding.yaml`.

Use these commands from the Command Palette:

1. **Cupcake: Open in GUI Editor** for visual editing.
2. **Cupcake: Edit Metadata & Files** to inspect identity, language, and embedded source.
3. **Cupcake: Open as Raw YAML** for precise snippet and schema edits.
4. **Cupcake: Preview Activity** for the extension's native student preview.
5. **Cupcake: Show Activity Tutorial** for the activity-specific format.

The extension may ask its own optional editing-data consent question. Choose according to your research preferences; this project does not change that preference. The extension's hosted Run/Check functions require Cupcake sign-in. The local course's compiler bridge works only in its own browser host and does not change the extension's authentication model.

Each activity's `$schema` refers to the official versioned URI. Offline copies of those exact installed schemas live in `schemas/`. No global VS Code setting, account token, or TLS setting was changed.

## Edit and rebuild

`content/modules/*.yaml` and `content/projects.yaml` are the maintainable source of truth. They contain preparation notes, objectives, readings, reference programs, per-type hints, choice explanations, puzzle blocks, editable regions, input contracts, and the purpose of each test. `content/course_data.py` loads them. `tools/build_course.py` emits the learner packages and captures example outputs using the C++23 compiler.

```powershell
python tools/build_course.py
python tools/validate_course.py
```

Direct edits to generated activity YAML are useful for GUI experimentation but will be overwritten by a rebuild. Move durable changes into the canonical content YAML. Keep IDs stable only when old saved state remains compatible. This revision uses new `cpp23-v2-` IDs and a separate browser storage key. `tools/revise_course_content.py` records the one-time editorial migration from the preserved v1 source; do not rerun it over later authoring edits.

When adding an exercise:

- Use `runtime.language: cpp` and version `'23'`, and run `tools/verify_cpp23.py` after changing the compiler.
- Embed one `main.cpp` under source. Optional local `.h`/`.hpp` includes are supported by this demo.
- Keep each snippet unique, or use a deliberate context/occurrence.
- Ensure editable and block locations do not overlap.
- Provide at least one test that distinguishes each plausible wrong implementation.
- Use bounded, fully described inputs and deterministic output.
- Explain all supplied helpers and unfamiliar syntax in the preparation notes before requiring learners to use them.
- Give progressive hints that suggest reasoning, and explain the mistaken idea behind each distractor.
- Maintain all seven activity types per module. Keep traces' expected outputs independently authored, and align each visualization state with a source line and an explanation.
- Do not include an authored status field on graded test cases; pass/fail comes from execution.

The local runner is a course-specific adapter. It supports the snippet/context/occurrence locations used here, inline main.cpp plus local headers, and these activity/test shapes. It does not implement arbitrary external paths, extends chains, multiple translation units, or every language. The twenty C++ macro visualizations use manually authored JSVEE state actions; the upstream automatic generator remains Python-specific. The displayed state is a teaching model, not a physical memory layout or debugger recording.

The local adapter adds guidance, visible supporting headers, explained samples, pre-submission hints, and document-sized iframe resizing. The server also applies an exact-match response-only adjustment to the pinned free-coding viewer so learners can check restored or unchanged code. Vendored asset files and hashes remain intact. These local host features do not automatically accompany YAML imported into another deployment; native YAML still includes the activity statement, hints, and explanations. See `docs/CXX23-REVIEW.md` for the compatibility boundary.

## Move to the lab infrastructure

To run this complete app for trusted collaborators on a Linux server, follow
[the Docker/Apache deployment guide](DEPLOYMENT.md). The activity-only catalog export
below is a separate route for an existing Cupcake installation.

Run `python tools/package_course.py` to create `exports/cpp-course-cupcake.zip`. It contains native YAML, the reading/lesson index, the explicitly custom course manifest, and license/provenance notes. It excludes the local runner, browser runtime data, research downloads, and solutions.json. The reference source is necessarily embedded in the native activity packages; this is an authoring distribution, not a secret-answer assessment format.

The deployed Cupcake activity catalog uses GitHub-backed repositories. Arrange the activity folders in a lab-authorized repository, register/synchronize that repository through the deployment's normal authoring administration, then verify the public/private visibility and resulting launch URLs. This investigation did not establish or invoke a supported unauthenticated upload API, so there is no fabricated automatic import command.

The course manifest is **not** a validated Cupcake Journey definition. To use the deployment's Journey feature, map these modules/lessons to the Journey format supported by that deployment, or use the supplied browser course host. Individual YAML files already conform to their native activity schemas.

For SLC catalog registration, create records through the normal authorized catalog workflow with activity titles, language/domain, topics, activity type, license, and the verified launch URLs. Catalog registration and hosting are distinct steps. The original task authorized creating a testable course, and no remote catalog writes have been made.

For an untrusted learner installation, use the lab's sandboxed execution backend or another isolated service. The trusted-collaborator Docker deployment binds `127.0.0.1:20700:5173` for host Apache and serves `/cupcake-lab/` through a deployment adapter. The administrator manages Apache Basic auth and verifies the legacy host's external port restrictions as described in the deployment guide. Do not deploy server.py directly on a public interface. Local time/output limits, token checks, and an execution mutex do not prevent C++ code from calling OS APIs with the runner user's permissions.

## Content provenance

The code and teaching prose authored here are original and MIT licensed. LearnCpp links are mapped to its current lesson URLs, including renamed constants, vector, and range-loop pages. The course uses selected readings across the chapter progression, not copied chapters or quizzes. Review assessment wording and topic depth with an instructor before using it as a graded course.

The copied Cupcake extension declares MIT in package.json. Its installed distribution did not include a standalone upstream license text. `PROVENANCE.json` records that fact and hashes all copied viewer assets. Confirm upstream notices before publishing a redistributed viewer bundle; individual original course YAML can be hosted by an existing Cupcake deployment without distributing our local viewer copy.
