# FFLS reproducibility and verification routes

Run the primary integrity and witness route from the package root:

```bash
python supplementary/code/run_ffls_certificate.py
```

This route validates:

- exact direct substitution of displayed finite envelopes;
- selected rational continuum witnesses for the SWRO and energy-hub cases;
- required audit/certificate file presence;
- canonical cardinality summaries;
- proof-carrying certificate checks; and
- SHA-256 manifest entries.

It does **not** replace the supplied complete branch-status records. Full Reserve and PV branch logs are retained in the frozen Zenodo archival package. The PV branch audit can also be rerun separately using the scripts included in the archival package.

Locked benchmark statuses:

```text
k_R = 5
k_EV = 2
k_D = infinity
k_H = infinity
```

## Complete frozen package

The complete reproducibility archive, including full branch logs, checkpoint outputs, proof-carrying certificates, manifests, and all machine-readable evidence, is archived at:

**https://doi.org/10.5281/zenodo.22166445**

This GitHub repository is a public code/documentation mirror. The Zenodo record is the frozen archival version associated with the article.

## SOFIE v2 measured-data applicability audit

The SOFIE audit is independent of the four FFLS cardinality calculations. It is a measurement-to-envelope applicability audit only.

The raw SOFIE database is obtained from Zenodo DOI `10.5281/zenodo.12744385` and is accepted only when its MD5 is `6de82b1c4df99a83dfb355a40decc8ab`.
