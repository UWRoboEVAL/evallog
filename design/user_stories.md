# User Stories Design

Who is the user. 
What do they want to do with the tool. 
What needs and desires do they want for the tool. 
What is their skill level.


### Abhishek

1. Abhishek compares a new robot control model against a baseline in simulation. He wants a tool to read his automated logs and act as a strict referee against lucky streaks. He needs a lightweight checker to prevent false success claims without the overhead of heavy study-planning frameworks. Abhishek is an expert in Python but relies on established statistical methods.

2. Sarah tests a new manipulation policy on a physical robot. She wants a CLI tool to log each try and tell her exactly when to stop, minimizing manual scene resets. She needs a lightweight referee that translates raw stats into simple "stop" or "keep going" signals. Sarah knows Python but isn't a statistician.

3. David evaluates robot programs using public RoboArena datasets. He wants to automatically feed bulk trial records into a script to find exactly when a policy proved superior. He needs a tool that handles data imports and generates clean, publish-ready tables with error bars. David is highly proficient in Python scripting.

4. Dr. Elena directs a robotics lab and wants to standardize how students report policy improvements. She needs the tool to generate an easy-to-read final report showing confidence intervals so she can instantly verify claims and prevent cherry-picked results. Dr. Elena understands the statistics conceptually but does not write Python code.

5. Marcus maintains an automated evaluation pipeline for a shared robotics codebase. He wants a tool to automatically block GitHub pull requests if a new model isn't statistically better than the baseline. He needs it to run headless in CI/CD, ingest logs, and return strict system exit codes. Marcus is an expert in Python and MLOps but treats the statistics as a black box.

6. Jin competes in a public robotics challenge with a limited daily submission quota. He wants to compare local simulation runs to see if his latest policy tweak is genuinely better before submitting it to the official server. He needs a strict statistical referee that imports CSVs to prevent confirmation bias. Jin is advanced in Python and machine learning.

7. Chloe tests a navigation policy using two different physical cameras on a real-world obstacle course. She wants to stop manually walking the robot through the course as soon as one camera proves definitively better. She needs a responsive CLI that outputs a highly visible "STOP" signal while she manages the physical hardware. Chloe is an expert in ROS and Python but relies entirely on the tool for the math.

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

1. Embodied AI company: Kenji. Kenji is a machine learning engineer at an embodied AI startup. Every week he must decide whether a new checkpoint should replace the model on customer robots. He wants that decision backed by statistics, not by watching a few videos. He needs a clear ship-or-hold result with the error rate stated, plus a saved record of the trials behind it. Kenji is an expert Python developer who knows A/B testing.
2. Teaching: Dr. Lee. Dr. Lee teaches an undergraduate robotics course and wants to show students why 20 trials are often not enough to claim that one robot is better. She needs a short demo on public data that shows the decision changing as trials come in. Dr. Lee is comfortable with Python and wants to run it live in class.
3. Administrator: Ben. Ben is the systems administrator for a lab whose robot computers have no internet access. He wants to install evallog from a downloaded package. He needs few dependencies, a standard pip install, and support for Linux and macOS. Ben is highly technical but knows nothing about robot learning.
4. Accessibility: Ivan. Ivan is a robotics researcher who is color-blind and often reads reports with a screen magnifier. He wants to read evallog's report without relying on color to tell two policies apart. He needs charts with direct labels and tables with clear text that stay readable when enlarged. Ivan is highly technical and comfortable reading statistics tables.
5. User to design against: Victor. Victor is an eager student who wants his policy to look good. He checks the result after every trial, wants to stop the moment he is ahead, and might delete a bad session. The tool must keep its error rate valid even when results are checked after every trial, and it must record any deletion or restart made through the tool. Victor is technically capable, which makes this misuse easy.
6. User to design against: Gina. Gina is a graduate student who wants to show that her policy beats a rival's. She is tempted to count trials from easy tasks for her policy and trials from hard tasks for the rival. She might also log trials for only one of the two policies. The tool must warn when trials are unpaired or the two policies were not tested under matching conditions. Gina has intermediate technical skills and knows how the experiments are set up.
7. Partial-credit researcher: Hannah. Hannah is a researcher who scores trials with partial credit: 1 for full success, 0.5 for grasping the object but dropping it, and 0 for failure. She wants evallog to accept these scores instead of forcing her to round them to pass or fail. The statistics must stay valid for scores between 0 and 1. Hannah is highly technical and reads statistics papers when she has to.
8. Product manager: Tom. Tom is a product manager at a robotics company. He signs off on releases but does not read code or statistics. He wants to decide whether to approve a release. He needs a one-sentence conclusion, such as "the new version is better, tested at a 5% error rate," and one simple chart. Tom's technical skill is low, but he understands the product and its customers well.
9. New student: Lina. Lina is a first-year master's student who just joined a robotics lab. She wants to log her first evaluation without breaking anything. She needs a quick-start guide and examples she can copy. She also needs error messages that say what went wrong, such as a misspelled policy name. Lina has used Python in class notebooks but rarely uses the command line.
10. Research assistant: Diego. Diego is an undergraduate research assistant who resets the scene and records outcomes during long evaluation sessions. He wants to enter each result on a laptop next to the robot in a few seconds. He sometimes types the wrong outcome. He needs a safe way to correct the last entry, with the correction still recorded in the history. Diego is comfortable with computers but is not a programmer.
