## 2026-05-29
- Task 3 verification failed on undocumented FlyAI example values; corrected the reference to use numeric `--sort-type` examples and documented seat wording, and removed `one-way` from examples.
- FlyAI docs alignment note: `--journey-type` should use numeric direct/connecting or transit values, while one-way is represented by omitting `--back-date`; train seat wording should stay as `second class`.
- Task 5 verification needed a lowercase keyword fix because case-sensitive grep did not match `Template`/`Example`; added a lowercase template sentence so `template`, `placeholder`, and `example` now match.
