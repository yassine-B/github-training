# Lesson 43 — Advanced Docker Builds, Container Registries & Release Engineering

**Level:** Advanced
**Category:** Real-world CI/CD project
**Focus:** Docker, BuildKit, Buildx, GHCR, container security, image supply chain, deployment automation, and release engineering.

---

## 1. Lesson overview

In Lesson 42, we studied advanced GitHub Actions architecture:

- Reusable workflows.
- Composite Actions.
- Custom JavaScript and Docker Actions.
- Workflow orchestration.
- Centralized CI/CD.
- Workflow inputs, outputs, and secrets.
- Enterprise automation architecture.

Now we move to the next stage: **building a production-grade container delivery pipeline.**

A professional CI/CD system should do more than execute tests. It should also:

1. Build reproducible Docker images.
2. Optimize image size and build performance.
3. Scan images for vulnerabilities.
4. Generate software supply-chain metadata.
5. Publish images to a container registry.
6. Identify releases using immutable references.
7. Deploy verified images to environments.
8. Monitor deployment health.
9. Support safe rollback and recovery.

We will use a realistic application architecture based on Django REST Framework, React, PostgreSQL, Docker, and Nginx.

### 1.1 What you will build

Imagine a repository containing a restaurant-management platform:

```text
restaurant-platform/
│
├── backend/
│   ├── config/
│   ├── apps/
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
│
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── kubernetes/
│
├── helm/
│
├── docker-compose.yml
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── docker-build.yml
        ├── docker-security.yml
        ├── docker-publish.yml
        ├── deploy-staging.yml
        └── deploy-production.yml
```

The objective is to automate this delivery process:

```text
Developer pushes code
        |
        v
GitHub Actions CI
        |
        v
Python and React tests
        |
        v
Docker image builds
        |
        v
Security verification
  - Trivy
  - SBOM
  - Provenance
        |
        v
Publish images to GHCR
        |
        v
Record image digests
        |
        v
Deploy verified images
        |
        v
Development -> Staging -> Production
        |
        v
Health checks and release verification
```

### 1.2 Complete Lesson 43 curriculum

| # | Topic |
|---:|---|
| 1 | Docker image architecture and layers |
| 2 | Production Dockerfiles |
| 3 | Multi-stage Docker builds |
| 4 | Docker BuildKit |
| 5 | Docker Buildx |
| 6 | GitHub Container Registry (GHCR) |
| 7 | Docker image naming conventions |
| 8 | Semantic image tagging |
| 9 | Immutable image digests |
| 10 | Docker layer caching |
| 11 | GitHub Actions cache backend |
| 12 | Multi-platform builds |
| 13 | Container vulnerability scanning |
| 14 | Trivy integration |
| 15 | Software Bill of Materials (SBOM) |
| 16 | Container image signing |
| 17 | Image provenance and attestations |
| 18 | Secure image publishing |
| 19 | Docker Compose deployment |
| 20 | SSH-based deployment architecture |
| 21 | Self-hosted deployment runners |
| 22 | Kubernetes deployment workflows |
| 23 | Helm chart deployment |
| 24 | Blue-green deployment |
| 25 | Canary deployment |
| 26 | Rollback automation |
| 27 | Database migrations |
| 28 | Deployment health checks |
| 29 | Release management |
| 30 | Complete Django + React production pipeline |

---

## 2. Docker image architecture

Before writing GitHub Actions workflows, understand what we are actually building.

A Docker image is a packaged filesystem and execution configuration used to create containers.

For example, a Django backend image may contain:

```text
Backend Docker Image
│
├── Base image
│   └── Python runtime
│
├── System dependencies
│
├── Python dependencies
│   ├── Django
│   ├── Django REST Framework
│   ├── Gunicorn
│   └── Other packages
│
├── Application source
│
└── Startup configuration
    └── Gunicorn
```

A React frontend image may contain:

```text
Frontend Docker Image
│
├── Nginx runtime
│
└── Static frontend files
    ├── index.html
    ├── assets/
    └── application bundles
```

The frontend build environment does not necessarily need to be included in the final image.

### 2.1 Image versus container

| Docker image | Docker container |
|---|---|
| Application package | Running instance |
| Immutable template | Runtime instance |
| Stored in a registry | Runs on a Docker host |
| Identified by tags and digests | Has a container ID |
| Can create multiple containers | Executes application processes |

Think of an image as the packaged application and a container as an instance created from that package.

### 2.2 Understand Docker image layers

Consider this Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]
```

Docker builds an image using filesystem changes and image configuration.

Conceptually:

```text
Application image
│
├── Application source layer
│
├── Python dependencies layer
│
├── Base image filesystem
│
└── Image configuration
```

Docker can reuse unchanged build layers during subsequent builds.

For example:

- You change a React component.
- The backend dependencies have not changed.
- The backend dependency layer does not need to be rebuilt.
- The frontend build may need to run again.

This is one reason Dockerfile instruction ordering matters.

**Important distinction:** Filesystem layers and image configuration metadata are different parts of the image model. The diagram is conceptual, not a literal representation of every OCI image component.

### 2.3 Inspect image layers

Build an image:

```powershell
docker build -t restaurant-backend:training `
  -f docker/backend.Dockerfile .
```

Inspect it:

```powershell
docker image inspect restaurant-backend:training
```

Show image history:

```powershell
docker history restaurant-backend:training
```

List images:

```powershell
docker images
```

Questions to investigate:

1. Which layers consume the most space?
2. Which Dockerfile instructions created those layers?
3. What happens when you change `requirements.txt`?
4. What happens when you only change application source code?

---

## 3. Production Dockerfiles

A production Dockerfile should prioritize:

- Small image size.
- Reproducible dependencies.
- Non-root execution.
- Minimal runtime dependencies.
- Correct process and signal handling.
- No embedded credentials.
- Separation between build and runtime environments.
- Predictable configuration.

A Dockerfile that works locally is not automatically production-ready.

### 3.1 Django production Dockerfile

Create:

`docker/backend.Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install application dependencies
FROM base AS dependencies

COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir \
    -r requirements.txt

# Production runtime
FROM base AS production

RUN addgroup --system app \
    && adduser --system --ingroup app app

COPY --from=dependencies \
    /usr/local/lib/python3.12/site-packages \
    /usr/local/lib/python3.12/site-packages

COPY --from=dependencies \
    /usr/local/bin \
    /usr/local/bin

COPY --chown=app:app backend/ /app/

USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3"]
```

Adjust `config.wsgi` to match your Django project.

This example assumes the dependencies are compatible with the selected Python image. Packages requiring native compilation or operating-system libraries may require an additional build-dependencies stage.

**Production considerations:**

- Use a tested Python version.
- Pin application dependencies appropriately.
- Configure Django's `DEBUG=False`.
- Supply `SECRET_KEY` through runtime secrets.
- Configure `ALLOWED_HOSTS`.
- Configure database connectivity.
- Configure static files and media storage.
- Use a proper health endpoint.
- Configure worker count according to the deployment environment.

Do not put production credentials into the Dockerfile.

### 3.2 React production Dockerfile

Create:

`docker/frontend.Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM node:22-alpine AS builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci

COPY frontend/ ./

RUN npm run build

# Production runtime
FROM nginx:alpine AS production

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

For Vite, the default build output is `dist/`.

For Next.js or another framework, the runtime image and output configuration will differ.

### 3.3 Create `.dockerignore`

A `.dockerignore` file prevents unnecessary files from entering the build context.

Create a root `.dockerignore`:

```text
.git
.github
.vscode
.idea

**/__pycache__
**/*.pyc
**/.pytest_cache
**/.venv
**/venv

**/node_modules
**/dist
**/build

.env
.env.*
!.env.example

*.log
coverage
```

Adapt this file to your build context.

Do not exclude files required by your Docker build. For example, if your frontend Dockerfile needs `package-lock.json`, do not exclude it.

Why does this matter?

- Smaller build contexts.
- Faster uploads to the builder.
- Less accidental inclusion of local files.
- Lower risk of copying local secrets into images.

### 3.4 Build and run locally

Build the backend:

```powershell
docker build `
  -f docker/backend.Dockerfile `
  -t restaurant-backend:local .
```

Build the frontend:

```powershell
docker build `
  -f docker/frontend.Dockerfile `
  -t restaurant-frontend:local .
```

Inspect:

```powershell
docker images

