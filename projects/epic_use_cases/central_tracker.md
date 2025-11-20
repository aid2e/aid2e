# Central Tracker Optimization

A compact toolbox for designing and tuning a central tracking detector using simulations, reconstruction code, and automated parameter searches. The primary objective is to optimize momentum resolution by varying detector parameters and reconstruction settings.

What we tune
- Geometry: number and placement of barrel layers and forward/backward disks.
- Sensor/readout: pitch, segmentation, and material budget.
- Reconstruction and algorithmic parameters that affect track finding and fitting.

Current status
- Core Python tools and example experiments exist to run parameter scans (barrel layers, disks, etc.).
- Notebooks provide basic analysis and visualization.
- Result aggregation, pinned reproducible examples, and CI are minimal / in progress.

Next steps
- Add pinned example runs and synthetic-data configs for reproducibility.
- Improve result aggregation and add more advanced optimization methods (e.g., Bayesian optimization).
- Expand tests and documentation so new geometries and algorithms can be added easily.