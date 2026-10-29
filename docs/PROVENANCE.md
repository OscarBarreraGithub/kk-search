# Provenance and third-party material

This project preserves a research snapshot. Source publications, experimental data and upstream code retain their own copyrights, licenses and attribution requirements. No blanket license is applied to the collected third-party material.

- Target: [arXiv:2610.31458](https://arxiv.org/abs/2610.31458).
- Original CMS paired-dijet result plus erratum/addendum: [arXiv:2206.09997v3](https://arxiv.org/abs/2206.09997v3).
- Broad-mediator reinterpretation, now merged into that result: [arXiv:2507.17884v2](https://arxiv.org/abs/2507.17884v2).
- Public analyst code: `tw-hu/CMSAnalysis`, commit `8c4e503bcf874159240cd81096fab2ee0c57b95d`.
- Additional setup README: `izisopou/READMEs`, commit `012184e3dd2216206216d0bb2d2d0d0a5b75e526`.
- Secondary spectrum: `hftsoi/symbolfit`, commit `d6c8bf035bedf30da4e8f4ae777dc6ca5c453cdf`, `examples/datasets/dijet_pair/dataset.py`; original license preserved in the snapshot.
- CERN dataset titles, record identifiers, DOIs and license metadata are preserved in `inventory/dataset_inventory.json` and the restored original metadata.

The restored `download_log.jsonl` records retrieval URLs, times, hashes and failures for the collection pipeline. `SHA256.json` identifies the exact delivered files. A few public repository files were retrieved through GitHub rather than the HTTP collector; their pinned identities are recorded separately in `code_provenance.json`.

The top-level collection/report-building scripts preserve the work performed. Their historical paths and dates refer to the original snapshot. The PDF and inventory were reviewed, but the physics code was not executed and the selected old software environment has not been rebuilt.