docker image inspect restaurant-backend:local
```

Run:

```powershell
docker run --rm -p 8000:8000 restaurant-backend:local

docker run --rm -p 8080:80 restaurant-frontend:local
```

Open:

```text
http://localhost:8080
```

The backend requires its database and environment configuration. A container that builds successfully may still fail at runtime if those dependencies are missing.

---

## 4. Multi-stage Docker builds

Multi-stage builds allow you to use different stages for building and running an application.

For example:

```text
Stage 1: Dependencies
        |
        v
Stage 2: Application build
        |
        v
Stage 3: Production runtime
        |
        v
Final image
```

### 4.1 Why multi-stage builds matter

| Single-stage build | Multi-stage build |
|---|---|
| Build tools may remain in the final image | Build tools can be excluded |
| Often larger | Usually smaller |
| More runtime dependencies | Smaller runtime dependency set |
| Less separation | Clear build/runtime separation |

Consider a React application.

The build process needs Node.js and npm. The production application can be served by Nginx without including the Node.js build environment.

### 4.2 Django multi-stage example

The previous backend Dockerfile already separates dependency installation from the final runtime.

You can extend this pattern when native dependencies need compilation:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip wheel \
    --no-cache-dir \
    --wheel-dir /wheels \
    -r requirements.txt

FROM python:3.12-slim AS production

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install \
    --no-cache-dir \
    --no-index \
    --find-links=/wheels \
    /wheels/* \
    && rm -rf /wheels

COPY backend/ .

RUN addgroup --system app \
    && adduser --system --ingroup app app

USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

This is a teaching example. Native runtime libraries required by compiled Python packages must also be present in the final image.

### 4.3 Inspect the final image

Build both versions and compare:

```powershell
docker images
```

Record:

- Image size.
- Number of layers.
- Build duration.
- Runtime dependencies.
- Included build tools.

**Exercise:** Create a single-stage and multi-stage frontend image. Compare their sizes and explain the differences.

---

## 5. Docker BuildKit

BuildKit is Docker's modern build engine.

It provides:

- Improved build performance.
- Parallel build execution.
- Advanced cache management.
- Build secrets.
- Build mounts.
- Multi-platform builds.
- Build attestations.

### 5.1 BuildKit architecture

BuildKit evaluates build instructions and dependencies using a build graph.

It can avoid executing unnecessary stages and can reuse cached build results.

For example:

```dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

FROM base AS dependencies

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

FROM base AS production

COPY --from=dependencies \
    /usr/local/lib/python3.12/site-packages \
    /usr/local/lib/python3.12/site-packages

COPY backend/ .
```

BuildKit can target a specific stage:

```powershell
docker buildx build `
  --target dependencies `
  -f docker/backend.Dockerfile .
```

### 5.2 BuildKit build command

```powershell
docker buildx build `
  --file docker/backend.Dockerfile `
  --tag restaurant-backend:latest `
  --load `
  .
```

### 5.3 BuildKit secret mounts

Never put credentials directly into Dockerfile instructions.

Avoid:

```dockerfile
ARG API_TOKEN

RUN echo "$API_TOKEN"
```

Build arguments are not designed to be secret storage. Values may appear in build metadata, logs, or other places depending on how they are used.

Instead, use BuildKit secret mounts.

Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN --mount=type=secret,id=pip_config,target=/etc/pip.conf \
    pip install --no-cache-dir -r requirements.txt
```

Build command:

```powershell
docker buildx build `
  --secret id=pip_config,src=./pip.conf `
  -f docker/backend.Dockerfile `
  .
```

This is useful when accessing private Python package indexes.

The secret is exposed to the relevant build instruction rather than deliberately copied into the image filesystem.

### 5.4 BuildKit cache mounts

BuildKit can also mount cache directories to speed up package installation.

Example:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

This cache is a build optimization. It is not a replacement for dependency locking or reproducible builds.

---

## 6. Docker Buildx

Buildx is an extended Docker CLI interface that uses BuildKit.

You will use it frequently in GitHub Actions.

### 6.1 Inspect Buildx

```powershell
docker buildx version

docker buildx ls

docker buildx inspect
```

### 6.2 Create a builder

```powershell
docker buildx create `
  --name training-builder `
  --driver docker-container `
  --use
```

Bootstrap it:

```powershell
docker buildx inspect --bootstrap
```

### 6.3 Build with Buildx

```powershell
docker buildx build `
  --platform linux/amd64 `
  --file docker/backend.Dockerfile `
  --tag restaurant-backend:training `
  --load `
  .
```

The `--load` option loads a compatible build result into the local Docker image store.

### 6.4 Build multiple platforms

```powershell
docker buildx build `
  --platform linux/amd64,linux/arm64 `
  --file docker/backend.Dockerfile `
  --tag restaurant-backend:training `
  --push `
  .
```

The registry receives a multi-platform image index that references platform-specific images.

Multi-platform builds often require a registry push rather than loading the result into the classic local Docker image store.

### 6.5 Understand the platforms

| Platform | Typical environment |
|---|---|
| `linux/amd64` | Most x86-64 servers and PCs |
| `linux/arm64` | ARM64 servers and devices |
| `linux/arm/v7` | Certain older ARM devices |

Your deployment hardware determines which architecture you need.

**Exercise:** Build an AMD64 image and inspect its platform metadata. Then publish a multi-platform image and inspect the image index.

---

## 7. GitHub Container Registry (GHCR)

GHCR is GitHub's container registry.

It stores container images associated with GitHub accounts and organizations.

Registry address:

```text
ghcr.io
```

Example:

```text
ghcr.io/your-owner/restaurant-backend:1.0.0
```

### 7.1 Understand image naming

```text
ghcr.io/OWNER/IMAGE:TAG
```

| Component | Example | Meaning |
|---|---|---|
| Registry | `ghcr.io` | GitHub Container Registry |
| Owner | `your-owner` | Account or organization |
| Image | `restaurant-backend` | Image name |
| Tag | `1.0.0` | Image version |

Use your actual GitHub owner rather than copying the example owner.

### 7.2 Create a GHCR package

You do not necessarily need to create the package manually.

Publishing a new image can create its associated package.

You can subsequently find it under the GitHub account or organization Packages section.

### 7.3 Authenticate locally

For local training, authenticate with a suitable GitHub token stored securely.

```powershell
docker login ghcr.io -u YOUR_GITHUB_USERNAME
```

Docker will prompt for the password.

Use a token with the appropriate package permissions:

- Package write permission for publishing.
- Package read permission for pulling private images.

Never commit the token or place it in a Dockerfile.

### 7.4 Build and publish manually

```powershell
docker build `
  -f docker/backend.Dockerfile `
  -t ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0 .

docker push ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
```

Pull:

```powershell
docker pull ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
```

Inspect:

```powershell
docker image inspect `
  ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
```

### 7.5 Understand package visibility

| Visibility | Access |
|---|---|
| Public | Anyone can pull |
| Private | Authorized users and workflows |
| Internal | Available within eligible organizations |

For commercial applications, private packages are often appropriate.

Review package permissions and repository access before publishing.

---

## 8. Docker image naming conventions

Consistent image names make large CI/CD environments easier to manage.

Consider:

```text
restaurant-backend
restaurant-frontend
restaurant-worker
restaurant-scheduler
restaurant-nginx
```

A useful naming convention identifies:

- Product or application.
- Service.
- Optional component or variant.

Example:

```text
ghcr.io/your-owner/restaurant-backend
ghcr.io/your-owner/restaurant-frontend
ghcr.io/your-owner/restaurant-worker
```

Avoid ambiguous names such as:

```text
image1
test
production
final
new-image
```

### 8.1 Separate application identity from environment

Prefer one versioned image promoted between environments:

```text
restaurant-backend:1.2.0
```

The same image can be deployed to:

- Development.
- Staging.
- Production.

Do not rebuild the image separately for every environment merely to change configuration.

Environment-specific settings should normally be injected at runtime.

---

## 9. Semantic image tagging

One of the most important release-engineering decisions is how you identify application images.

Consider:

```text
restaurant-backend:latest
restaurant-backend:1.0.0
restaurant-backend:1.1.0
restaurant-backend:main
restaurant-backend:sha-a81f42c
```

These tags serve different purposes.

### 9.1 Semantic versioning

Use:

```text
MAJOR.MINOR.PATCH
```

| Version | Meaning |
|---|---|
| `1.0.0` | Initial stable release |
| `1.1.0` | Backward-compatible feature |
| `1.1.1` | Backward-compatible bug fix |
| `2.0.0` | Breaking change |

Example:

```text
restaurant-backend:1.0.0
restaurant-backend:1.1.0
restaurant-backend:2.0.0
```

### 9.2 Commit SHA tags

You should also identify images by the source commit.

Example:

```text
restaurant-backend:sha-a81f42c
```

Advantages:

- Traceable to source code.
- Useful for debugging.
- Helps identify exactly which code was built.
- Useful for deployment records and rollback references.

### 9.3 Recommended tagging strategy

| Git event | Docker tag |
|---|---|
| Pull request | `pr-42` |
| Push to main | `main` |
| Git tag `v1.2.0` | `1.2.0` |
| Git tag `v1.2.0` | `1.2` |
| Git tag `v1.2.0` | `1` |
| Any commit | `sha-<short-sha>` |

A tag is a human-readable reference. It can be moved if the registry permits it.

Avoid treating `latest` as a production release identifier.

### 9.4 Automate tags with Docker Metadata Action

The Docker Metadata Action generates image tags and OCI labels from GitHub events and Git references.

Example:

```yaml
- name: Docker metadata
  id: meta
  uses: docker/metadata-action@v6
  with:
    images: ghcr.io/YOUR_OWNER/restaurant-backend
    tags: |
      type=semver,pattern={{version}}
      type=semver,pattern={{major}}.{{minor}}
      type=ref,event=branch
      type=ref,event=pr
      type=sha
