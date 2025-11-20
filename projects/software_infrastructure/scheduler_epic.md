# Scheduler EPIC — AID2E Workflow Scheduler Overview

This repository contains, Python-first scheduler prototype and developer tooling that we use to orchestrate compute-heavy simulation and optimization tasks for the AID2E (AI-assisted Detector Design for EIC) project. The codebase focuses on scheduling primitives, policy experimentation, and simple operational helpers to support distributed simulation workloads (for example, Geant4-based detector simulations) and integration points with PanDA / iDDS submission systems used by large experiments.

The goal is to provide a readable, extensible scheduler baseline we can iterate on quickly while integrating into the AID2E distributed workflow: queueing, dispatching, retry/backoff, and light-weight lifecycle management for jobs that drive multiobjective detector-design optimization experiments.

---

## Why this repository matters to AID2E

- AID2E requires a scalable, automated way to run large numbers of expensive Geant4 simulations and downstream evaluation tasks across distributed compute resources.
- This scheduler prototype is intended as both a local testbed and a building block for tailored integrations with PanDA and iDDS, which handle large-scale submission, data movement, and resilience in production-grade workflows.
- The repository's emphasis on transparent parameterization and modular policies lets us experiment with resource-aware scheduling strategies and optimization-driven dispatch decisions that matter for multiobjective detector design (performance vs. cost vs. geometry constraints).

---

## What this repo implements

- Core scheduling loop implemented in Python: task representation, in-memory queueing, basic worker dispatch and lifecycle hooks.
- Modular policy layer: pluggable scheduling policies (FIFO, priority) and clear interfaces for adding fairness, weighted scheduling, or resource-awareness.
- Shell helpers and small scripts: bootstrap local runs, generate synthetic workloads, and run example dispatch loops for development and demos.
- Configuration-driven behavior: YAML/JSON configuration for scheduling parameters, retry/backoff, and basic resource declarations.
- Lightweight telemetry hooks and structured logging to make it straightforward to add Prometheus metrics or exporters later.

Languages: primarily Python (implementation and tests) with small shell helpers for developer workflows.

---

## Current status (where we are now)

- Working prototype of core scheduler primitives (task objects, queue, dispatcher, worker loop).
- Basic policies implemented: FIFO and a simple priority queue.
- Shell scripts exist for local launch, basic workload generation, and example invocations that mimic small-scale PanDA/iDDS submissions.
- Early integration points: interfaces and adapters planned for PanDA / iDDS submission translation are sketched; a minimal adapter exists to demonstrate conceptual integration but is not production-ready.
- Unit tests present for core components; coverage is partial and focused on the scheduler loop and policy behavior.
- Documentation is developer-oriented: inline comments and a top-level README describe how to run local experiments. High-level project documentation and end-to-end examples are minimal.
- Not yet ready for production: no HA control plane, persistent distributed state, robust failure-handling at PanDA scale, or integrated metrics exporters.

---

## Planned work (near- and mid-term, aligned to AID2E goals)

Near-term (next sprints)
- Complete unit/integration test coverage for scheduler primitives and policy interfaces.
- Stabilize configuration parsing and validation; add schema checks for task descriptors used by AID2E workflows.
- Implement a small, pluggable persistence backend (file/SQLite) so in-flight work can survive restarts for local and small-cluster tests.
- Add basic metrics (Prometheus counters/gauges) and improve structured logging to support monitoring during large-scale experiment runs.
- Harden the PanDA/iDDS adapter: implement reliable task translation, submission, and status mapping for Geant4 simulation jobs.

Mid-term
- Add richer scheduling policies: fair-share, weighted priorities, resource-aware placement (CPU/GPU/memory), and rate-limiting tuned for simulation bursts.
- Support stateless worker models that poll the dispatcher and can be scaled horizontally by the PanDA/iDDS back-ends.
- Provide example AID2E pipelines: parameter sweeps and multiobjective optimization experiments that show integrated end-to-end execution from parameter generation through evaluation.
- Integrate provenance and basic data-product tracking so AID2E optimization outputs are reproducible and auditable.

Longer-term
- Explore preemption policies, autoscaling strategies for worker pools, and tighter integration with PanDA for large production runs.
- Add a compact web UI for visibility and simple control for experiment leads and operators.
- Expand to support calibration/alignment workflows and Detector-2 design studies with the same distributed scheduling primitives.