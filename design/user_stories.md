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

### User Story 1: Researcher (Alex)

**Who is the user**

Alex is a third-year PhD student in a manipulation lab, preparing a CoRL submission. Alex compares a new policy against two baselines on three tasks, using the lab's shared Franka arm. The arm is shared by the whole lab, so Alex can book only two afternoons a week.

**What does Alex want to do with the tool**

Alex wants to log each trial during an afternoon session and, after every trial, know which of the six comparisons already have a conclusion. That way the remaining robot time goes only to comparisons that are still open. When the evaluation ends, Alex wants results that can go straight into the paper. (Use case 1: live early screening.)

**What needs and desires does Alex have for the tool**

Alex needs to fix the rules before the first trial, see after every trial which comparisons can stop, and know roughly how many trials the rest will take. Looking at the results that often must not weaken the guarantee, and the guarantee must cover all six comparisons together. Alex also needs everything required to rerun the analysis kept with the results, so reviewers can check it. Alex would like a summary that goes into the paper without retyping.

**What is Alex's skill level**

Alex writes Python every day to train models and is comfortable with the command line and YAML config files. Alex took a graduate statistics course and understands confidence intervals and p-values, but has not studied sequential tests or multiple-comparison corrections, and has no time to learn them before the deadline.

**Needs**

- **#1** As a Researcher, I want to fix alpha, delta and the comparisons when I create the study, so that the guarantee is set before any data arrives. [Need]
   - Acceptance: alpha defaults to 0.05.
   - Acceptance: alpha must be greater than 0 and at most 0.20; a larger value is rejected with a message that screening use rarely goes above 0.20.
   - Acceptance: after the first trial is logged, a change to alpha is refused; to use another alpha, create a new study.
   - Acceptance: the metric (success or progress) is chosen here too.
   - Acceptance: the report flags any alpha other than 0.05.
- **#2** As a Researcher, I want each comparison's current decision (A better / B better / no meaningful difference / inconclusive), so that I know which ones can stop. [Need]
- **#3** As a Researcher, I want to know how many more trials each comparison needs, so that I can plan the session. [Need]
   - Acceptance: the estimate uses the trials logged so far, not an assumed success rate. Pre-study power analysis stays Extensible.
- **#4** As a Researcher, I want one guarantee to cover all comparisons together, so that many comparisons do not make a false conclusion likely. [Need]
- **#5** As a Researcher, I want to check results at any time without weakening the guarantee, so that I can stop as soon as the evidence is enough. [Need; non-functional]
- **#6** As a Researcher, I want everything needed to rerun the analysis kept with the results, so that others can check the conclusion. [Need]
- **#7** As a Researcher, I want a paper-ready summary of every comparison, so that no number is copied wrong. [Desire]

### User Story 2: Operator (Sam)

**Who is the user**

Sam is an undergraduate research assistant who works in Alex's lab, two three-hour shifts a week. Sam runs trials for Alex: places the objects, starts the policy, watches the robot finish, judges success or failure, and resets the scene. Sam stands beside the arm for the whole shift, often holding an object, with a laptop on a cart nearby.

**What does Sam want to do with the tool**

Sam wants to record each result within a few seconds of judging the trial, then reset the scene and run the next one. When Sam records something wrong, Sam wants to fix it without calling Alex. By the end of the shift, Sam wants to be sure every trial was recorded. Deciding which comparisons can stop is Alex's job, not Sam's.

**What needs and desires does Sam have for the tool**

Sam needs to record each result in a few seconds with very little typing, have a mistyped name caught on the spot, fix a wrong entry without asking Alex, and never lose a trial already recorded. Sam would like to note how far the robot got and why it failed in the same step as the result.

**What is Sam's skill level**

Sam is a second-year mechanical engineering student. Sam can follow a written checklist and type a short command, but does not write Python and knows no statistics. Sam learned the tool in a ten-minute walkthrough from Alex.

**Needs**

- **#8** As an Operator, I want to record a result in seconds with little typing, so that logging does not slow the session. [Need]
   - Note: CLI, GUI or both is left to the Component Spec. The professor's "GUI to take data in" is one way to meet this.
- **#9** As an Operator, I want to fix a wrong entry myself, so that I do not have to ask Alex. [Need]
   - Note: the original entry stays visible after the fix, because Alex needs an auditable record (story 6).
- **#10** As an Operator, I want to note progress and the failure reason with the result, so that I need no separate notebook. [Desire]
   - Note: failure reasons are picked from a list Alex sets up.
- **#11** As an Operator, I want mistyped policy or task names caught, so that a typo does not create a fake policy. [Need]
- **#12** As an Operator, I want recorded trials to survive a crash, so that I never rerun trials. [Need]

### User Story 3: Integrator (Jordan)

**Who is the user**