```

The output can be passed to the image build Action.

For production, pin third-party Actions to reviewed full commit SHAs and maintain a process for updating those pins.

---

## 10. Docker image digests

Tags are mutable.

For example:

```text
restaurant-backend:1.0.0
```

Someone with sufficient registry permissions could replace the image associated with that tag.

A digest identifies image content using a cryptographic hash.

Example:

```text
ghcr.io/YOUR_OWNER/restaurant-backend@sha256:abc123...
```

### 10.1 Tag versus digest

#### Tag

```text
restaurant-backend:1.0.0
```

A human-readable reference that may move.

#### Digest

```text
restaurant-backend@sha256:...
```

A content-addressed reference to a particular image manifest or index.

### 10.2 Inspect an image digest

```powershell
docker buildx imagetools inspect `
  ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
```

### 10.3 Pull by digest

```powershell
docker pull `
  ghcr.io/YOUR_OWNER/restaurant-backend@sha256:YOUR_DIGEST
```

Replace the placeholder with the real digest returned by your registry.

### 10.4 Why digests matter

Use digests when:

- Promoting images between environments.
- Deploying a tested artifact.
- Verifying image identity.
- Implementing rollback.
- Building an auditable release process.

For multi-platform images, distinguish between the image index digest and platform-specific manifest digests.

**Important release principle:** Build once, verify once, and promote the same artifact. Do not rebuild the production image after staging tests have passed.

---

## 11. Docker layer caching

Building images repeatedly can be expensive.

Docker caching allows unchanged build layers to be reused.

Consider:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
```

A small source-code change can invalidate the dependency installation layer.

A better structure:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
```

Now application source changes do not necessarily invalidate dependency installation.

### 11.1 Understand cache invalidation

A cache layer may be invalidated when:

- Its instruction changes.
- An input file changes.
- A previous layer changes.
- A build argument affecting the instruction changes.

Docker cache behavior depends on the instruction and its inputs.

### 11.2 GitHub Actions BuildKit cache

The Docker Build Push Action supports external cache sources and destinations.

Example:

```yaml
- name: Build Docker image
  uses: docker/build-push-action@v7
  with:
    context: .
    file: docker/backend.Dockerfile
    push: false
    tags: restaurant-backend:training
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

`mode=max` exports intermediate build-stage cache too.

### 11.3 Cache considerations

- Use separate cache scopes for different images.
- Do not place secrets in cache.
- Avoid allowing untrusted workflows to poison trusted build caches.
- Monitor cache storage usage.
- Use compatible Buildx versions on self-hosted runners.
- Understand which workflows can read and write each cache.

**Exercise:** Build the same image twice. Record the build duration. Change only an application source file, rebuild, and compare the output.

---

## 12. GitHub Actions cache backend

The GitHub Actions cache backend allows BuildKit to store and retrieve build cache through GitHub Actions infrastructure.

This is useful when builds run on temporary GitHub-hosted runners.

Example:

```yaml
- name: Set up Buildx
  uses: docker/setup-buildx-action@v4

- name: Build backend
  uses: docker/build-push-action@v7
  with:
    context: .
    file: docker/backend.Dockerfile
    push: false
    tags: restaurant-backend:training
    cache-from: type=gha,scope=backend
    cache-to: type=gha,scope=backend,mode=max
```

For the frontend, use a different scope:

```yaml
cache-from: type=gha,scope=frontend
cache-to: type=gha,scope=frontend,mode=max
```

### 12.1 Why use separate scopes?

Without clear separation, different builds may overwrite or compete for cache data.

A scope can identify:

- Backend cache.
- Frontend cache.
- Worker cache.
- Different platform caches.

### 12.2 Practical exercise

Create a workflow that:

1. Builds the backend.
2. Uses the GitHub Actions cache.
3. Builds the backend again.
4. Compares build times.
5. Uses a separate cache scope for the frontend.

Document the results.

---

## 13. Multi-platform builds

Imagine you sell your application to customers using different server hardware.

One customer may use an AMD64 server. Another may use ARM64 hardware.

You can publish multiple architectures under one image reference.

### 13.1 GitHub Actions example

```yaml
name: Multi Platform Build

on:
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v4

      - name: Login to GHCR
        uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and publish
        uses: docker/build-push-action@v7
        with:
          context: .
          file: docker/backend.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ghcr.io/YOUR_OWNER/restaurant-backend:multi-platform
```

This example uses readable Action version tags. For a production workflow, use verified immutable Action references and update them deliberately.

### 13.2 Verify the result

```powershell
docker buildx imagetools inspect `
  ghcr.io/YOUR_OWNER/restaurant-backend:multi-platform
```

Inspect the platform entries.

### 13.3 Platform compatibility

A multi-platform build is not automatically guaranteed to work on every architecture.

Consider:

- Native Python dependencies.
- Operating-system packages.
- Architecture-specific binaries.
- Base image support.
- Build-time emulation requirements.
- Runtime hardware capabilities.

**Exercise:** Build and inspect both AMD64 and ARM64 variants. Document any dependency that could affect architecture compatibility.

---

## 14. Container vulnerability scanning

Building a Docker image is not enough.

You must examine the software components and configuration inside it.

Common vulnerability sources include:

- Outdated operating-system packages.
- Vulnerable Python dependencies.
- Vulnerable Node.js dependencies.
- Insecure image configurations.
- Exposed secrets.
- Unmaintained base images.

A container scanning process should examine both the image and its build configuration.

### 14.1 Vulnerability severity

| Severity | Typical response |
|---|---|
| Critical | Immediate investigation and urgent remediation |
| High | Prioritized remediation |
| Medium | Planned remediation |
| Low | Track and remediate according to policy |
| Unknown | Investigate and classify |

A scanner finding is not automatically proof that an application is exploitable.

Evaluate:

- Whether the vulnerable component is present.
- Whether the vulnerable functionality is used.
- Whether the issue is reachable.
- Whether a fix exists.
- Whether the affected image is deployed.
- Whether compensating controls exist.

### 14.2 Scanning policy

Define:

- Which severities block a release.
- How unfixed vulnerabilities are handled.
- Who approves exceptions.
- How long an exception remains valid.
- How remediation is tracked.
- How scan results are retained.

Avoid blindly ignoring every unfixed vulnerability or failing every build for every low-risk finding.

---

## 15. Trivy integration

Trivy is a security scanner that can inspect container images, filesystems, repositories, and configuration.

### 15.1 Install Trivy locally

Follow the official installation instructions:

[Trivy installation](https://trivy.dev/latest/getting-started/installation/)

### 15.2 Scan your backend image

```powershell
trivy image restaurant-backend:local
```

### 15.3 Filter by severity

```powershell
trivy image `
  --severity HIGH,CRITICAL `
  restaurant-backend:local
```

### 15.4 Generate JSON output

```powershell
trivy image `
  --format json `
  --output trivy-report.json `
  restaurant-backend:local
```

### 15.5 Fail a build when serious vulnerabilities are found

