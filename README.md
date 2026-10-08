# Verified Cardinality of Fully Fuzzy Linear Systems

Public code and reproducibility repository for the IEEE Access article:

**Verified Cardinality of Fully Fuzzy Linear Systems: A Certified Diagnostic Framework for Finite and Underdetermined Engineering Benchmarks**

## Publication status

Accepted for publication in **IEEE Access**.  
Final-files manuscript ID: **Access-2026-43698**.

## Authors

- Ghassan Malkawi
- Ahmed Abdelaziz Elsayed
- Firuz Kamalov
- Bakeel Hussein
- Eyad Adnan — corresponding author

## Locked benchmark results

- Reserve benchmark: `k_R = 5`
- PV-BESS-EV benchmark: `k_EV = 2`
- SWRO benchmark: `k_D = infinity`
- Energy-hub benchmark: `k_H = infinity`

## Archival reproducibility record

The frozen archival reproducibility package associated with the accepted article is available on Zenodo:

**DOI: 10.5281/zenodo.22166445**

https://doi.org/10.5281/zenodo.22166445

The Zenodo record is the archival version associated with the article. This GitHub repository is the public code/documentation mirror and may receive maintenance-only updates after publication. Scientific results and claim boundaries should be interpreted from the accepted article and the frozen Zenodo record.

## Reproducibility scope

The reproducibility materials support:

- exact direct-substitution checks for retained finite FFLS solutions;
- complete Reserve and PV-BESS-EV branch-audit evidence;
- exact-rational and proof-carrying verification routes;
- symbolic continuum certificates for the SWRO and energy-hub benchmarks;
- external published-example checks; and
- the SOFIE v2 measured-data applicability audit.

The SOFIE audit is a measured-data applicability audit only. It is **not** a fifth FFLS benchmark and does not alter the four locked benchmark cardinalities.

## Primary verification route

The frozen Zenodo archive contains the complete branch logs, certificates, manifests, outputs, and scripts required for the full integrity/witness route.

From the complete extracted archival package:

```bash
python supplementary/code/run_ffls_certificate.py
```

## SOFIE v2 source

The third-party SOFIE raw database is not redistributed. Use the pinned public dataset:

- DOI: `10.5281/zenodo.12744385`
- required file: `sofie_data_26-06_2024.db`
- required MD5: `6de82b1c4df99a83dfb355a40decc8ab`

## Citation

Until the final IEEE article DOI is assigned, cite the frozen reproducibility archive as:

> Malkawi, G., Elsayed, A. A., Kamalov, F., Hussein, B., & Adnan, E. (2026). *Verified Cardinality of Fully Fuzzy Linear Systems: A Certified Diagnostic Framework for Finite and Underdetermined Engineering Benchmarks* (Version V5R7). Zenodo. https://doi.org/10.5281/zenodo.22166445

## Contact

Corresponding author: **Eyad Adnan**  
Email: **eadnan@hct.ac.ae**