Jordan is a research engineer in Alex's lab who maintains the lab's LIBERO evaluation script. Every night the script runs a new checkpoint for thousands of simulated rollouts on the lab's GPU machines and writes the results to a CSV file. Before the team builds on a new checkpoint, Jordan compares it with the previous one.

**What does Jordan want to do with the tool**

Jordan wants conclusions from the results the script already produces, without rewriting the script or rerunning anything. For each new checkpoint, Jordan wants to know which tasks improved, which got worse, and which have too few rollouts to tell.

**What needs and desires does Jordan have for the tool**

Jordan needs to feed in the existing results file as it is, and to see per task whether a new checkpoint is worse than the old one. Jordan would like to send each rollout to evallog from inside the script while a run is still going.

**What is Jordan's skill level**

Jordan is an expert Python programmer who builds evaluation pipelines and runs jobs on GPU machines. Jordan knows success rates and averages well, but rarely uses confidence intervals and has never needed a multiple-comparison correction.

**Needs**

- **#13** As an Integrator, I want to use my script's results file as it is, so that I need not rewrite or rerun anything. [Need]
   - Note: covers the professor's "CSV file input".
- **#14** As an Integrator, I want to send each rollout from my code as it finishes, so that conclusions stay current during long runs. [Desire]
   - Note: covers the professor's "API input". Python API or HTTP is left to the Component Spec.
- **#15** As an Integrator, I want to see which tasks a new checkpoint made worse, or cannot yet tell, so that regressions do not slip through. [Need]

### User Story 4: Re-analyst (Riley)

**Who is the user**

Riley is a postdoc at another university writing a survey of vision-language-action policies for manipulation. Riley has no robot. Riley's material is the result tables in about ten papers and the public RoboArena records.

**What does Riley want to do with the tool**

Riley wants to check which published claims hold up: whether "ours 19/25 vs. baseline 14/20" is a real difference, whether reported LIBERO numbers fall inside intervals from fresh rollouts, and whether paper claims agree in direction with RoboArena head-to-head results. (Use case 2: retrospective re-analysis.)

**What needs and desires does Riley have for the tool**

Riley needs intervals and a test for counts copied from papers, a way to put those counts next to trial-level results, RoboArena records that can be analyzed without hand conversion, comparisons on RoboArena's progress score, and one policy under different names treated as one. Riley would like to enter a whole survey table at once instead of one comparison at a time.

**What is Riley's skill level**

Riley reads papers critically and knows standard statistics well, including confidence intervals and why small samples mislead. Riley works in Python notebooks with pandas, but does not want to learn a new data format.

**Needs**

- **#16** As a Re-analyst, I want intervals and a test for paper counts such as 19/25 vs. 14/20, so that I can judge a claim without raw trials. [Need]
- **#17** As a Re-analyst, I want paper numbers next to trial-level results for the same policy, so that I can see whether they agree. [Need]
- **#18** As a Re-analyst, I want to analyze RoboArena records directly, so that I need no hand conversion. [Need]
- **#19** As a Re-analyst, I want one policy under different names treated as one, so that joins do not miss matches. [Need]
- **#20** As a Re-analyst, I want to enter a whole results table at once, so that a survey is not dozens of entries. [Desire]
- **#21** As a Re-analyst, I want to compare on RoboArena's progress score, so that comparisons can be decided when full success is rare. [Need]

### User Story 5: Reader (Morgan)

**Who is the user**

Morgan is the professor who leads Alex's lab and advises eight students. Morgan decides which projects get robot time and when a result is ready to submit. Morgan sees evallog's output in weekly group meetings and in drafts that students send.

**What does Morgan want to do with the tool**

Morgan wants to read a student's report and, within a minute, decide whether the result is solid enough to submit, needs more trials, or should be dropped. Morgan never logs data or runs the tool.

**What needs and desires does Morgan have for the tool**

Morgan needs to see every comparison's conclusion, trial count and certainty in one view, and to see the rules the study used, so that a result tuned after the fact would stand out. Morgan would like to see why each policy failed, to steer the next round of work.

**What is Morgan's skill level**

Morgan is an expert in robot learning and understands confidence intervals and p-values. Morgan does not install software for students' projects, and reads an HTML report on a laptop or a projected slide.

**Needs**

- **#22** As a Reader, I want every comparison's conclusion, trial count and certainty in one view, so that I can judge the result in under a minute. [Need]
- **#23** As a Reader, I want failure counts by reason for each policy, so that I can steer the next round. [Desire]
- **#24** As a Reader, I want the report to show the study's rules and any change to them, so that I can trust nothing was tuned afterward. [Need]

### User Story 6: Beginner (Casey)

**Who is the user**

Casey is a software developer who builds robots at home in the evenings. Casey bought a low-cost SO-101 arm, followed the LeRobot tutorial, and trained two checkpoints of the same policy on a pick-and-place task. No one helps: Casey is the researcher, the operator and the reader at once.

