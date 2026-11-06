"""Fail the container build if CVE-2026-111497 decoders remain installed."""

import importlib.metadata
import json
import subprocess

import brotli
import urllib3.response
from packaging.version import Version

versions = {}
for package, floor in [("Brotli", "1.2.1"), ("brotlicffi", "1.2.1.0")]:
    try:
        installed = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        if package == "Brotli":
            raise
        continue
    if Version(installed) < Version(floor):
        raise RuntimeError(f"Vulnerable {package}: {installed}")
    versions[package] = installed

packages = subprocess.check_output(["apk", "info", "-v"], text=True).splitlines()
native = next(p.removeprefix("brotli-libs-") for p in packages if p.startswith("brotli-libs-"))
comparison = subprocess.check_output(
    ["apk", "version", "-t", native, "1.2.1-r0"], text=True
).strip()
if comparison not in {"=", ">"}:
    raise RuntimeError(f"Vulnerable native brotli-libs: {native}")
versions["brotli-libs"] = native

# Exercise the decoder selected by the HTTP client with ordinary compressed data.
payload = b"Wizarr Brotli security build verification"
decoder = urllib3.response.BrotliDecoder()
if decoder.decompress(brotli.compress(payload)) + decoder.flush() != payload:
    raise RuntimeError("HTTP client Brotli decoding failed")
versions["http_decoder"] = urllib3.response.brotli.__name__
print(json.dumps(versions, sort_keys=True))
