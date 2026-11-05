# User Stories Design

## Hao

## User Story 1: Real-robot researcher

**Who is the user**

Majilong is a second-year PhD student in a robot learning lab. She trains manipulation policies and tests them both in simulation and on the lab's real robot arm. Every real-robot trial takes about a minute, and she has to reset the scene by hand each time, so she can only afford 20–40 trials per policy. Her advisor often asks whether her new method is really better, and with so few trials she is never sure whether a gain is real or just luck.

**What does she want to do with the tool**

She has just trained a new policy and wants to compare it with the baseline on 10 tasks. She wants to:

- Log each trial right after she runs it, and find out whether she already has enough evidence to stop, so she does not waste hours on trials whose answer is already clear.
- Spend the time she saves on the tasks that are still undecided.
- Make sure that when she reports "my method wins on 6 of 10 tasks", none of those wins is a lucky streak.

**What needs and desires does she have for the tool**

- A clear answer after each trial: *keep going*, *stop: new policy is better*, or *stop: no real difference*, with the confidence level stated.
- A one-line command she can type between robot resets, or a button she can press on a simple dashboard.
- Clean records of every trial, including the policy, task, starting position, outcome and why it failed, so she can show her advisor exactly what happened and rerun the analysis later.
- A final report with a results table, confidence intervals, and plots showing how the evidence built up, ready to paste into her paper.

**What is her skill level**

Majilong writes Python every day, uses the command line, and maintains her own training and evaluation code. She knows what a success rate and a p-value are, but she has never studied sequential testing or how to correct for comparing many tasks at once. She does not want to become a statistician; she wants the tool to make those decisions correctly and explain the result in plain language.

## User Story 2: Simulation benchmark engineer

**Who is the user**

Leo is a machine learning engineer on a robotics team. He evaluates several versions of a vision-language-action policy on a simulation benchmark with dozens of tasks. A full evaluation sweep takes most of a day on the team's shared GPUs, and he runs one every time the team changes a training or inference setting. Most of the time, the answer for many tasks is obvious long before the sweep finishes.

**What does he want to do with the tool**

He wants to compare three new policy versions against the current baseline on 40 tasks. He wants to:

- Call the tool from his existing evaluation script after every rollout, without changing how the script runs the simulator.
- Stop evaluating a policy–task pair as soon as the result is clear, and give the GPU time to the pairs that are still undecided.
- Get one summary telling the team which versions are better, worse, or no different, without being fooled by the large number of comparisons.

**What needs and desires does he have for the tool**

- A Python API that takes one rollout result at a time and returns the current decision for that comparison.
- Correct handling of many comparisons at once, with a simple choice between strict control (no false wins) and a looser setting for exploration.
- A study configuration file he can commit to the repository, so every sweep uses the same settings and can be reproduced.
- A machine-readable output (CSV) he can feed into the team's existing dashboards, plus an HTML report for weekly meetings.

**What is his skill level**

Leo is a strong Python developer who writes his own evaluation pipelines and is comfortable with configuration files, CI and command-line tools. He knows basic statistics such as t-tests and confidence intervals, but not anytime-valid methods or multiple-comparison corrections. He wants a tool that is lightweight, well documented and easy to drop into existing code.

## User Story 3: Researcher checking existing results

**Who is the user**

Priya is a postdoc writing the related-work section of a paper and reviewing submissions for a robotics conference. She often reads claims such as "our policy reaches 75% success, compared with 60% for the baseline" based on 20 trials. She also has access to public evaluation records, such as head-to-head real-robot comparisons, and wants to know whether those support the claims.

**What does she want to do with the tool**

She wants to check whether reported improvements are real, without running any new experiments. She wants to:

- Enter results reported in papers as simple counts (such as "19/25") and see the confidence interval for each.
- Import existing trial-by-trial records and replay them in their original order, to see when a reliable conclusion could have been reached.
- Compare a paper's claim with independent evaluation records of the same policies, to see whether they agree.

**What needs and desires does she have for the tool**

- An import command that reads a CSV or a public evaluation dataset and checks it for errors, telling her exactly which rows are invalid.
- A clear verdict for each claim: supported, not supported, or not enough data to tell.
- A note whenever a paper does not report the number of trials, since no interval can be computed without it.
- A table and a plot she can include in a review or in her paper's related-work section.

**What is her skill level**

Priya is comfortable with Python notebooks and has a solid statistics background, including hypothesis testing. She does not want to write her own analysis code for every paper she reads; she wants a fast, reproducible check that follows accepted statistical practice.

## Kevin

1. As a Researcher, I want to set alpha, delta and the list of comparisons once when I create the study, so that the error guarantee is fixed before any data arrives.
2. As a Researcher, I want to see, for each comparison, the current decision (A better / B better / no meaningful difference / inconclusive), so that I know which comparisons can stop.
3. As an Integrator, I want to import a CSV of policy results that my own script produced, so that I get decisions without re-running anything.
4. As a Reader, I want a plot of the interval narrowing over trials with the stopping point marked, so that I can see why the study stopped when it did.

## Suhang

4. Academic researcher: Priya. Priya is a PhD student comparing her new grasping policy with the lab's old one on a single robot arm, one trial at a time. Each trial needs a manual scene reset. She wants one short command to log each result and a clear "keep going" or "stop" answer. Priya writes Python every day but knows only basic statistics.
5. Simulation user: Arjun. Arjun evaluates each trained policy with thousands of simulated rollouts on rented GPUs. He wants to stop as soon as the answer is clear, to save compute. He needs a small Python API that takes one result at a time and returns the current decision. Arjun is an expert Python developer.
6. Embodied AI company: Kenji. Kenji is a machine learning engineer at an embodied AI startup. Every week he must decide whether a new checkpoint should replace the model on customer robots. He wants that decision backed by statistics, not by watching a few videos. Kenji is an expert Python developer who knows A/B testing.
7. Public data user: Sam. Sam is reviewing a paper that claims 15 of 20 successes for the new method, against 11 of 20 for the baseline. He wants to check whether the difference could be luck. He needs to enter the reported numbers, or import the authors' log, and get a plain answer. Sam is an experienced researcher who knows some Python.
8. Teaching: Dr. Lee. Dr. Lee teaches an undergraduate robotics course and wants to show students why 20 trials are often not enough to claim that one robot is better. She needs a short demo on public data that shows the decision changing as trials come in. Dr. Lee is comfortable with Python and wants to run it live in class.
