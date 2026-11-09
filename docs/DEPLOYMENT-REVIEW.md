# Deployment review

The codebase is a Python HTTP server with a static JavaScript course host and a
vendored Cupcake 0.1.4 viewer. It loads generated YAML activities and compiles C++23
submissions using a local compiler. Canonical authoring sources live in `content/`;
`course/` and `web/course.json` are generated deliverables. No database, package
manager frontend build, external grading API, or login service is required.

## Changes made for the lab handoff

| Finding | Resolution |
| --- | --- |
| Local startup and compiler setup assumed Windows | Added a Linux Docker image containing Python 3.12 and Debian GCC 14, with actual C++23 probes and full course validation during the build. |
| Dependency ranges allowed silent changes | Added a complete version/hash lock for direct and transitive Python dependencies; local and Docker installs use the same lock. |
| Existing server assumed local origins and root paths | A deployment-only handler rebases served shell URLs under `/cupcake-lab/` and accepts the configured HTTPS proxy origin. Original application/course files remain unchanged. |
| Target uses Docker 18.09 and standalone Compose v1 | Use `docker-compose.yml` schema 2.2, a classic-builder Dockerfile, one image/build selector, and shell health polling. File validation passed with Compose 1.23.2. |
| Target naming and hosting conventions differ | Service/container `cupcake-lab__webapp`, binding `127.0.0.1:20700:5173`, directory `/home/qkw3/cupcake-lab/`, host Apache public URL with Basic auth. |
| Linux timeout cleanup killed only the immediate child | Run children in their own process group and clean up descendants even when their parent exits normally. Added Linux CPU/address-space/file-size limits through a separate launcher. |
| A program that ignored stdin could block the watchdog | Use a file for child stdin instead of a potentially blocking pipe write. |
| A fast process could exceed the output cap and exit before polling detected it | Check output size after exit as well; do not execute compiler output after an output-limit failure. |
| A read-only image could not hold temporary compilation/report files | Added bounded temporary mounts with an executable work directory and a separate report location. |
| Whole-workspace transfers would include the Windows toolchain, downloads, and caches | Added an allowlisted build context and curated source archive with checksums and a file manifest. |
| A network setting let container health pass without host port access | Corrected Compose port publishing and verified HTTP access from the host, in addition to in-container checks. |
| Viewer files are third-party assets with a pinned compatibility adjustment | Verify all 40 provenance hashes and the exact patch anchor before build/package; preserve the original files and provenance. |

The container uses a non-root UID, read-only filesystem, dropped capabilities,
no-new-privileges, memory/CPU/process limits, an init process, bounded logs, a health
check, and restart policy. No host paths or Docker socket are mounted.

## Validation

The Linux x86-64 image was built with GCC 14.2.0. The course validator passed all
142 schemas and 504 executed cases, including 60 parameter variants, 40 rejected
distractors, 20 puzzles, four permitted block permutations, 20 authored
visualizations, and negative cases for compiler errors, wrong output, timeouts,
output limits, blank starters, and wrong puzzle ordering.

Additional checks cover dependency consistency, viewer checksums, large unread
stdin, fast excessive output, descendant cleanup, JavaScript syntax, six synthetic
SPLICE message-handler checks, and six live HTTP integration checks. Host HTTP
checks also reject foreign Host headers, missing execution tokens, path traversal,
and unknown activity IDs. The running container was confirmed non-root, read-only,
healthy. The revised target mapping is `127.0.0.1:20700:5173`. The app does not
set, require or inspect Authorization headers; Basic auth is entirely in Apache.
Deployment HTTP tests also
exercise prefix-preserving/stripping mappings, proxy Host variants, configured
HTTPS origins, rebased iframe/download/asset URLs, JSVEE and HEAD requests.

Browser UI validation remains incomplete: Computer Use could not verify the
browser's current URL confidently and ended the browser check. The deployment
guide includes a manual browser launch and Check Answer step. HTTP integration
checks are not represented as a browser test.

## Limits retained deliberately

- This is a trusted-collaborator deployment. Arbitrary C++ and the web server share
  a container and writable temporary directories; it is not an adversarial-code
  sandbox. Programs have outbound network access. Use a separate isolated runner
  for untrusted learners.
- Apache routing, TLS, access control and port restrictions are provided by the
  lab administrator. No actual target-server configuration is changed here.
- The real CentOS 7 / Docker 18.09 runtime is not accessible from this workspace.
  Modern Debian syscall compatibility depends on its kernel/runc/libseccomp;
  target runtime probes in the deployment guide must pass before sign-off.
- Progress and event records remain in each browser. There is no central gradebook,
  shared learner identity, or assessment-record service. Compilation is serialized;
  a simultaneous submission receives HTTP 429 and should be retried.
- Existing upstream viewer provenance declares MIT but lacks a supplied standalone
  license text. Preserve provenance and resolve notices before public distribution.
- Python packages and the base image are locked. Debian security packages can
  advance on a fresh source build, which reruns validation. Save/load the built
  image for an identical artifact.

See [DEPLOYMENT.md](DEPLOYMENT.md) for transfer, launch, operation, and rollback.
