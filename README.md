# C++ Studio with Cupcake

**Lab deployment:** [https://adapt2.sis.pitt.edu/learncpp-demo-cupcake/](https://adapt2.sis.pitt.edu/learncpp-demo-cupcake/)
is the intended Apache HTTPS route. See [the deployment guide](docs/DEPLOYMENT.md)
for CentOS 7, Docker 18.09.1 and standalone docker-compose v1. The public route is
configured by the server administrator; this repository does not provision Apache.
The container includes Python, GCC, dependencies, course content and the viewer.

## Clone and deploy

As `qkw3` on the server:

```bash
git clone https://github.com/QuinnKWolter/learncpp-demo-cupcake.git /home/qkw3/learncpp-demo-cupcake
cd /home/qkw3/learncpp-demo-cupcake
git checkout v0.1.1
```

Expected layout is one repository with `docker-compose.yml`, `Dockerfile`,
`server.py`, `requirements.lock`, `web/`, `course/`, `content/`, `schemas/`,
`tools/`, `deploy/`, and `docs/` at its root. The service/container is
`learncpp-demo-cupcake__webapp`, bound as `127.0.0.1:20700:5173` for host Apache.

The roughly 397 MB **prebuilt image is not stored in Git**. When available, obtain
`learncpp-demo-cupcake-image.tar` and its checksum from [release v0.1.1](https://github.com/QuinnKWolter/learncpp-demo-cupcake/releases/tag/v0.1.1) or a
separate scp transfer, then use the default `image:` mode:

```bash
sha256sum -c learncpp-demo-cupcake-image.tar.sha256
docker load -i learncpp-demo-cupcake-image.tar
docker-compose up -d
bash deploy/wait-healthy.sh
```

**When no prebuilt image is available, building from source is the fallback:** replace the single
`image:` selector line with `build: .`, then run:

```bash
DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 docker-compose build
docker-compose up -d
bash deploy/wait-healthy.sh
```

Do not keep both selectors active. The guide covers host/runtime verification,
the `/learncpp-demo-cupcake/` adapter, state, updates, rollback and the alternative
`exports/learncpp-demo-cupcake-deploy.tar.gz` transfer. Modern Debian on the legacy host still
requires the documented real-server runtime checks before deployment sign-off.

## Local authoring

Open **http://127.0.0.1:5173** while the server is running.

```powershell
cd D:\Cupcake
python server.py
```

The course contains **20 modules and 142 native Cupcake activities**, including two capstones. It follows selected [LearnCpp readings](https://www.learncpp.com/) from introductory programming through templates, ownership, polymorphism, exceptions, and streams. The exercises and local runner target **C++23**, verified with a workspace-local GCC 16.2 toolchain. See the [teaching and standard review](docs/CXX23-REVIEW.md).

Every module has preparation notes and all seven activity types: worked example, authored step-through visualization, Parsons puzzle, completion, multiple choice, parameterized tracing, and free coding. Each assessed activity has progressive hints, reasoned feedback, and explained input/output examples. Tests are visible, formative practice.

## Use it

1. Read **Read & Connect**, then use the linked LearnCpp pages for further depth.
2. Open **Worked example** and click the annotated source regions; use **Step through** to follow changing values.
3. Try **Arrange code**, **Fill gaps**, **Explain why**, **Predict output**, and **Write code**. Each activity explains its controls and goal.
4. Click **Check Answer** to run real C++ or grade the conceptual question.
5. Open **SPLICE inspector** to see score, state, event, and resize messages.
6. Use **Export progress** or **Export events** to download local records.

The first capstone follows module 14; the second follows module 20. Navigation suggests prerequisites without locking access. Worked examples and step-throughs use an explicit self-review mark, separate from assessed grades.

Revised progress uses `cupcake-cpp23-studio-v2`; the previous course's storage is preserved separately. In the course host, free-coding drafts save after a short pause and are restored on reopening. Checked scores remain distinct from edits. Completion choices, puzzle arrangements, and trace variants start a fresh attempt; previous scores remain visible. Standalone activities restore checked code only, using separate storage. See [SPLICE details](docs/SPLICE.md).

## Files

| Location | Purpose |
| --- | --- |
| `course/activities/` | 142 self-contained Cupcake YAML files, each with the official activity `$schema` |
| `course/course.yaml` | Our course sequencing manifest; **not** an upstream Cupcake Journey schema |
| `course/README.md` | Complete notes, reading links, and activity index |
| `course/solutions.json` | Author reference implementations for editable regions |
| `content/modules/*.yaml`, `content/projects.yaml` | Canonical sources of lessons, activities, explanations, and tests |
| `content/course_data.py` | Loader for the canonical YAML authoring sources |
| `web/` | Local course host, guidance adapter, and vendored Cupcake viewer assets |
| `schemas/` | Schemas copied from the installed Cupcake 0.1.4 extension |
| `tools/` | Rebuild, compiler adapter, validation, and packaging tools |
| `docs/INVESTIGATION.md` | Findings about Cupcake, the catalog, packaging, execution, and logging |
| `docs/SPLICE.md` | Protocol implementation, launch instructions, state format, and limits |
| `docs/AUTHORING.md` | Editing in VS Code and moving activities into a lab deployment |
| `docker-compose.yml`, `Dockerfile`, `deploy/` | Legacy-host deployment and startup health polling |
| `tools/serve_deployment.py` | Apache origin and subpath adapter; original app files stay intact |
| `docs/DEPLOYMENT.md` | Transfer, launch, operations and rollback |
| `research/` | Local generated/research evidence; excluded from Git and deployment archives |

## Requirements and checks

Python 3.11+, PyYAML, jsonschema, and a C++23 compiler. The pinned portable compiler is preferred from `.tools/gcc/mingw64/bin/g++.exe`; set `CUPCAKE_CXX` to select another executable. The setup script installs only inside this workspace and records its source and digest.

```powershell
python -m pip install -r requirements.txt
python tools/setup_compiler.py
python tools/verify_cpp23.py
python tools/build_course.py
python tools/validate_course.py
node tools/check_splice_state.mjs
python tools/check_local_service.py
python tools/package_course.py
```

Install dependencies only if missing. Rebuilding uses the compiler to capture example output. Validation checks schemas and locations, compiles every solution, checks every test, tries all parameter variants, rejects distractors, and probes compilation errors, wrong output, timeouts, output limits, and blank starters.

The bundled viewer comes from the installed **Cupcake Activity Authoring for VS Code 0.1.4** extension. Its files and hashes remain intact; `server.py` applies one exact-match, response-only compatibility adjustment so unchanged/restored free code can be checked. Guidance and resizing live in our adapter. See [review details](docs/CXX23-REVIEW.md). Provenance is recorded in `web/vendor/cupcake/PROVENANCE.json`; `python tools/setup_vendor.py` recopies the installed bundle.

## Execution boundary

Direct `python server.py` use is a **trusted local demo**, bound to `127.0.0.1` by default. Compiled programs run with your user's permissions. The [Docker deployment](docs/DEPLOYMENT.md) serves trusted collaborators through host Apache Basic auth at `/learncpp-demo-cupcake/`, using a non-root container and resource limits. Port 20700 binds only to host loopback; the guide records the additional filtering verification needed on Docker 18.09. The app does not use the Authorization header. Timeouts, output limits, and a shared container are **not an adversarial-code security sandbox**. Untrusted learners need a separate sandboxed execution service. Progress remains browser-local; there are no shared server-held assessment records. The original YAML remains usable with Cupcake's own execution infrastructure.

No course content was uploaded to or registered in the lab's Cupcake/catalog installations. No lab credentials are copied into this project. The demo blocks remote execution and telemetry calls; LearnCpp links open external readings only when visited.

The lessons and exercises here are original. LearnCpp is free to read; that does not establish an open redistribution license for its text. This package links to its lessons without republishing them. `LICENSE` covers only the original materials in this workspace; the upstream viewer has separate provenance and notices.