```powershell
trivy image `
  --severity HIGH,CRITICAL `
  --exit-code 1 `
  restaurant-backend:local
```

A nonzero exit status can make the workflow fail.

### 15.6 Integrate Trivy into GitHub Actions

Example:

```yaml
- name: Scan Docker image
  uses: aquasecurity/trivy-action@v0.36.0
  with:
    image-ref: restaurant-backend:local
    format: table
    exit-code: "1"
    ignore-unfixed: true
    vuln-type: os,library
    severity: HIGH,CRITICAL
```

Check the Action's current documentation before adopting a version. Pin third-party Actions to verified full commit SHAs in production.

### 15.7 Scan more than the image

You can also scan repository configuration:

```powershell
trivy fs .

trivy config .
```

This helps identify risks before an image is deployed.

**Exercise:** Build your backend image, scan it, save a JSON report, and document the highest-severity findings.

---

## 16. Software Bill of Materials (SBOM)

SBOM means Software Bill of Materials.

It is an inventory of software components contained in an application or artifact.

Example:

```text
restaurant-backend
│
├── Python 3.12
│
├── Django
│
├── Django REST Framework
│
├── Gunicorn
│
├── psycopg
│
└── Other dependencies
```

### 16.1 Why SBOM matters

An SBOM helps you:

- Identify installed dependencies.
- Investigate vulnerability exposure.
- Understand software supply chains.
- Track licenses.
- Support compliance activities.
- Respond to newly disclosed vulnerabilities.

### 16.2 Common SBOM formats

| Format | Description |
|---|---|
| SPDX | Software package and license information |
| CycloneDX | Software component and supply-chain information |

### 16.3 Generate an SBOM with Buildx

```powershell
docker buildx build `
  --file docker/backend.Dockerfile `
  --tag restaurant-backend:sbom `
  --sbom=true `
  --output type=oci,dest=backend-image.tar `
  .
```

### 16.4 Generate an SBOM attestation when publishing

```yaml
- name: Build and publish image
  uses: docker/build-push-action@v7
  with:
    context: .
    file: docker/backend.Dockerfile
    push: true
    tags: ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
    sbom: true
```

Docker BuildKit can attach SBOM attestations to built images.

### 16.5 SBOM policy

For every production release, record:

- Application version.
- Source commit.
- Image digest.
- Build timestamp.
- SBOM format.
- SBOM location.
- Scanner results.
- Review status.

An SBOM is an inventory, not proof that the software is secure.

**Exercise:** Generate SPDX and CycloneDX SBOMs for your backend image. Compare the information and document which format you would use for your project.

---

## 17. Container image signing

How do you know an image came from the expected build process?

Image signing provides a way to verify image identity and integrity using cryptographic signatures.

Two concepts:

| Concept | Purpose |
|---|---|
| Image digest | Identifies image content |
| Image signature | Provides verifiable authenticity and integrity information |

### 17.1 Cosign

Cosign is commonly used for signing and verifying container images.

Documentation:

