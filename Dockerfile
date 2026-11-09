# Compatible with the classic Docker 18.09 builder; no BuildKit frontend required.
FROM python:3.12-slim-trixie@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CUPCAKE_CXX=/usr/bin/g++ \
    CUPCAKE_RUNTIME_DIR=/app/.runtime \
    CUPCAKE_REPORT_DIR=/tmp/cupcake-reports
WORKDIR /app

# Debian trixie's GCC 14 includes the C++23 language/library features used here.
RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 cupcake \
    && useradd --uid 10001 --gid 10001 --no-create-home cupcake
COPY requirements.lock ./
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.lock \
    && python -m pip check

COPY server.py LICENSE ./
COPY tools/ tools/
COPY content/ content/
COPY course/ course/
COPY schemas/ schemas/
COPY web/ web/
RUN mkdir -p .runtime research \
    && chown cupcake:cupcake .runtime research
USER 10001:10001
# Fail the build for missing/changed vendor assets, invalid content or a compiler mismatch.
RUN python tools/check_installation.py \
    && python tools/check_execution.py \
    && python tools/validate_course.py \
    && python tools/check_deployment.py \
    && cp /tmp/cupcake-reports/*.json research/

EXPOSE 5173
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "tools/healthcheck.py"]
CMD ["python", "tools/serve_deployment.py"]
