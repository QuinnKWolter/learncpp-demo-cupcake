# Deploy C++ Studio on adapt2

The target is the CentOS 7 host `pawscomp2.sis.pitt.edu`, with Docker **18.09.1**,
standalone **docker-compose v1**, and host Apache httpd 2.4.6 providing HTTPS.
The directory is **`/home/qkw3/cupcake-lab/`**, owned by `qkw3`. Collaborators visit
**https://adapt2.sis.pitt.edu/cupcake-lab/**; they need no SSH tunnels or server accounts.

The service/container is **`cupcake-lab__webapp`**. It binds
**`127.0.0.1:20700:5173`** so host Apache can reach it locally. Port 20700 is
intentionally not externally routable; collaborator traffic must pass through
Apache HTTPS and its Basic authentication. Port 5173 is the Python application's
actual listening port, not a Vite development server. Apache, DNS, TLS, Basic auth,
and firewall configuration remain the administrator's responsibility; this guide
does not include Apache configuration. See the legacy-Docker loopback caveat below.

## Confirmed application details

- There is **no Vite configuration or frontend build**. Python serves static HTML/JS.
- No UI fetch is hardcoded to `http://localhost:5173` or `http://127.0.0.1:5173`.
  Root-relative fetches were `/course.json`, `/api/run`, `/api/activity?id=...`, and
  `/api/teaching?id=...`. Imports, assets, navigation/history, activity iframes,
  YAML downloads, copied iframe markup, and the JSVEE loader also assumed `/`.
- The deployment-only adapter, `tools/serve_deployment.py`, rebases those **served
  responses** to `/cupcake-lab/`. Validated application files, vendor files, course
  content, and the 142-activity/504-check suite remain unchanged. JSON/YAML activity
  payloads are not rewritten and contain no backend-generated localhost launch URLs.
- The UI uses **no WebSocket or SSE connections**; no upgrade/streaming route is needed.
- The app does not set, require, or inspect the `Authorization` header, and does not
  issue `WWW-Authenticate` challenges. Apache may consume or forward its Basic auth
  header without an app-level collision. The app's separate `X-Cupcake-Local`
  execution token and Origin checks remain in place; neither is user authentication.
- Compose sets `CUPCAKE_BASE_PATH=/cupcake-lab` and
  `CUPCAKE_PUBLIC_ORIGIN=https://adapt2.sis.pitt.edu`. The adapter handles Apache
  preserving or stripping the prefix, and preserving or rewriting Host. Preserve
  the browser's Origin header. Use the canonical HTTPS URL with a trailing slash;
  the server alias is not a second configured public application origin.

## 1. Clone the repository (primary transfer route)

