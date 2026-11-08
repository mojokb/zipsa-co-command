# Conditional performance evidence

Apply only when performance is an acceptance criterion or the task measures, compares or reports a speedup/regression. Do not add benchmarks to unrelated fixes/features or promote optional measurements into completion gates. Use existing authorized environments and harnesses; this grants no execution or shared-resource authority.

- Before measuring, name the user-visible claim, metric/unit, workload and timed boundary. Inspect what the harness counts and excludes. Select an acceptance threshold only from the confirmed requirement, not from the observed result.
- Compare equivalent versions, browser/tool revisions and options, build mode, data, concurrency, cache state and infrastructure. Preserve original failures when a tool/environment changes, then rerun affected comparisons; never combine unlike timings into one result.
- Verify outputs, errors/timeouts/retries and completed work alongside timing. Confirm that the intended operation actually ran inside the timed boundary. Fast failures, skipped work or unconsumed lazy results are not speedups.
- For comparative claims, repeat both sides enough to observe variability, interleave or otherwise control warmup/load drift, and report sample count and a suitable center/spread. An explicitly requested one-run estimate stays labelled as such and cannot establish superiority.
- Identify the measured bottleneck and relate microbenchmarks to the end-to-end path the user waits for. Do not infer user-visible improvement from an isolated helper's speed alone. If correctness, work accounting, comparability or evidence needed for the claim is missing, report inconclusive and name the gap rather than picking a winner.

Tasks define applicable workloads, correctness checks, environment controls and measurement procedures before implementation. Test records raw results and conditions with the target snapshot in existing evidence. Review checks whether the claimed improvement follows from those results, without rerunning benchmarks unless required or explicitly requested. Keep the concise conclusion with links to raw observations; do not invent performance numbers.
