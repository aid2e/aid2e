# AID2EUtilities

AID2EUtilities is a compact toolkit of Python utilities and small shell helpers designed to bridge AID2E workflows with the ePIC software stack. The repository collects lightweight, reusable tools that make data movement, conversion, validation, and automated interactions with ePIC easier for researchers and engineers working in the AID2E ecosystem.

## What this project provides
- A set of Python utilities for:
  - Connecting to or preparing data for the ePIC stack (lightweight adapter functions and helpers).
  - Converting common dataset formats used in our workflows (utilities for HDF5, NetCDF, CSV and metadata normalization).
  - Validating dataset structure and metadata prior to ingestion into ePIC pipelines.
  - Small CLI wrappers and scripts to automate repetitive tasks (packaging, upload, quick summaries).
- A couple of shell helper scripts for quick environment setup and common operational tasks.
- Examples and templates showing common workflows (ingest, convert, validate — minimal examples included).
- Basic documentation to get started and examples to copy into existing pipelines.

## Target users and use-cases
- Researchers and engineers using AID2E who need to prepare, validate or move data into the ePIC stack.
- Rapid prototyping of data conversion and ingestion steps for experiments.
- Lightweight automation around ePIC operations (preprocessing, packaging, sanity checks).

Common workflows enabled:
- Convert lab output files into normalized HDF5/NetCDF with consistent metadata.
- Run pre-ingest checks and metadata validation before handing datasets to ePIC.
- Small automation scripts to package and upload datasets to a storage backend used by ePIC.

## Current status (where we are)
- Core conversion and validation utilities: implemented in a first-pass, working form.
- CLI wrappers and shell helpers: present for the most common operations.
- Examples: small examples and templates included to demonstrate typical usage.
- Documentation: README and inline docstrings present; a consolidated homepage (this description) added.
- Tests and CI: minimal unit tests exist for a few core utilities; broader test coverage and CI automation are still under development.
- Stability: the toolkit is usable for day-to-day tasks but is considered “alpha” — the public API may change as we harden interfaces and expand features.

## Planned work (roadmap)
Short-term (next 1–3 months)
- Increase unit test coverage and add CI (GitHub Actions) for basic linting and test runs.
- Flesh out example workflows with end-to-end demos (convert → validate → ingest).
- Stabilize core adapter interfaces used by ePIC integrations.

Medium-term (3–9 months)
- Add more robust format converters (additional edge cases, streaming support for large files).
- Improve metadata tooling: richer validation rules, schema versioning, and auto-correction suggestions.
- Package the toolkit for pip installation and release versioned artifacts.

Long-term
- Add a small service/daemon mode for automated watchers that detect new data and run conversion + validation pipelines automatically.
- Provide a set of higher-level integrations or SDK helpers specifically for common ePIC deployments used by the AID2E community.