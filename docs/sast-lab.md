# SAST and merge gate experiment

- `d380ee6`: Added Bandit to CI. The scan passed.
- `29adbcc`: Added a dummy hardcoded password. Bandit reported
  B105, and the required CI check blocked merging.
- `3b4148a`: Renamed `password` to `value`. The scan passed,
  but the hardcoded string remained in the source code.
- `7a2e4e9`: Removed the unused dummy value and its comment.
  Bandit reported no issues, and both functional tests passed.

## Lesson learned

A passing SAST check does not prove that code is secure.
Reviewers must inspect whether the underlying problem was fixed.
Only synthetic data was used in this experiment.