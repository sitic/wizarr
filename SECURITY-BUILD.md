# Patched Wizarr image

This fork applies upstream PR [#1502](https://github.com/wizarrrr/wizarr/pull/1502),
commit `bc1f910d24e77a236582e076fa886f2912a5a26c`, for CVE-2026-111497.
It raises the Python Brotli and brotlicffi minimums and updates their locked
versions. The runtime image also requires Alpine `brotli-libs>=1.2.1-r0`.

Run **Build patched Wizarr image** (`security-image.yml`) manually on `main`.
It builds natively for ARM64 and AMD64 using the committed lockfile. Each
build checks lockfile consistency, installed Python and native decoder
versions, and a normal round trip through urllib3's Brotli decoder. A failed
check prevents publication of that architecture; both must pass before the
shared tags are published.

Images are published to `ghcr.io/sitic/wizarr` with tags `latest`,
`brotli-fixed`, and `sha-<full-source-commit>`. Deploy the source-specific tag
or manifest digest to avoid silently changing the deployed build. The image
sets `APP_VERSION=2026.10.1+sitic.brotli1.2.1` and records its source revision in OCI
labels. The Python dependencies are not re-resolved in this workflow.

Keep existing application data and back it up before deploying. Once an
official release is independently verified to include the Python and native
fixes, the deployment can switch back to the upstream image.