[Cosign overview](https://docs.sigstore.dev/cosign/overview/)

Conceptual workflow:

```text
Build image
    |
    v
Calculate image digest
    |
    v
Sign image
    |
    v
Publish signature
    |
    v
Verify before deployment
```

### 17.2 Key-based signing

A signing key can be used to sign an image digest.

However, private signing keys require secure storage, access control, rotation, and recovery procedures.

Do not commit private signing keys.

### 17.3 Keyless signing

Keyless signing uses an identity provider and short-lived credentials rather than requiring a permanently managed signing private key.

GitHub Actions can integrate with Sigstore using OpenID Connect.

The workflow needs appropriate identity token permissions.

### 17.4 Verification policy

Before deploying a signed image, determine:

- Which identity is allowed to sign?
- Which repository is trusted?
- Which workflow is trusted?
- Which image digest is being verified?
- Which certificate identity is expected?
- What happens when verification fails?

Generating a signature without enforcing verification does not establish a deployment security policy.

**Exercise:** Study Cosign signing and verification. Write a document explaining how your deployment environment would reject an image with an untrusted signature.

---

## 18. Image provenance and attestations

Image provenance describes how an image was built.

It can provide information about:

- Source repository.
- Source revision.
- Build process.
- Builder identity.
- Build metadata.

### 18.1 Enable provenance

```yaml
- name: Build and publish
  uses: docker/build-push-action@v7
  with:
    context: .
    file: docker/backend.Dockerfile
    push: true
    tags: ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
    provenance: mode=max
    sbom: true
```

### 18.2 SBOM versus provenance

| SBOM | Provenance |
|---|---|
| What software is included? | How was it built? |
| Dependency inventory | Build history and metadata |
| Supports vulnerability investigation | Supports supply-chain verification |

Both contribute to software supply-chain transparency.

### 18.3 Attestation verification

Generating an attestation is not the same as verifying it.

A production deployment policy should verify:

1. The attestation is present.
2. It is associated with the expected image digest.
3. The source repository is trusted.
4. The source revision is approved.
5. The builder identity is trusted.
6. The build process satisfies your policy.

**Exercise:** Generate provenance for a test image and document the information you can retrieve from it.

---

## 19. Secure GHCR publishing with GitHub Actions

Now we combine the previous concepts.

Create:

`.github/workflows/docker-publish.yml`

The following workflow publishes an image to GHCR when code is pushed to `main` or when a version tag is pushed.

It also generates SBOM and provenance attestations.

```yaml
name: Docker Build and Publish

on:
  push:
    branches:
      - main
    tags:
      - "v*"

  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Login to GHCR
        uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Generate image metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ghcr.io/YOUR_OWNER/restaurant-backend
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=ref,event=branch
            type=sha

      - name: Build and publish
        id: build
        uses: docker/build-push-action@v7
        with:
          context: .
          file: docker/backend.Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha,scope=backend
          cache-to: type=gha,scope=backend,mode=max
          sbom: true
          provenance: mode=max
```

**Before running:**

- Replace `YOUR_OWNER` with your actual GitHub owner.
- Ensure the Dockerfile and build context match your repository.
- Configure package permissions.
- Ensure only trusted events can publish production images.
- Use reviewed immutable Action references in production.
- Confirm the workflow's package permissions are sufficient.
- Separate untrusted pull-request validation from package publishing.

### 19.1 Why separate PR validation from publishing?

A pull request should generally build and test an image without publishing it to the production package.

Recommended separation:

| Event | Build | Scan | Publish |
|---|---|---|---|
| Pull request | Yes | Yes | No |
| Push to main | Yes | Yes | Candidate image |
| Version tag | Yes | Yes | Versioned release |

This reduces the exposure of package-write privileges to untrusted pull-request code.

### 19.2 Improve the workflow

Extend the workflow to:

1. Run application tests before building.
2. Build the backend and frontend separately.
3. Scan both images.
4. Generate SBOMs.
5. Publish images only from trusted events.
6. Record the resulting image digests.
7. Upload reports as workflow artifacts.
8. Publish versioned release images.

---

## 20. Docker Compose deployment

Now we move from building images to running the complete application.

Your application has several services:

```text
Restaurant Platform
│
├── Backend
│   └── Django / DRF
│
├── Frontend
│   └── React / Nginx
│
├── Database
│   └── PostgreSQL
│
└── Reverse Proxy
    └── Nginx
```

### 20.1 Production Compose configuration

Create:

`docker-compose.production.yml`

```yaml
services:
  backend:
    image: ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0
    restart: unless-stopped

    env_file:
      - .env.production

    depends_on:
      db:
        condition: service_healthy

    networks:
      - internal

  frontend:
    image: ghcr.io/YOUR_OWNER/restaurant-frontend:1.0.0
    restart: unless-stopped

    ports:
      - "8080:80"

    networks:
      - internal

  db:
    image: postgres:16
    restart: unless-stopped

    environment:
      POSTGRES_DB: restaurant
      POSTGRES_USER: restaurant
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

    volumes:
      - postgres_data:/var/lib/postgresql/data

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U restaurant -d restaurant
      interval: 10s
      timeout: 5s
      retries: 5

    networks:
      - internal

volumes:
  postgres_data:

networks:
  internal:
    driver: bridge
```

This is a training example, not a complete production deployment.

In a real system:

- Pin the PostgreSQL image version and preferably its digest.
- Store database credentials securely.
- Restrict database network exposure.
- Configure backups and recovery.
- Configure backend health checks.
- Use a reverse proxy for frontend/backend routing.
- Handle migrations explicitly.
- Configure persistent storage and monitoring.
- Define a tested recovery procedure.

For production, avoid treating a mutable tag such as `1.0.0` as the final deployment identity. Prefer a verified image digest.

### 20.2 Pull and start

```powershell
docker compose `
  -f docker-compose.production.yml pull

docker compose `
  -f docker-compose.production.yml up -d
```

Inspect:

```powershell
docker compose `
  -f docker-compose.production.yml ps
```

Logs:

```powershell
docker compose `
  -f docker-compose.production.yml logs -f
```

### 20.3 Stop

```powershell
docker compose `
  -f docker-compose.production.yml down
```

Do not use `down -v` on a production deployment unless you deliberately intend to remove persistent volumes.

### 20.4 Promote the same image

A safer deployment model is:

```text
Build image once
      |
      v
Scan and verify
      |
      v
Record image digest
      |
      v
Deploy to staging
      |
      v
Test staging
      |
      v
Approve production
      |
      v
Deploy the same digest
```

This avoids rebuilding an image between staging and production.

---

## 21. SSH-based deployment architecture

SSH deployment is a common way for GitHub Actions to communicate with a remote Linux server.

Architecture:

```text
GitHub Actions Runner
        |
        v
Build and publish images
        |
        v
Authenticated deployment connection
        |
        v
Remote Linux Server
        |
        v
Pull verified images from GHCR
        |
        v
Update Docker Compose services
        |
        v
Run health checks
```

### 21.1 Deployment prerequisites

The target server needs:

- Linux.
- Docker Engine.
- Docker Compose plugin.
- Network access to the container registry.
- An appropriate deployment account.
- Protected deployment credentials.
- A backup and recovery strategy.

### 21.2 GitHub deployment secrets

Navigate to:

`Repository → Settings → Secrets and variables → Actions`

Example secret names:

| Secret | Purpose |
|---|---|
| `DEPLOY_HOST` | Server hostname |
| `DEPLOY_USER` | Deployment account |
| `DEPLOY_SSH_KEY` | SSH authentication material |
| `DEPLOY_PORT` | SSH port if customized |

Use environment-specific secrets where appropriate.

Never put private keys or credentials in your repository.

### 21.3 Deployment workflow structure

Create:

`.github/workflows/deploy-staging.yml`

```yaml
name: Staging Deployment

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    environment:
      name: staging

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Deployment preparation
        run: |
          echo "Staging deployment requested"
          echo "The approved image digest must be verified"
          echo "Deployment execution is handled by the deployment process"
```

This is an architecture starting point, not a complete remote deployment implementation.

For actual remote deployment:

- Use a carefully configured SSH client or trusted deployment Action.
- Verify the server identity using a known host key.
- Use an account with restricted privileges.
- Deploy an approved image digest.
- Verify the deployment result.
- Avoid exposing secrets in command output.

**Never disable SSH host-key verification to make automation succeed.**

For your local-first restaurant software, a controlled update mechanism may eventually be more appropriate than assuming permanent external connectivity.

---

## 22. Self-hosted GitHub Actions runners

A GitHub-hosted runner is provided by GitHub.

A self-hosted runner is a machine you manage that executes GitHub Actions jobs.

### 22.1 Comparison

| Feature | GitHub-hosted | Self-hosted |
|---|---|---|
| Infrastructure | GitHub managed | You manage |
| Initial setup | Minimal | More work |
| Hardware control | Limited | Full |
| Custom software | Workflow setup | Install locally |
| Maintenance | GitHub | You |
| Security responsibility | Shared | Greater responsibility |

### 22.2 Why use self-hosted runners?

Examples:

- Private infrastructure.
- Specialized hardware.
- Internal network access.
- Large build workloads.
- Custom development environments.
- Controlled deployment infrastructure.

### 22.3 Runner architecture

```text
GitHub Repository
       |
       v
GitHub Actions Service
       |
       v
Self-hosted Runner
       |
       v
Internal Infrastructure
       |
       v
Deployment Target
```

### 22.4 Runner security

A self-hosted runner can expose its host environment and credentials to jobs that execute on it.

Do not run untrusted pull-request code on a privileged deployment runner.

Use:

- Separate runner groups.
- Restricted repository access.
- Isolated environments.
- Disposable runners where appropriate.
- Limited permissions.
- Controlled network access.
- Regular runner updates.

A runner used to build untrusted pull requests should not automatically have access to production infrastructure.

Documentation:

[GitHub Actions hosting your own runners](https://docs.github.com/en/actions/hosting-your-own-runners)

**Exercise:** Design two runner groups: one for CI builds and one for protected deployment jobs. Document their access boundaries.

---

## 23. Kubernetes deployment workflows

Docker Compose is useful for managing services on a Docker host.

Kubernetes is a container orchestration platform designed to manage workloads across a cluster.

### 23.1 Important Kubernetes resources

| Resource | Responsibility |
|---|---|
| Pod | Runs one or more containers |
| Deployment | Manages application replicas and updates |
| Service | Provides stable network access |
| ConfigMap | Non-sensitive configuration |
| Secret | Sensitive configuration data |
| Ingress | HTTP/HTTPS routing |
| Namespace | Resource isolation |
| PersistentVolume | Storage abstraction |
| Job | Runs a finite task |
| CronJob | Runs scheduled tasks |

### 23.2 Backend deployment manifest

Create:

`kubernetes/backend-deployment.yml`

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: restaurant-backend

spec:
  replicas: 2

  selector:
    matchLabels:
      app: restaurant-backend

  template:
    metadata:
      labels:
        app: restaurant-backend

    spec:
      containers:
        - name: backend

          image: ghcr.io/YOUR_OWNER/restaurant-backend:1.0.0

          ports:
            - containerPort: 8000

          resources:
            requests:
              cpu: 100m
              memory: 128Mi

            limits:
              cpu: 500m
              memory: 512Mi
```

This is a basic learning manifest. A production deployment also needs probes, security context, appropriate service accounts, configuration, secrets, and network policies.

### 23.3 Apply the deployment

```powershell
kubectl apply -f kubernetes/backend-deployment.yml
```

Inspect:

```powershell
kubectl get deployments

kubectl get pods

kubectl describe deployment restaurant-backend
```

### 23.4 Kubernetes image updates

In production, prefer updating a Deployment to a verified image digest rather than relying on a mutable tag.

Also configure:

- Readiness probes.
- Liveness probes.
- Startup probes where needed.
- Resource requests and limits.
- Secrets management.
- Network policies.
- Appropriate service accounts.
- Image pull credentials for private registries.

Documentation:

[Kubernetes deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

**Exercise:** Create a backend Deployment and Service for a local Kubernetes training cluster. Validate the manifests before applying them.

---

## 24. Helm chart deployments

Helm is a package manager for Kubernetes.

It allows you to define reusable Kubernetes deployment templates.

Instead of maintaining separate manifests for different environments, you can create one chart and configure it through values files.

### 24.1 Example structure

```text
helm/
└── restaurant-platform/
    ├── Chart.yaml
    ├── values.yaml
    │
    ├── values-dev.yaml
    ├── values-staging.yaml
    ├── values-production.yaml
    │
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        ├── ingress.yaml
        └── configmap.yaml
```

### 24.2 Chart configuration

`Chart.yaml`

```yaml
apiVersion: v2

name: restaurant-platform

description: Restaurant application deployment

type: application

version: 1.0.0

appVersion: "1.0.0"
```

### 24.3 Values

`values.yaml`

```yaml
backend:
  replicaCount: 2

  image:
    repository: ghcr.io/YOUR_OWNER/restaurant-backend
    tag: "1.0.0"

  service:
    port: 8000
```

### 24.4 Validate the chart

```powershell
helm lint helm/restaurant-platform
```

Render templates:

```powershell
helm template restaurant-platform helm/restaurant-platform
```

### 24.5 Deploy

```powershell
helm upgrade --install restaurant-platform `
  helm/restaurant-platform `
  --namespace restaurant `
  --create-namespace
```

Documentation:

[Helm documentation](https://helm.sh/docs/)

**Exercise:** Create a Helm chart with separate development and staging values files. Explain which values should be environment-specific and which should remain part of the application image.

---

## 25. Blue-green deployments

Blue-green deployment is a release strategy that maintains two application environments.

```text
Blue
Version 1
Currently serving traffic

Green
Version 2
New version under testing
```

The process:

```text
Traffic initially goes to Blue
          |
          v
Deploy new version to Green
          |
          v
Test Green
          |
          v
Verify health and compatibility
          |
          v
Switch traffic to Green
          |
          v
Green becomes active
```

### 25.1 Advantages

- Reduced deployment downtime.
- Controlled traffic switching.
- Previous version remains available.
- Easier application rollback.

### 25.2 Limitations

- Requires additional infrastructure.
- Database changes need compatibility planning.
- Two application environments may increase resource consumption.
- Switching traffic does not automatically reverse database changes.
- Background workers and scheduled jobs need careful coordination.

### 25.3 Practical scenario

```text
Blue:
restaurant-backend:1.0.0

Green:
restaurant-backend:1.1.0
```

Test Green before switching production traffic.

**Exercise:** Draw a blue-green deployment architecture for your Django + React application. Identify where the reverse proxy or load balancer switches traffic.

---

## 26. Canary deployments

A canary deployment gradually introduces a new version to a limited portion of traffic.

For example:

| Stage | Old version | New version |
|---|---:|---:|
| Initial | 100% | 0% |
| Stage 1 | 90% | 10% |
| Stage 2 | 75% | 25% |
| Stage 3 | 50% | 50% |
| Final | 0% | 100% |

These percentages are illustrative, not mandatory deployment settings.

### 26.1 Monitoring criteria

Before increasing traffic, examine:

- HTTP error rate.
- Response latency.
- CPU and memory usage.
- Database errors.
- Application health checks.
- Business-level metrics.

### 26.2 Automatic rollback

A canary deployment can stop or reverse traffic progression if defined health criteria are violated.

However, rollback needs a compatible previous application version and a database migration strategy that supports it.

### 26.3 Canary versus blue-green

| Blue-green | Canary |
|---|---|
| Maintains two environments | Gradually introduces a new version |
| Traffic switches between environments | Traffic is split progressively |
| Requires capacity for both environments | Requires traffic-management capabilities |
| Rollback can switch traffic back | Rollback reduces or removes new-version traffic |

**Exercise:** Design a canary rollout with three stages. Define the metrics and thresholds that must pass before moving to the next stage.

---

## 27. Rollback automation

A deployment is not complete just because an image starts successfully.

You must be able to recover from failed releases.

### 27.1 Docker Compose rollback concept

Maintain a record of the previously deployed image digest.

```text
Current:
restaurant-backend@sha256:NEW_DIGEST

Previous:
restaurant-backend@sha256:OLD_DIGEST
```

If health checks fail:

1. Stop further rollout.
2. Record the failed release.
3. Restore the previously approved image reference.
4. Restart the affected service.
5. Run health checks.
6. Confirm recovery.
7. Create an incident or deployment record.

Do not assume that changing a tag alone is a sufficient rollback strategy.

### 27.2 Kubernetes rollback

Inspect history:

```powershell
kubectl rollout history deployment/restaurant-backend
```

Rollback:

```powershell
kubectl rollout undo deployment/restaurant-backend
```

Inspect:

```powershell
kubectl rollout status deployment/restaurant-backend
```

### 27.3 Rollback limitations

Application rollback and database rollback are separate problems.

For example:

```text
Application 1.0
      |
      v
Database schema 1
      |
      v
Application 2.0
      |
      v
Database schema 2
```

If version 2 requires schema 2, simply restoring application version 1 may break compatibility.

This is why backward-compatible migrations are important.

**Exercise:** Document a failed deployment scenario and the exact recovery sequence for Compose and Kubernetes.

---

## 28. Django database migrations during deployment

Your Django application uses migrations to manage database schema changes.

A deployment workflow must decide:

- When migrations run.
- Which identity runs them.
- Whether the migration is backward-compatible.
- What happens if a migration fails.
- How application instances behave during migration.
- How the database is backed up and recovered.

### 28.1 Inspect migrations

```powershell
python manage.py showmigrations
```

Check pending migrations:

```powershell
python manage.py migrate --plan
```

Apply:

```powershell
python manage.py migrate
```

### 28.2 Expand-and-contract strategy

Use an expand-and-contract approach.

#### Phase 1 — Expand

- Add new nullable columns or tables.
- Preserve compatibility with the old application.
- Avoid immediately removing old fields.

#### Phase 2 — Transition

- Deploy code that supports both old and new structures.
- Migrate data where required.
- Verify that the new application uses the new structure.

#### Phase 3 — Contract

- Remove obsolete fields only after old application versions are no longer used.
- Remove old code paths.
- Verify the final schema.

### 28.3 Example deployment sequence

```text
Backup database
      |
      v
Check migration plan
      |
      v
Apply compatible migrations
      |
      v
Deploy application
      |
      v
Run health checks
      |
      v
Confirm deployment
```

### 28.4 Migration safety

A production migration should have:

- Explicit ownership.
- A reviewed migration plan.
- Backup and recovery procedures.
- An understanding of locking and execution time.
- Compatibility with the currently running application.
- A record of its execution result.

Never assume that reverting a Git commit automatically reverses a database migration.

**Exercise:** Create a sample Django migration plan and document how you would deploy it without breaking the previous application version.

---

## 29. Deployment health checks

A successful Docker build does not prove that the application works.

You need runtime verification.

### 29.1 Django health endpoint

A simple endpoint might return:

```json
{
  "status": "ok"
}
```

For example, your application might expose:

```text
GET /health/
```

The exact implementation depends on your Django project.

### 29.2 GitHub Actions smoke test

```yaml
- name: Verify backend health
  run: |
    curl --fail \
      --retry 5 \
      --retry-delay 5 \
      http://localhost:8000/health/
```

This assumes the application is running and the endpoint is configured.

### 29.3 Types of checks

| Check | Purpose |
|---|---|
| Startup probe | Has the application started? |
| Liveness probe | Is the process healthy? |
| Readiness probe | Can it accept traffic? |
| HTTP smoke test | Does an endpoint respond? |
| Integration test | Do components work together? |
| Database check | Is the database accessible? |

Avoid using one endpoint that performs expensive database or external-service operations for every liveness check.

### 29.4 Deployment verification sequence

```text
Deploy application
       |
       v
Wait for startup
       |
       v
Check readiness
       |
       v
Run HTTP smoke tests
       |
       v
Check error rate and logs
       |
       v
Mark deployment successful
```

A failed health check should prevent the release from being marked successful.

---

## 30. Release engineering

Now we combine Git tags, GitHub Releases, Docker image tags, digests, and deployment records.

Your release should be traceable from source code to the running image.

### 30.1 Release structure

```text
Git commit
    |
    v
Git tag v1.0.0
    |
    v
GitHub Release v1.0.0
    |
    v
Docker image build
    |
    v
SBOM + Provenance
    |
    v
Container security verification
    |
    v
Publish GHCR image
    |
    v
Record image digest
    |
    v
Deploy approved digest
    |
    v
Record deployment
```

### 30.2 Suggested release naming

| Component | Version |
|---|---|
| Application | `v1.0.0` |
| Backend image | `1.0.0` |
| Frontend image | `1.0.0` |
| Release tag | `v1.0.0` |
| Database migration release | Documented alongside application release |

### 30.3 Release notes

Include:

- New features.
- Bug fixes.
- Breaking changes.
- Database migration requirements.
- Security changes.
- Docker image references.
- Image digests.
- Deployment instructions.
- Rollback considerations.

### 30.4 GitHub Releases

The Git tag identifies the source revision.

The Docker image digest identifies the built artifact.

They should be recorded together.

A release record should make it possible to answer:

1. Which commit produced this image?
2. Which workflow built it?
3. Which image digest was published?
4. Which security checks passed?
5. Which SBOM and provenance records exist?
6. Which environments received the image?
7. Which image was running before the deployment?

---

## 31. Complete Django + React production pipeline

Let's combine everything.

### 31.1 Target architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--------------------+
    |                    |
    v                    v
Python CI             React CI
    |                    |
    +----------+---------+
               |
               v
        Docker Build
               |
               v
        Security Scanning
               |
               v
        SBOM + Provenance
               |
               v
        GitHub Container Registry
               |
               v
        Verified Image Digests
               |
               v
        Staging Deployment
               |
               v
        Health Checks
               |
               v
        Production Approval
               |
               v
        Production Deployment
               |
               v
        Release Monitoring
```

### 31.2 Recommended workflow separation

| Workflow | Responsibility |
|---|---|
| `ci.yml` | Application tests |
| `docker-build.yml` | Docker image build |
| `docker-security.yml` | Trivy and configuration scanning |
| `docker-publish.yml` | GHCR publishing |
| `docker-attest.yml` | SBOM and provenance |
| `deploy-staging.yml` | Staging deployment |
| `deploy-production.yml` | Protected production deployment |
| `rollback.yml` | Recovery workflow |

This separation makes the architecture easier to maintain and audit.

### 31.3 Recommended pipeline stages

#### Stage 1 — Pull request validation

- Python tests.
- React tests.
- Linting.
- Type checking.
- Docker build validation.
- Security scanning.

Do not publish production images from untrusted pull-request workflows.

#### Stage 2 — Main branch build

- Build backend image.
- Build frontend image.
- Use BuildKit cache.
- Run image scans.
- Generate SBOM.
- Generate provenance.

#### Stage 3 — Publish

- Authenticate with GHCR.
- Publish approved images.
- Record digests.
- Store release metadata.

#### Stage 4 — Staging

- Pull the published image by digest.
- Deploy the exact image that passed verification.
- Run health checks.
- Perform smoke tests.

#### Stage 5 — Production

- Require appropriate environment approval.
- Deploy the approved digest.
- Run health checks.
- Record the deployment.
- Keep a rollback reference.

### 31.4 Special consideration for your offline-first POS system

Your restaurant POS should not depend on GitHub being available while the restaurant is operating.

A sensible architecture is:

```text
Developer
    |
    v
GitHub CI/CD
    |
    v
GHCR
    |
    v
Approved release package
    |
    v
Controlled local update process
    |
    v
Restaurant server
    |
    +--- POS
    +--- Kitchen display
    +--- Printer
    +--- Ready-order screen
    +--- PostgreSQL
```

The local server should continue operating if internet connectivity disappears.

Updates should be:

- Controlled.
- Versioned.
- Verified.
- Recoverable.
- Supported by database backups.
- Tested before production rollout.

A local update process should not require a permanent connection to GitHub or GHCR during normal restaurant operations.

---

## 32. End-to-end practical project

**Main project:** Build a complete container delivery pipeline in `github-deep-dive-training`.

Your goal is to create a working training environment that demonstrates the full lifecycle from source code to deployment.

### Stage A — Docker foundations

- Create a sample backend application.
- Create a sample frontend application.
- Write production Dockerfiles.
- Configure multi-stage builds.
- Create `.dockerignore` files.
- Build images locally.
- Inspect image layers and sizes.

### Stage B — BuildKit and Buildx

- Enable BuildKit.
- Create a Buildx builder.
- Build a single-platform image.
- Build a multi-platform image.
- Configure build caching.
- Test BuildKit secret mounts.

### Stage C — GHCR

- Authenticate with GHCR.
- Publish a backend image.
- Publish a frontend image.
- Configure package visibility.
- Pull published images.
- Inspect image digests.

### Stage D — Image versioning

- Create semantic version tags.
- Create SHA-based tags.
- Configure Docker Metadata Action.
- Test branch, PR, and release tagging.
- Document image naming conventions.

### Stage E — DevSecOps

- Install and run Trivy.
- Scan operating-system packages.
- Scan application dependencies.
- Generate an SBOM.
- Generate provenance.
- Study Cosign.
- Document image verification policies.

### Stage F — Deployment

- Create Docker Compose deployment.
- Deploy to a local test environment.
- Configure health checks.
- Simulate a failed release.
- Practice rollback.
- Study Kubernetes deployment.
- Create a Helm chart.

### Stage G — Release engineering

- Create a Git tag.
- Publish a GitHub Release.
- Publish versioned Docker images.
- Record image digests.
- Document release notes.
- Create a deployment record.

---

## 33. Practical exercise checklist

Use this checklist to track your progress.

### Lesson 43 progress — 0/37

#### Docker foundations

- [ ] Create backend and frontend Dockerfiles.
- [ ] Implement multi-stage builds.
- [ ] Create `.dockerignore` files.
- [ ] Build and inspect images locally.

#### BuildKit and Buildx

- [ ] Configure BuildKit.
- [ ] Create a Buildx builder.
- [ ] Build an AMD64 image.
- [ ] Build a multi-platform image.
- [ ] Configure BuildKit caching.
- [ ] Practice BuildKit secret mounts.

#### GHCR and image versioning

- [ ] Authenticate with GHCR.
- [ ] Publish the backend image.
- [ ] Publish the frontend image.
- [ ] Configure package visibility.
- [ ] Pull images from GHCR.
- [ ] Inspect image digests.
- [ ] Implement semantic image tagging.
- [ ] Implement SHA-based tagging.
- [ ] Configure Docker Metadata Action.

#### Container security

- [ ] Scan images with Trivy.
- [ ] Generate a Trivy JSON report.
- [ ] Generate an SBOM.
- [ ] Generate provenance attestations.
- [ ] Study Cosign image signing.
- [ ] Create the Docker publishing workflow.

#### Deployment

- [ ] Configure Docker Compose deployment.
- [ ] Study SSH deployment architecture.
- [ ] Study self-hosted runners.
- [ ] Create Kubernetes deployment manifests.
- [ ] Create a Helm chart.
- [ ] Document blue-green deployment.
- [ ] Document canary deployment.
- [ ] Practice application rollback.
- [ ] Implement Django migration planning.
- [ ] Configure deployment health checks.

#### Release engineering

- [ ] Create a versioned release.
- [ ] Document the complete CI/CD architecture.

---

## 34. Documentation files to create

Keep the same documentation convention used in your previous lessons.

Create:

```text
docs/
└── github/
    └── module-04-actions/
        │
        ├── lesson-43-advanced-docker-ci-cd.md
        │
        └── lesson-43/
            ├── docker-image-architecture.md
            ├── production-dockerfiles.md
            ├── multi-stage-builds.md
            ├── docker-buildkit.md
            ├── docker-buildx.md
            ├── github-container-registry.md
            ├── docker-image-naming.md
            ├── semantic-image-tagging.md
            ├── image-digests.md
            ├── docker-layer-caching.md
            ├── multi-platform-builds.md
            ├── container-vulnerability-scanning.md
            ├── trivy-integration.md
            ├── sbom-generation.md
            ├── image-signing.md
            ├── image-provenance.md
            ├── ghcr-publishing-workflow.md
            ├── docker-compose-deployment.md
            ├── ssh-deployment.md
            ├── self-hosted-runners.md
            ├── kubernetes-deployment.md
            ├── helm-deployment.md
            ├── blue-green-deployment.md
            ├── canary-deployment.md
            ├── rollback-automation.md
            ├── django-database-migrations.md
            ├── deployment-health-checks.md
            ├── release-engineering.md
            ├── django-react-cicd.md
            └── practical-exercises.md
```

### Main Markdown file

Create:

`docs/github/module-04-actions/lesson-43-advanced-docker-ci-cd.md`

Recommended structure:

```markdown
# Lesson 43 — Advanced Docker Builds, Container Registries & Release Engineering

## 1. Learning Objectives
## 2. Docker Image Architecture
## 3. Docker Image Layers
## 4. Production Dockerfiles
## 5. Multi-stage Builds
## 6. Docker BuildKit
## 7. Docker Buildx
## 8. GitHub Container Registry
## 9. Docker Image Naming
## 10. Semantic Image Tagging
## 11. Image Digests
## 12. Docker Layer Caching
## 13. GitHub Actions Cache Backend
## 14. Multi-platform Builds
## 15. Container Vulnerability Scanning
## 16. Trivy Integration
## 17. SBOM Generation
## 18. Image Signing
## 19. Image Provenance
## 20. GHCR Publishing
## 21. Docker Compose Deployment
## 22. SSH Deployment
## 23. Self-hosted Runners
## 24. Kubernetes Deployment
## 25. Helm
## 26. Blue-green Deployment
## 27. Canary Deployment
## 28. Rollback Automation
## 29. Database Migrations
## 30. Deployment Health Checks
## 31. Release Engineering
## 32. Django + React CI/CD Architecture
## 33. Practical Exercises
## 34. Completion Checklist
## 35. Official References
```

---

## 35. Git workflow — commits, PR, tag and release

We will continue using your existing branch, pull request, commit, tag, and release practices.

### Step 1 — Create the branch

```bash
git switch main

git pull origin main

git switch -c feat/lesson-43-docker-release-engineering
```

### Step 2 — Create the documentation

Start with:

- `lesson-43-advanced-docker-ci-cd.md`
- `docker-image-architecture.md`
- `production-dockerfiles.md`
- `multi-stage-builds.md`
- `docker-buildkit.md`
- `docker-buildx.md`

Continue with the remaining files as you complete their exercises.

### Step 3 — Suggested commits

Keep commits organized by responsibility.

#### Documentation

```bash
git add docs/github/module-04-actions/

git commit -m "docs(actions): add advanced Docker CI/CD lesson"
```

#### Docker examples

```bash
git add docker/

git commit -m "feat(docker): add production container build examples"
```

#### GitHub Actions

```bash
git add .github/workflows/

git commit -m "feat(actions): add Docker build and publish workflows"
```

#### Kubernetes and Helm

```bash
git add kubernetes/ helm/

git commit -m "feat(deploy): add Kubernetes and Helm examples"
```

Only stage directories that you have actually created and reviewed.

### Step 4 — Validate

```bash
git status

git diff --check

docker compose config
```

For Dockerfiles:

```bash
docker build \
  -f docker/backend.Dockerfile \
  -t restaurant-backend:training .
```

For Helm:

```bash
helm lint helm/restaurant-platform
```

For Kubernetes:

```bash
kubectl apply --dry-run=client \
  -f kubernetes/backend-deployment.yml
```

Validate your GitHub Actions YAML and run the workflows in GitHub before considering the exercises complete.

### Step 5 — Push

```bash
git push -u origin feat/lesson-43-docker-release-engineering
```

### Step 6 — Create a pull request

**PR title:**

`feat(actions): add advanced Docker CI/CD and release engineering`

**PR description:**

#### Summary

Introduces Lesson 43, covering production Docker builds, BuildKit, Buildx, GHCR, container security, and deployment automation.

#### Changes

- Added production Dockerfile examples.
- Added multi-stage build documentation.
- Added BuildKit and Buildx exercises.
- Added GHCR authentication and publishing.
- Added semantic image tagging strategies.
- Added image digest documentation.
- Added Docker layer caching.
- Added multi-platform build examples.
- Added Trivy vulnerability scanning.
- Added SBOM and provenance documentation.
- Added image signing concepts.
- Added Docker Compose deployment.
- Added Kubernetes and Helm examples.
- Added blue-green and canary deployment concepts.
- Added rollback strategies.
- Added database migration guidance.
- Added deployment health checks.
- Documented Django + React CI/CD architecture.

#### Validation

- [ ] Dockerfiles build successfully.
- [ ] Multi-stage builds tested.
- [ ] Buildx configured.
- [ ] GHCR authentication tested.
- [ ] Images published successfully.
- [ ] Image digests recorded.
- [ ] Trivy scanning tested.
- [ ] SBOM generation verified.
- [ ] Provenance reviewed.
- [ ] Deployment configuration validated.
- [ ] No credentials committed.

#### Related lessons

- Lesson 40 — GitHub Actions Security.
- Lesson 41 — Security Automation and Compliance.
- Lesson 42 — Advanced GitHub Actions Architecture.
- Lesson 43 — Advanced Docker Builds and Release Engineering.

### Step 7 — Merge and create a tag

After reviewing and merging:

```bash
git switch main

git pull origin main

git tag -a module-04-lesson-43 \
  -m "Module 4 Lesson 43: Advanced Docker CI/CD"

git push origin module-04-lesson-43
```

### Step 8 — Create a GitHub Release

| Field | Value |
|---|---|
| Tag | `module-04-lesson-43` |
| Title | Module 4 — Lesson 43: Advanced Docker Builds & Release Engineering |
| Description | Production Docker builds, BuildKit, Buildx, GHCR, image security, SBOM, provenance, Kubernetes, and release engineering. |

---

## 36. Official documentation and references

Keep these resources bookmarked.

| Technology | Documentation |
|---|---|
| Docker multi-stage builds | [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) |
| Docker BuildKit | [Docker BuildKit](https://docs.docker.com/build/buildkit/) |
| Docker Buildx | [Docker Buildx](https://docs.docker.com/build/buildx/) |
| Docker Build Push Action | [Docker Build Push Action](https://github.com/docker/build-push-action) |
| Docker cache | [Docker cache](https://docs.docker.com/build/ci/github-actions/cache/) |
| GHCR | [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) |
| Docker Metadata Action | [Docker Metadata Action](https://github.com/docker/metadata-action) |
| Docker Login Action | [Docker Login Action](https://github.com/docker/login-action) |
| Trivy | [Trivy](https://trivy.dev/) |
| Trivy Action | [Trivy Action](https://github.com/aquasecurity/trivy-action) |
| SBOM attestations | [SBOM attestations](https://docs.docker.com/build/metadata/attestations/sbom/) |
| Build attestations | [Build attestations](https://docs.docker.com/build/metadata/attestations/) |
| Cosign | [Cosign](https://docs.sigstore.dev/cosign/overview/) |
| Kubernetes | [Kubernetes](https://kubernetes.io/docs/) |
| Kubernetes Deployments | [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) |
| Helm | [Helm](https://helm.sh/docs/) |
| GitHub self-hosted runners | [GitHub self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners) |
| GitHub Actions secure use | [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) |

**Versioning note:** GitHub Actions, Docker Actions, scanners, and Docker tooling evolve. Before using a version in a production workflow, verify its current release, permissions, compatibility, and security guidance in the official documentation. Prefer immutable references for third-party Actions.

---

## 37. Completion criteria

You can consider Lesson 43 complete when you can independently:

- Explain Docker images, containers, and image layers.
- Write production-oriented Dockerfiles.
- Build multi-stage Docker images.
- Explain and use BuildKit and Buildx.
- Configure build secrets and caching.
- Build multi-platform images.
- Authenticate with GHCR and publish images.
- Apply semantic versioning and SHA-based tags.
- Explain why image digests are important.
- Scan images with Trivy.
- Generate and inspect an SBOM.
- Explain image signing and provenance.
- Build a GitHub Actions publishing workflow.
- Deploy images using Docker Compose.
- Explain SSH deployment and self-hosted runner security.
- Deploy applications using Kubernetes and Helm.
- Explain blue-green and canary deployment strategies.
- Plan database migrations safely.
- Configure deployment health checks.
- Design a rollback strategy.
- Connect Git tags, GitHub Releases, image digests, and deployment records.

The most important result is not simply having a workflow that builds an image. It is having a traceable delivery process that can build, verify, publish, deploy, and recover from a failed release.

---

## 38. Next lesson — Lesson 44

**Level:** Advanced
**Category:** Production engineering

### Lesson 44 — GitHub Actions Observability, Monitoring, Reliability & Advanced Automation

Lesson 43 focused on building and delivering containers.

Lesson 44 will focus on operating and monitoring your automation infrastructure.

### Planned curriculum

| # | Topic |
|---:|---|
| 1 | GitHub Actions observability architecture |
| 2 | Workflow execution monitoring |
| 3 | Job and step performance analysis |
| 4 | GitHub Actions logs |
| 5 | Workflow summaries |
| 6 | Job summaries with `$GITHUB_STEP_SUMMARY` |
| 7 | Custom workflow metrics |
| 8 | GitHub Actions REST API monitoring |
| 9 | Workflow failure notifications |
| 10 | Slack and Microsoft Teams notifications |
| 11 | Email notifications |
| 12 | Scheduled health checks |
| 13 | Automated workflow recovery |
| 14 | Retry strategies |
| 15 | Failure handling |
| 16 | Timeout management |
| 17 | Runner monitoring |
| 18 | Self-hosted runner scaling |
| 19 | Runner groups and access control |
| 20 | Cost optimization |
| 21 | GitHub Actions usage analysis |
| 22 | Monitoring with Prometheus |
| 23 | Monitoring with Grafana |
| 24 | Centralized CI/CD dashboards |
| 25 | Deployment monitoring |
| 26 | Release health monitoring |
| 27 | Incident response automation |
| 28 | Automated issue creation |
| 29 | Automated incident reports |
| 30 | Complete CI/CD observability project |

**Final objective:** Build an observable CI/CD system that detects workflow failures, collects execution information, reports problems, monitors deployments, and supports operational troubleshooting.

**Next milestone:** Complete the Lesson 43 Docker foundations, GHCR publishing, and Trivy exercises first. Those three areas provide the foundation for the rest of the project.