**What does Casey want to do with the tool**

Casey wants to find out whether the newer checkpoint is really better than the older one. Casey does not know how many trials that takes, and wants the tool to say when the evidence is enough.

**What needs and desires does Casey have for the tool**

Casey needs to start a comparison without choosing any statistical settings, to be told how to set up trials so the comparison is valid, and to get the conclusion in plain words with a one-line reason. Casey would like error messages that say what to fix, so that a setup mistake does not end the evening.

**What is Casey's skill level**

Casey writes Python at work and can follow a tutorial's commands, but knows no statistics and has never heard of a confidence interval. Casey reads documentation only when stuck.

**Needs**

- **#25** As a Beginner, I want to start a comparison without choosing any statistical settings, so that I can begin right away. [Need]
- **#26** As a Beginner, I want the conclusion in plain words with a one-line reason, so that I understand it without statistics. [Need]
- **#27** As a Beginner, I want error messages that say what to fix, so that I do not get stuck. [Desire]
- **#28** As a Beginner, I want to be told how to set up valid trials, such as the same starting positions for both checkpoints, so that no trial is wasted. [Need]

### User Story 7: Benchmark maintainer (Quinn)

**Who is the user**

Quinn is a research engineer who maintains a public leaderboard for a simulated manipulation benchmark. Groups submit policies; each one runs on 10 tasks with 50 episodes per task, and the leaderboard ranks them.

**What does Quinn want to do with the tool**

Quinn wants the leaderboard to show which policies are actually different, instead of ranking them by gaps smaller than the noise. Each leaderboard release is one fixed study, so a new submission waits for the next release.

**What needs and desires does Quinn have for the tool**

Quinn needs to compare many policies at once and know which differences are real, and to show results per task as well as overall.

**What is Quinn's skill level**

Quinn is an expert Python programmer who runs automated pipelines. Quinn knows statistics well, including the multiple-comparison problem, and wants the method documented well enough to cite on the leaderboard page.

**Needs**

- **#29** As a Benchmark maintainer, I want to know which of many policies truly differ, so that the leaderboard does not rank noise. [Need]
- **#30** As a Benchmark maintainer, I want results per task and overall, so that users see where each policy is strong. [Need]

### User Story 8: Instructor (Taylor)

**Who is the user**

Taylor teaches a graduate course on robot learning. Every year, students present results such as "15/20 vs. 12/20" as clear wins, and Taylor wants a lecture that shows why such a gap can be noise.

**What does Taylor want to do with the tool**

Taylor wants to replay a recorded study in class, trial by trial, so that students watch the conclusion form and see when stopping early is safe. Then Taylor wants students to repeat it in a homework notebook.

**What needs and desires does Taylor have for the tool**

Taylor needs to show a recorded study unfolding trial by trial, and needs small example data that runs on a student laptop without large downloads. Taylor would like to set up a simulated study with known true success rates, so that students can check the tool against the right answer.

**What is Taylor's skill level**

Taylor is an expert in robot learning and statistics and builds lecture demos in Jupyter. Taylor's students know Python basics and introductory statistics.

**Needs**

- **#31** As an Instructor, I want to replay a study trial by trial as its conclusion forms, so that students see why early stopping can be trusted. [Need]
   - Note: the replay animation is Phase 2 in the Project Description, with no timeline slot.
- **#32** As an Instructor, I want small example data that runs on a laptop, so that the whole class can follow. [Need]
- **#33** As an Instructor, I want a simulated study with true rates I choose, so that students can check the tool against the answer. [Desire; Extensible, after Dec 16]

### User Story 9: Methods researcher (Avery)

**Who is the user**

Avery is a PhD student who studies how robot policies should be evaluated. Avery's thesis compares stopping rules and needs real trial-level logs to test them on. Avery has no robot and relies on public data.

**What does Avery want to do with the tool**

Avery wants to replay existing trial logs, in their real order and in many random orders, and measure how early a decision could have been reached and how often it matches the full-data result. Avery then wants to compare those numbers with Avery's own method on the same data.

**What needs and desires does Avery have for the tool**

Avery needs to replay existing logs and get the spread of stopping points and the agreement with the full data, and needs a clean trial-level dataset in one documented format. Avery also relies on reports that state the method and settings behind each conclusion (story 24).

**What is Avery's skill level**

Avery is an expert in statistics, fluent in Python, and reads the source code of the tools Avery uses.

**Needs**

- **#34** As a Methods researcher, I want to replay a log in its real order and many random orders, so that I can measure stopping time and agreement with the full data. [Need]
- **#35** As a Methods researcher, I want one clean, documented trial-level dataset (LIBERO and RoboArena), so that I can study evaluation without collecting data. [Need]

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
