# SOFIE v2 measured-data applicability audit

## Scope

This component supports the manuscript's measured-data applicability audit for the SOFIE PV-BESS-EV microgrid. It tests a reproducible measurement-to-envelope workflow. It is **not** a fifth FFLS benchmark, plant-specific FFLS validation, or evidence that the operating microgrid has `k_EV = 2`.

## Pinned public source

- Zenodo record: `12744385`
- DOI: `10.5281/zenodo.12744385`
- Dataset version used: `v2`
- Observation period: `2024-01-10` through `2024-06-26`
- Required database: `sofie_data_26-06_2024.db`
- Required MD5: `6de82b1c4df99a83dfb355a40decc8ab`
- Nominal battery-storage capacity stated by the official record: `38.4 kWh`

The third-party database is not redistributed. Download the pinned v2 file from the official Zenodo record and verify the MD5 before running the audit.

## Reproduction environment

Python dependencies: `pandas`, `numpy`, and `Pillow`.

The complete SOFIE audit script, derived outputs, QA tables, and chronological calibration/holdout figure are preserved in the frozen archival package:

**https://doi.org/10.5281/zenodo.22166445**

## Core reported results

| Variable | Calibration q05 / q50 / q95 | Holdout inside | Coverage |
|---|---:|---:|---:|
| PV daily generation | 4.0615 / 19.735 / 71.8279 kWh/day | 37/41 | 90.24% |
| EV daily demand | 0 / 15.485 / 60.4636 kWh/day | 38/41 | 92.68% |
| Nominal-capacity-scaled daily SOC range | 1.920 / 7.296 / 21.888 kWh-equivalent/day | 38/41 | 92.68% |

The SOFIE audit does not alter any of the four locked FFLS benchmark cardinalities.
