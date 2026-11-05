# roboeval

## Abstract

Course project for CSE 583 (Software Engineering for Data Science), University of Washington, Autumn 2026.

## Problem

Robot learning researchers decide whether a new policy is better by running evaluation rollouts, in simulation or on a real robot. This is expensive: comparing 1 baseline and 3 new policies on 20 tasks with 20 trials each takes 1,600 rollouts. On real hardware, every rollout needs an operator, so most papers run only 10–40 trials per condition and report a bare success rate with no uncertainty.

This leads to two failures:

- **Wasted rollouts.** Every planned trial is run, even when the answer is already clear after a few.
- **False conclusions.** Small samples, checking results early, and comparing many tasks at once all make "Policy A beats B" claims that are just noise.

## What roboeval solves

roboeval tells you, after every trial, whether you can stop evaluating, for each policy and each task, while keeping the chance of a false conclusion below a level you choose (e.g. 5%).

- Stop early when the result is clear, and spend the saved trials on tasks that are still undecided.
- Compare several new policies against one baseline across many tasks.
- Get a report you can put in a paper: confidence intervals, decisions, and failure modes.

## Our approach

1. **Log** each trial with a fixed schema: policy, task, initial condition, outcome, failure mode.
2. **Test** each policy-task pair with anytime-valid sequential tests, which stay valid no matter how often you check the results.
3. **Correct** for many comparisons at once (family-wise or false-discovery-rate control).
4. **Decide** after every trial: win, loss, give up, or continue.
5. **Report** results as tables and an HTML summary.

roboeval works with results from simulation benchmarks and real robots, and is a lightweight Python library that plugs into existing evaluation scripts. We validate its statistics by simulation (does a 5% error rate really stay at 5%?) and demonstrate it on simulated and real-robot evaluation data.

## Team

| Name | GitHub |
| --- | --- |
| Hao Lee | [@Haollll](https://github.com/Haollll) |
| Abhishek Joshi | [@15abhishek](https://github.com/15abhishek) |
| Suhang Xu | [@HangSensei](https://github.com/HangSensei) |
| Chi-Lung (Kevin) Ma | [@Kevinma0215](https://github.com/Kevinma0215) |

## License

[MIT](LICENSE)