Repository: [QuinnKWolter/learncpp-demo-cupcake](https://github.com/QuinnKWolter/learncpp-demo-cupcake).
Initial deployment release: [v0.1.0](https://github.com/QuinnKWolter/learncpp-demo-cupcake/releases/tag/v0.1.0).
As **qkw3** on the server:

```bash
cd /home/qkw3
git clone https://github.com/QuinnKWolter/learncpp-demo-cupcake.git /home/qkw3/cupcake-lab
cd /home/qkw3/cupcake-lab
git checkout v0.1.0
docker version
docker-compose version
uname -m
docker-compose config --quiet
```

The file uses schema **2.2**, supported by standalone docker-compose **1.13+** and
Docker 18.09. This local-service schema enforces memory/CPU/PID limits without
Swarm. It has no top-level project name, profiles, plugin-only syntax, or startup
wait flags. Standalone Compose **1.23.2** was used to validate it. If the installed
v1 binary predates 1.13, the administrator must provide a compatible v1 version.

Expected layout:

```text
/home/qkw3/cupcake-lab/
  docker-compose.yml
  Dockerfile
  .gitignore
  requirements.txt
  requirements.lock
  server.py
  deploy/wait-healthy.sh
  tools/serve_deployment.py
  tools/                 # build, package and validation scripts
  content/               # canonical authoring sources
  course/                # generated YAML and course manifest
  schemas/
  web/                   # static host and bundled viewer
  docs/
  LICENSE
  README.md
```

The approximately **397 MB** `cupcake-lab-image.tar` is **not stored in Git**.
Get the matching GitHub Release attachment or scp it separately, together with its
`.sha256`. Use the versioned download URLs below. When no prebuilt image is
available, use the source-build fallback below. Source builds need Docker Hub,
Debian and PyPI access; saved-image loading/running needs no build downloads.
The prebuilt image is **Linux amd64/x86-64** and includes Python 3.12, GCC 14,
locked dependencies, viewer, schemas and all 142 activities. No host Python, Node,
compiler, VS Code extension, database, or grading API is needed.

## 2. Select one deployment mode

Keep exactly **one** active selector in `docker-compose.yml`:

```yaml
    image: ${CUPCAKE_IMAGE:-cupcake-lab:latest}  # default prebuilt-image mode
```

For source mode, replace that **single line** with:

```yaml
    build: .
```

Do not leave both selectors active. All other settings remain the same.
`CUPCAKE_IMAGE` optionally selects a versioned local image in prebuilt mode.

### Option A: prebuilt image (preferred when practical)

```bash
cd /home/qkw3/cupcake-lab
wget https://github.com/QuinnKWolter/learncpp-demo-cupcake/releases/download/v0.1.0/cupcake-lab-image.tar
wget https://github.com/QuinnKWolter/learncpp-demo-cupcake/releases/download/v0.1.0/cupcake-lab-image.tar.sha256
sha256sum -c cupcake-lab-image.tar.sha256
docker load -i cupcake-lab-image.tar
docker image inspect cupcake-lab:latest --format '{{.Os}}/{{.Architecture}} {{.Id}}'
# Leave docker-compose.yml in image: mode.
```

Use the same check/load commands for files transferred by scp. Checksum must say
`OK`, and platform must be `linux/amd64` for this server. Loading the image avoids
the host's historical BuildKit problems. The image/checksum attachments must come
from the same release as the checked-out code.

### Option B: source build (fallback when no image is available)

After changing the one selector line to `build: .`:

```bash
cd /home/qkw3/cupcake-lab
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0
docker-compose config --quiet
docker-compose build
```

The Dockerfile uses classic-builder instructions without an external BuildKit
frontend. The build checks dependencies, viewer hashes, execution controls, C++23,
all 142 activities/504 cases, and the deployment adapter. A failed check stops the
build. Allow several minutes, about 2 GiB available RAM and at least 3 GiB free
disk; retain more space if keeping multiple image versions.

## 3. Start and verify (both modes)

```bash
cd /home/qkw3/cupcake-lab
docker-compose up -d
bash deploy/wait-healthy.sh
docker-compose ps
docker-compose logs --tail=50 cupcake-lab__webapp
curl -sI http://127.0.0.1:20700/
curl --fail http://127.0.0.1:20700/cupcake-lab/api/health
docker-compose exec -T cupcake-lab__webapp python tools/verify_cpp23.py
docker-compose exec -T cupcake-lab__webapp python tools/check_local_service.py
docker-compose exec -T cupcake-lab__webapp python tools/check_deployment.py
```

The shell helper polls Docker health for up to 120 seconds and exits nonzero with
logs on failure. This replaces plugin-only wait flags. Health JSON must include
`"ok": true`, `"compiler": true`, `"standard": "c++23"`, and `"activities": 142`.
The local-service test prints six passed checks. The deployment test covers the
subpath, assets/APIs, iframe URLs, JSVEE, HEAD, proxy Host, and origin/token checks.
Complete these checks **on the real server** before opening collaborator access.

Once the administrator enables the Apache route:

```bash
curl --fail --user '<shared-username>' https://adapt2.sis.pitt.edu/cupcake-lab/api/health
```

curl prompts for the shared password; do not put it in the command or repository.
Then open **https://adapt2.sis.pitt.edu/cupcake-lab/** in a browser, authenticate to
Apache, open a module
and a free-coding exercise, submit code, and reopen it to verify saved progress.
Internal HTTP and public HTTPS checks test different parts of the deployment.

Port 20700 binds only to host IPv4 loopback. Direct external access to it is
intentionally unavailable; Apache Basic auth protects the entire `/cupcake-lab/`
route, including assets and `/api/run`. This shared C++ runner remains for the
small trusted collaborator group, with the existing container-level limits.

## Legacy-host compatibility

**Loopback binding caveat on Docker 18.09:** Docker documents that releases older
than 28 can allow same-L2 hosts to reach localhost-published ports. The requested
loopback mapping is configured, but it alone cannot establish the external-access
boundary on this old Engine. The administrator must enforce the host/network
filtering boundary and verify that 20700 cannot be reached externally, including
from the same network segment. See [Docker's port-publishing note](https://docs.docker.com/engine/network/port-publishing/).

The pinned Python 3.12 slim **Debian trixie** base and GCC 14 are unchanged. The
image builds/runs locally; runtime probes also passed with the upstream Docker
18.09 seccomp allowlist applied on a modern host. That is **not** an emulation of
CentOS 7's kernel, old runc, or old libseccomp. The actual server has not been tested
from this workspace.

Modern Debian can encounter syscall/seccomp incompatibilities on old Docker hosts;
see the [Docker Official Images compatibility reference](https://github.com/docker-library/official-images/issues/16829).
If the target reports thread-creation failures, `Operation not permitted`, package
signature errors, or similar problems, retain the logs and have the administrator
check Docker/runc/libseccomp compatibility. Loading a prebuilt image bypasses build
failures, but cannot correct a runtime/kernel incompatibility. A failed target probe
means the deployment is not ready. No relaxed security profile is shipped as a workaround.

## Persistence, disk and resources

| Item | Persistence and expected usage |
| --- | --- |
| App/course/viewer | In the image; survives restarts. Saved tar is about 397 MB. Reserve about 0.5 GiB per installed image, plus the downloaded tar and build cache. Shared layers reduce extra version storage. Inspect exact size with `docker image inspect cupcake-lab:latest --format '{{.Size}}'`. |
| Source | About 8 MB unpacked deployable source plus Git history; source tarball about 3.6 MB. Windows toolchains/research downloads are excluded. |
| Named volumes / bind mounts | **None.** No host mount directories, ownership fixes, or SELinux bind-mount relabeling are required. |
| Compiler work | Executable `/app/.runtime` tmpfs capped at 256 MiB; cleaned per execution and temporary across container lifecycle. |
| Temporary files/reports | `/tmp` tmpfs capped at 64 MiB; reports at `/tmp/cupcake-reports` are temporary. Build evidence stays in the image at `/app/research`. |
| Learner state | Drafts, scores and events persist in each browser's local storage. No central database/gradebook. Moving from localhost to adapt2 does not automatically migrate browser state; export it beforehand. |
| Logs | Docker JSON logs rotate at 10 MB/file, three files (about 30 MB plus overhead). Restarts retain them; container recreation/removal can discard them. |

Runtime is non-root UID/GID 10001, read-only root filesystem, dropped capabilities,
no-new-privileges, an init process, and 1 GiB RAM/two CPU/64 PID limits. Tmpfs use
counts toward memory. Actual enforcement depends on the target kernel/cgroups.
The configured policy is **`restart: unless-stopped`**: the service restarts after
host/Docker restarts when Docker starts on boot, while intentional stops remain
stopped until explicitly started again. An
unhealthy status alone does not restart a process. One submission compiles at a
time; simultaneous requests receive HTTP 429 and can retry. Compiled code shares
the web container and can access the network; use trusted collaborators only.

## Updates

Save both the code revision and actual image before updating:

```bash
cd /home/qkw3/cupcake-lab
git rev-parse HEAD > /home/qkw3/cupcake-lab-previous.commit
docker tag "$(docker inspect --format '{{.Image}}' cupcake-lab__webapp)" cupcake-lab:previous
# For the initially checked-out release tag, return to main before pulling:
git checkout main
git pull --ff-only
```

In source mode, the selector edit makes `docker-compose.yml` locally modified.
Before pulling, save a copy outside the repo and use
`git checkout -- docker-compose.yml`; after pulling, reapply `build: .` and any
other saved local settings. Default image mode needs no tracked-file edit.

Next, either verify and load the new image, or build from the updated source:

```bash
# Prebuilt mode:
docker load -i cupcake-lab-image.tar

# OR source mode with build: . selected:
DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 docker-compose build

# Common:
docker-compose up -d
bash deploy/wait-healthy.sh
docker-compose exec -T cupcake-lab__webapp python tools/check_local_service.py
```

Download/copy the new archive first and verify its checksum. Keep source and image
from the **same release**. `up -d` recreates services whose configuration/image
changed. If `CUPCAKE_IMAGE` selects a version tag, update it to the newly loaded tag.
Editing host source alone does not change a running image.

For longer retention than the moving `previous` slot, use explicit image tags:

```bash
docker tag "$(docker inspect --format '{{.Image}}' cupcake-lab__webapp)" cupcake-lab:2026-11-09-r1
```

Publish a matching Git tag, image attachment and checksum per release; record its
commit and image ID. Do not delete old images until their rollback window closes.

## Rollback

```bash
cd /home/qkw3/cupcake-lab
git checkout <previous-git-tag-or-commit>
# Ensure docker-compose.yml uses image: mode, not build: .
export CUPCAKE_IMAGE=cupcake-lab:previous
docker-compose up -d
bash deploy/wait-healthy.sh
docker-compose exec -T cupcake-lab__webapp python tools/check_local_service.py
```

Alternatively check out `"$(cat /home/qkw3/cupcake-lab-previous.commit)"`. A versioned
image can be selected with `CUPCAKE_IMAGE=cupcake-lab:<release-tag>`. Put that selection
in an ignored `.env` file if it must survive a fresh login. Unset/update it when
returning to `latest`. Source-only rollback means checking out the older code,
selecting `build: .`, rebuilding, and starting. Preserve local settings before a
checkout. Browser state is not erased, although changed activity IDs/regions can
affect saved-work compatibility.

## Tarball alternative / air-gapped transfer

On the Windows build machine:

```powershell
Set-Location D:\Cupcake
python tools/package_deployment.py
scp exports/cupcake-lab-deploy.tar.gz exports/cupcake-lab-deploy.tar.gz.sha256 qkw3@pawscomp2.sis.pitt.edu:/home/qkw3/
scp exports/cupcake-lab-image.tar exports/cupcake-lab-image.tar.sha256 qkw3@pawscomp2.sis.pitt.edu:/home/qkw3/
```

For an initial installation with no existing destination, on the server:

```bash
cd /home/qkw3
sha256sum -c cupcake-lab-deploy.tar.gz.sha256
tar -xzf cupcake-lab-deploy.tar.gz -C /home/qkw3
sha256sum -c cupcake-lab-image.tar.sha256
docker load -i cupcake-lab-image.tar
cd /home/qkw3/cupcake-lab
docker-compose up -d
bash deploy/wait-healthy.sh
```

Continue with the common verification steps. A fully air-gapped host needs **both**
source tarball and prebuilt image; source alone cannot download build dependencies.
The tarball excludes Git history: retain archived source directories and matching
tagged images for rollback. Do not extract updates over a Git checkout; use one
source-management route per installation. The older `cpp-course-cupcake.zip` is
activities only and cannot deploy the app.

To publish a new image from the modern build machine:

```powershell
docker build -t cupcake-lab:latest .
docker save -o exports/cupcake-lab-image.tar cupcake-lab:latest
$imageHash = (Get-FileHash exports/cupcake-lab-image.tar -Algorithm SHA256).Hash.ToLower()
"$imageHash  cupcake-lab-image.tar" | Set-Content -Encoding ascii exports/cupcake-lab-image.tar.sha256
```

## Operations and troubleshooting

From `/home/qkw3/cupcake-lab/` with approved Docker access:

```bash
docker-compose logs --tail=100 cupcake-lab__webapp
docker-compose restart cupcake-lab__webapp
docker-compose stop cupcake-lab__webapp
docker-compose up -d
```

| Symptom | Action |
| --- | --- |
| Compose rejects file | Confirm v1 >=1.13; run `docker-compose config --quiet`. |
| Image missing / attempted registry pull | Load `cupcake-lab:latest` first, or select source mode and build. No public registry image is assumed. |
| BuildKit error | Prefer saved image; otherwise use classic-builder environment settings above. |
| Syscall/thread permission failures | Run target probes and inspect logs; see legacy-host compatibility. |
| Port 20700 allocated | Have the administrator resolve the conflicting listener. |
| Host health works but HTTPS fails | Administrator checks Apache route/TLS/access configuration. |
| Assets/API fail | Check canonical `/cupcake-lab/` URL, trailing slash and public origin; test public subpath health. |
| Submission HTTP 403 | Preserve browser Origin and use configured HTTPS origin; arbitrary alternate origins are rejected. |
| HTTP 429 | Another compilation is active; retry when it finishes. |

Original license and viewer provenance remain included. The installed extension
declared MIT but supplied no standalone upstream license text; preserve provenance
and resolve notices before public redistribution. LearnCpp readings are linked,
not copied.
