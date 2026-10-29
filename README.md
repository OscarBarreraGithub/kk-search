# kk-search

Data-access audit and public-source collection for **arXiv:2610.31458**, *Evidence for Kaluza-Klein excitations of the graviton, gluon and quark at LHC*.

**Status: data collection, not a completed reproduction.** No new signal fit, significance calculation or discovery claim has been made. The snapshot directory is dated 2026-10-28; retrieval timestamps in the original collection use UTC.

## Start on a machine with FASRC access

```bash
git clone https://github.com/OscarBarreraGithub/kk-search.git
cd kk-search
python3 scripts/materialize.py
```

This restores the collected papers, figures, code, histograms and data inventories **offline from the archive in this repository**. Python 3.10+ is sufficient. The archive is divided into small transport parts because this repository was uploaded through the GitHub connector; the materializer checks every part and the combined archive before extraction.

Read [the access report](docs/KK_Data_Access_Report.pdf) and [the FASRC instructions](docs/FASRC.md).

To retrieve the four complete event/simulation files that were tested during collection:

```bash
python3 scripts/restore_samples.py --execute
python3 kk_data_access_2026-10-28/verify_package.py
```

The four files total **251.6 MB** and are downloaded from their public CERN URLs with size, Adler-32 and SHA-256 checks. They are not stored in normal Git history. The **[complete 296 MB collection is published as a GitHub release](https://github.com/OscarBarreraGithub/kk-search/releases/tag/data-2026-10-28)**, including all 953 files and the four samples. GitHub's runner successfully restored the sources, downloaded the samples, verified every inventoried checksum and published the ZIP, report and ZIP checksum. You may download that release instead of restoring the samples separately.

## What is preserved

| Material | Collected |
|---|---|
| Scientific sources | 30 papers and 561 official figure/table PDFs |
| Public CMS analyst repository | Pinned source tree, 57 ROOT files; 48 exported TH1 histograms |
| Additional numerical input | Provisional 44-bin inclusive four-jet spectrum from a secondary repository |
| CERN inventory | 34 records, with explicit file lists, byte sizes and checksums |
| Sample validation | Four complete files tested; 120,814 total entries, including 10,000 simulated entries |
| CMS auxiliary data | 2016 validated-run mask, luminosity, prescales and normtag files |
| Provenance | Source URLs, commit pins, failed downloads, SHA-256 inventory and validation results |
| Work performed | Collection scripts, inventory builder, report generator, access report and continuation instructions |

The archive contains 949 files. Restoring the four CERN samples gives the original 953-file collection. Collection scripts are at repository root; the snapshot is restored to `kk_data_access_2026-10-28/`. Small inventories are also directly browsable under [`inventory/`](inventory/).

## First bulk dataset: CMS 2016 G/H JetHT

```bash
python3 kk_data_access_2026-10-28/acquire_events.py \
  --record 30525 --record 30558 \
  --out /path/to/your/lab/storage/kk-data --max-gb 320
```

This is a **dry run**: 142 files, 244,738,738 events and 310.24 GB. Add `--execute` only when the destination is ready. Plan additional space for outputs. Use your lab's approved transfer/compute arrangements; no Harvard or CERN credentials are required for these public files.

## Limits that matter for the reproduction

- CMS 2016 G/H and ATLAS 2015-2016 open data cover only part of the published Run 2 exposure. Full relevant Run 3 events were not established as publicly available.
- The public CMS code snapshot predates the final erratum/addendum. It is not a certified final likelihood package; referenced picotrees, custom classes and final workspace locations have not all been obtained.
- Official HEPData exports were blocked by access challenges during collection. The secondary 44-bin copy remains provisional. See [`inventory/hepdata_access.json`](inventory/hepdata_access.json).
- The original and broad-resonance CMS searches reuse the same collisions; they are not independent evidence. NanoAOD/MiniAOD/PF variants and trigger streams also overlap.
- The small test files validate transport and format, not the presence of the claimed high-mass events. The ATLAS MC test file is a Sherpa single-photon sample inside the broad QCD collection.
- The full CMS 310 GB and ATLAS 49 TB datasets have **not** been collected into this project.

See [the work log](docs/WORK_LOG.md) and [third-party attribution](docs/PROVENANCE.md). The public sources retain their own licensing and citation requirements; this repository does not relicense them or imply endorsement by CMS, ATLAS, CERN or Harvard.
