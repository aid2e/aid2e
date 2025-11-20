# dRICH-MOBO — Project homepage

## Overview

This repository couples full simulations run in the eic-shell environment with scalable execution backends to explore detector design choices efficiently. The codebase integrates Slurm, joblib, and PanDA/IDDS so simulation campaigns can run in parallel across local clusters and distributed resources.

## Design and architecture (high level)

- Frontend: experiment descriptors and parameter sets that define a candidate detector configuration.
- Simulation layer: eic-shell based simulation + reconstruction that produces physics metrics (photon yield, angle resolution, PID metrics, etc.).
- Execution layer:
  - SlurmRunner: templated Slurm job scripts and runners to launch cluster jobs.
  - joblib mode: lightweight parallel execution for local development and fast feedback.
  - PanDA/IDDS connector: integration for large-scale, fault-tolerant distributed execution and data staging.
- Data & results: structured storage of outputs and metadata to enable tracking, visualization, and post-processing.
- Lightweight orchestration: components to submit batches of configurations, monitor jobs, collect outputs, and feed results back into analysis.

## Problem definition

### Motivation

- Designing the dRICH involves many continuous and discrete choices (geometry, materials, photodetector layout and thresholds, radiator options) where objectives compete (e.g., resolution vs. material budget vs. cost).
- High-fidelity simulations (e.g., Geant4-level within eic-shell) are computationally expensive; exhaustive search is impractical.


### Key technicalities

- Objectives: physics-derived metrics from full simulation and reconstruction.
- Decision variables: geometry parameters, material thicknesses, sensor placements, and readout settings.
- Parallelization: evaluations are parallelized across multiple levels — in-process concurrency via joblib, cluster scheduling and array jobs via SlurmRunner, and distributed campaigns via PanDA/IDDS. This multi-tier parallelism reduces wall-clock time and increases throughput.
- Execution robustness: job templating, retry logic, and data staging are implemented to address transient failures and large-scale campaign needs.
- Provenance: metadata, logs, and outputs are stored together to allow campaign replay and diagnostics.