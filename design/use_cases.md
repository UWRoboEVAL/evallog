# Use Cases

Each use case describes one function of the tool. The use cases are extracted from the stories in `user_stories.md` and are listed in the order a user meets them.

Use Cases 1 to 6 are the first version. The section "Future Version" lists the functions that come after the first version is complete. The table at the end shows which stories each use case comes from.

## Use Case 1: Create a Study

### Who is the User?
*   **Persona/Role:** Study owner
*   **Context:** The researcher who owns an evaluation. They are about to compare one or more new policies against a <mark>baseline</mark> on one or more tasks, and they decide what is compared and how strict the conclusion must be. Readers later rely on these rules being fixed in advance.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   **Name the baseline, the policies and the tasks** to compare.
    *   **Choose the <mark>metric</mark> (success or progress) and the error settings.**
    *   **Save the settings as a file** that can be committed and reused.
*   **Operational Workflows:**
    *   *Precondition:* The tool is installed.
    *   *Standard Operations:* The user **runs one command or one API call and accepts the defaults**. The tool **creates a study folder with a settings file and an empty trial table**.
    *   *Edge/Exception Operations:* The tool **rejects an invalid setting with a message that says what to fix**. After the study is created, the tool **refuses a change to the settings**; the user **creates a new study** instead.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   **<ins>Defaults for every statistical setting</ins>**, so a beginner can start without choosing any.
    *   **<ins>One guarantee that covers all comparisons in the study together</ins>**, with **<ins>a choice between strict control and a looser setting</ins>** for exploration.
*   **Desires / Experience Preferences:** **A plain-language explanation of each setting.** **The same settings file reused across studies**, so every sweep is reproducible.

### What is Their Skill Level?
*   **Technical Proficiency:** Medium to High. They use Python, the command line and YAML files.
*   **Domain Knowledge:** They know robot policy evaluation and success rates. They do not know sequential tests or multiple-comparison corrections.

### Inputs and Outputs
*   **Inputs:** Study name, baseline, policies, tasks, metric, <mark>alpha</mark>, <mark>delta</mark>, maximum trials, <mark>correction method</mark>.
*   **Outputs:** A study folder that holds the settings file (`study.yaml`) and an empty trial table (`trials.csv`).
*   **Transformation:** The tool fills any missing setting with its default, checks every setting, builds the list of <mark>comparisons</mark> (each policy against the baseline, on each task), and writes the study folder.

### Assumptions and Open Questions
*   <mark>Assumption:</mark> A study has exactly one baseline. Every comparison is one policy against that baseline, on one task.
*   <mark>Assumption:</mark> The policies and tasks are known when the study is created. To add a policy later, the user creates a new study.
*   <mark>Uncertainty:</mark> Do the same default values suit a real-robot study with 20 to 40 trials and a simulation study with thousands of rollouts?

## Use Case 2: Log a Trial

### Who is the User?
*   **Persona/Role:** Operator
*   **Context:** The person or script that runs trials and records each outcome. This can be an assistant who stands beside a real robot, a researcher who runs their own trials, or an evaluation script that logs simulated rollouts.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Record the outcome of one trial right after it finishes.
    *   Mark which trials form a pair, so two policies are compared under the same starting condition.
    *   Add a progress score and a failure reason when they have them.
    *   Find out at once that an entry is wrong, and learn what to fix.
*   **Operational Workflows:**
    *   *Precondition:* The study exists (Use Case 1).
    *   *Standard Operations:* A human operator types one short command between scene resets. A script calls the Python API once per rollout. The tool checks the entry, saves the trial and confirms it.
    *   *Edge/Exception Operations:* The tool rejects an entry with a policy or task that is not in the study, a missing required field, or a score outside the allowed range. The tool warns when trials are unpaired, or when the two policies were not tested under matching conditions. After a crash or power loss, every trial already recorded is still there.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   One entry takes a few seconds and very little typing.
    *   The command line and the Python API record a trial in the same way.
    *   Scores between 0 and 1 are accepted, not only pass or fail.
*   **Desires / Experience Preferences:** Error messages in plain words that say what went wrong and what to fix. Guidance on how to set up valid trials, such as the same starting positions for both policies.

### What is Their Skill Level?
*   **Technical Proficiency:** Low to High. A human operator may not write Python and follows a written checklist. An engineer calls the API from an existing script.
*   **Domain Knowledge:** They can judge whether a trial succeeded. They may know no statistics.

### Inputs and Outputs
*   **Inputs:** Policy, task, outcome (success 0/1, or progress from 0 to 1), pair identifier; optionally a condition identifier and a failure reason.
*   **Outputs:** One new row in the trial table and a confirmation message, or one message for each problem (rejection or warning).
*   **Transformation:** The tool checks the entry against the trial table schema and the study settings, adds a trial identifier and a timestamp, and appends the row to the trial table.

## Use Case 3: Check Comparison Decisions

### Who is the User?
*   **Persona/Role:** Study owner
*   **Context:** The person or pipeline that must know whether a <mark>comparison</mark> is <mark>settled</mark>. A researcher decides during a session whether to run more trials. A script or CI pipeline acts on the result. An engineer decides whether a new checkpoint ships.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   **See the current <mark>decision</mark> for each comparison**: the new policy is better, the <mark>baseline</mark> is better, there is no meaningful difference, or keep going.
    *   **Stop collecting trials for comparisons that are settled**, and spend the remaining time on the <mark>open</mark> ones.
    *   **Use the decision in an automated pipeline**, for example to block a pull request.
*   **Operational Workflows:**
    *   *Precondition:* The study exists (Use Case 1). It may hold no trials yet; trials come from Use Case 2 or 4.
    *   *Standard Operations:* After any trial, the user **asks for the status**. The tool **shows one line per comparison with the decision, the number of trials and the <mark>interval</mark>**. A script **gets the same result from the Python API or from the exit code**.
    *   *Edge/Exception Operations:* The user **may check after every trial**; this does not weaken the <mark>guarantee</mark>. When a comparison reaches the <mark>maximum number of trials</mark> without a decision, the tool **reports it as <mark>inconclusive</mark>**. When a comparison has no <mark>paired trials</mark> yet, the tool **reports that it has no data**.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   **<ins>A stated error rate that stays valid however often the results are checked</ins>**, and that **<ins>covers all comparisons together</ins>**.
    *   **<ins>Support for both pass-or-fail outcomes and scores between 0 and 1</ins>**.
    *   **<ins>A machine-readable result for scripts and CI</ins>**.
*   **Desires / Experience Preferences:** **A highly visible "STOP" signal that can be read while handling hardware.** **The conclusion in plain words with a one-line reason.**

### What is Their Skill Level?
*   **Technical Proficiency:** Medium to Expert. Most write Python every day.
*   **Domain Knowledge:** They know robot policy evaluation and success rates. Most treat the statistics as a black box and rely on the tool for the math.

### Inputs and Outputs
*   **Inputs:** The trial table and the study settings.
*   **Outputs:** For each comparison: the decision, a one-line reason, the number of trials used, and the interval for the difference between the two policies. For the whole study: an exit code.
*   **Transformation:** The tool pairs the trials of the two policies, computes an interval for their difference that is valid at any time and adjusted for the number of comparisons, and applies the decision rules.

### Assumptions and Open Questions
*   <mark>Assumption:</mark> A pair is one baseline trial and one policy trial with the same task and the same pair identifier. One baseline trial can be in the pairs of more than one comparison.
*   <mark>Assumption:</mark> "The number of trials" is the number of complete pairs of the comparison. The maximum number of trials is also counted in pairs.
*   <mark>Assumption:</mark> The tool uses the pairs in the order in which they became complete in the trial table. A trial with no partner is not used.
*   <mark>Assumption:</mark> A decision other than "keep going" and "no data" is final. Later trials do not change it, and they are not counted.
*   <mark>Assumption:</mark> The difference is the policy outcome minus the baseline outcome. An interval above 0 means that the new policy is better.
*   <mark>Assumption:</mark> The status command only reads the study. It does not change or add a file.
*   <mark>Assumption:</mark> The tool checks the rules in this order and reports the first that holds: no meaningful difference (the interval is entirely within −<mark>delta</mark> to +delta), the new policy is better (entirely above 0), the baseline is better (entirely below 0), inconclusive, keep going.
*   <mark>Assumption:</mark> To compare policies over all tasks together, the user creates a study with one task and logs every trial under it.
*   <mark>Assumption:</mark> When a policy has more than one trial with the same task and pair identifier, the tool uses the first one and warns about the others. Using a later trial would let an operator repeat a failed trial until it succeeds. A real correction is a Future Version function (Correct a Trial Entry).
*   <mark>Assumption:</mark> The exit code gives the state of the whole study; the machine-readable result gives each comparison. 0: every comparison is settled and none says the baseline is better. 3: at least one comparison says the baseline is better. 4: no comparison says the baseline is better, but at least one is open. 1 and 2 stay for program and usage errors. "No meaningful difference" and "inconclusive" do not fail the check.
*   <mark>Uncertainty:</mark> With the `fdr` <mark>correction method</mark>, what interval does the tool show, and can a decision change when another comparison changes?

## Use Case 4: Import Existing Records

### Who is the User?
*   **Persona/Role:** Integrator
*   **Context:** Someone who already has trial results that another program produced: CSV files and logs from their own evaluation scripts, or public RoboArena records.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Load a results file from their own evaluation script without rewriting the script or rerunning anything.
    *   Load public RoboArena records without converting them by hand.
    *   Treat one policy that appears under different names as one policy.
    *   Learn exactly which rows are invalid, and why.
*   **Operational Workflows:**
    *   *Precondition:* The study exists (Use Case 1) and names the policies and tasks to import.
    *   *Standard Operations:* The user points the import command at a file. The tool converts the records into trials, checks each row, and adds the valid rows to the study in their original order.
    *   *Edge/Exception Operations:* The tool does not import invalid rows; it lists each one with the reason. The checks and warnings are the same as in Use Case 2. A policy name that matches an entry in the alias table is replaced by its standard name.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   Import of CSV files and of RoboArena records, with progress scores as well as pass-or-fail outcomes.
    *   The original order of the trials kept, so the records can be replayed (see Use Case 5).
    *   An alias table for policy names.
*   **Desires / Experience Preferences:** The import runs without a user present, inside an existing pipeline. The user does not have to learn a new data format.

### What is Their Skill Level?
*   **Technical Proficiency:** High to Expert. They build evaluation pipelines or work in Python notebooks.
*   **Domain Knowledge:** They know their own data and pipelines well. Their statistics knowledge ranges from basic to strong.

### Inputs and Outputs
*   **Inputs:** A CSV file or a RoboArena data dump, and the study settings; optionally an alias table for policy names.
*   **Outputs:** New rows in the trial table, a summary of how many rows were imported and how many were rejected, and one message for each rejected row.
*   **Transformation:** The tool maps the source columns to the trial table schema, applies the alias table, checks each row, and appends the valid rows. One RoboArena A/B evaluation becomes two trials that share a pair identifier.

## Use Case 5: Replay Records

### Who is the User?
*   **Persona/Role:** Re-analyst
*   **Context:** Someone who studies or teaches from records that already exist, and runs no new trials. They want to know when a reliable conclusion could have been reached, or they show in class how a conclusion forms.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Replay recorded trials in their original order and see when each comparison reached a decision.
    *   Replay the same trials in many random orders and measure how early a decision arrives and how often it matches the result from all the data.
*   **Operational Workflows:**
    *   *Precondition:* The study holds recorded trials (Use Case 2 or 4).
    *   *Standard Operations:* The user selects a study and chooses the order: the original order, or a number of random orders with a fixed seed. The tool feeds the trials one at a time to the same decision logic as Use Case 3 and reports the stopping points.
    *   *Edge/Exception Operations:* When a comparison never reaches a decision, the tool reports it as undecided together with the number of trials used.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   The same decision rules as live use, so the replay shows what a live user would have seen.
    *   The agreement of each early decision with the full-data result.
    *   Small example data that runs on a student laptop without large downloads.
*   **Desires / Experience Preferences:** A plot that shows the evidence building up trial by trial.

### What is Their Skill Level?
*   **Technical Proficiency:** High to Expert. They work in Python scripts and Jupyter notebooks.
*   **Domain Knowledge:** They have a solid to expert statistics background. Students who watch the replay know Python basics and introductory statistics.

### Inputs and Outputs
*   **Inputs:** A trial table with recorded trials, the study settings, and the order option (original order, or a number of random orders and a seed).
*   **Outputs:** For each comparison: the trial at which a decision was reached, the decision, and whether it matches the full-data decision. For random orders: the distribution of stopping points.
*   **Transformation:** The tool sorts or shuffles the trials, runs the decision logic after each trial, and records the first trial at which each comparison is decided.

## Use Case 6: Generate a Report

### Who is the User?
*   **Persona/Role:** Study owner (produces the report) and Reader (reads it)
*   **Context:** The study owner runs the tool and pastes parts of the report into papers. The reader makes a decision from the results and may never run the tool: a professor who judges whether a result is ready to submit, a product manager who approves a release, or a researcher who reads with a screen magnifier.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   See the conclusion, the trial count and the certainty of every comparison in one view.
    *   See the rules the study used and the method behind each conclusion.
    *   Take tables and plots into a paper, a review or a weekly meeting.
*   **Operational Workflows:**
    *   *Precondition:* The study holds trials (Use Case 2 or 4).
    *   *Standard Operations:* The study owner runs the report command. The tool writes an HTML report and a CSV summary. The reader opens the report in a browser.
    *   *Edge/Exception Operations:* The report shows comparisons that are still undecided; it does not hide them.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   One row per comparison, with results per task and overall.
    *   A one-sentence conclusion in plain words, with the error rate stated.
    *   Charts and tables that do not rely on color alone and stay readable when enlarged.
    *   A machine-readable summary (CSV) for existing dashboards.
*   **Desires / Experience Preferences:** Failure counts by reason for each policy. A results table that goes into a paper without retyping. A description of the method that can be cited.

### What is Their Skill Level?
*   **Technical Proficiency:** Low to Expert. Some readers do not read code and do not install software.
*   **Domain Knowledge:** It varies. A product manager knows the product but no statistics. A professor understands confidence intervals and p-values.

### Inputs and Outputs
*   **Inputs:** The trial table, the study settings, and the decisions from Use Case 3.
*   **Outputs:** An HTML report with a status table and an evidence plot, and a CSV summary.
*   **Transformation:** The tool collects the decision, trial count and interval of each comparison, draws how each interval narrowed over the trials, and writes the report files.

## Future Version

These functions are planned for after the first version. The first version keeps its data formats and interfaces open for them, but does not implement them.

**Use cases**

*   **Correct a Trial Entry.** An operator fixes a wrong entry without editing the data file by hand. The correction is a new row that replaces the original entry, and both stay in the history. It extends Use Case 2. Open design question: a correction can change data that a decision already used.
*   **Analyze Reported Counts.** A re-analyst enters counts from a paper, such as "19/25 vs. 14/20", and gets an interval for each result and a test of the difference. The tool joins the reported results with trial-level results on the policy name. It uses the alias table of Use Case 4.

**Additions to the first-version use cases**

*   Record of every deletion and restart, shown in the report (Use Cases 2 and 6).
*   A button on a dashboard that logs a trial (Use Case 2).
*   Comparison of many policies with each other, not only with the baseline (Use Cases 1 and 3).
*   A comparison over all tasks together, in the same study as the comparisons for each task (Use Cases 1 and 3).
*   An estimate, before the study starts, of how many trials are needed (Use Case 1).
*   Reuse of the baseline trials of an earlier study in a new study (Use Case 1).
*   Replay of the same records under different settings (Use Case 5).
*   A replay animation, and a simulated study with known true success rates (Use Case 5).

## Non-functional Requirements

*   **Installation.** The tool installs from a downloaded package with a standard `pip install`, on a computer with no internet access. It needs few dependencies and supports Linux and macOS.
*   **Getting started.** The tool comes with a quick-start guide, examples that a user can copy, and small example data that runs on a laptop.

## Glossary

The terms that are highlighted in the use cases are defined here.

| Term | Meaning |
| --- | --- |
| Baseline | The policy that every other policy in the study is compared against. |
| Metric | The outcome that the study compares. It is either success (0 or 1) or progress (a score from 0 to 1). |
| Comparison | One policy against the baseline on one task. The tool gives one decision for each comparison. |
| Alpha | The error level that the user accepts. The default is 0.05. Its exact meaning depends on the correction method. |
| Delta | The smallest difference that matters to the user. The default is 0.10. When the whole interval lies within −delta to +delta, the tool reports "no meaningful difference". |
| Correction method | The rule that keeps the error level valid when a study has many comparisons. Strict control (`fwer`) limits the chance of one or more false conclusions in the whole study. The looser setting (`fdr`) limits the share of false conclusions among the conclusions that the tool reports. |
| Decision | The current result of one comparison. It is one of: the new policy is better, the baseline is better, no meaningful difference, inconclusive, keep going, no data. |
| Settled / Open | A comparison is settled when its decision is final (better, no meaningful difference, or inconclusive). It is open when its decision is "keep going" or "no data". |
| Interval | The range that contains the true difference between the policy and the baseline (policy minus baseline), at the error level of the study. It stays valid however often the user checks it. |
| Guarantee | The promise that false conclusions stay within alpha, in the sense that the correction method sets, for all comparisons of the study together, however often the user checks the results. |
| Paired trials (pair) | One baseline trial and one policy trial on the same task with the same pair identifier. A decision uses only complete pairs. |
| Maximum number of trials | The largest number of pairs that one comparison can use. It is the `max_trials` setting. The default is 100. |
| Inconclusive | The decision of a comparison that used the maximum number of trials and reached no other decision. |

## Stories and Use Cases

| Use case | Stories (persona names from `user_stories.md`) |
| --- | --- |
| 1. Create a Study | Alex, Leo, Casey, Morgan |
| 2. Log a Trial | Sam, Diego, Sarah, Chloe, Majilong, Leo, Jordan, Hannah, Lina, Casey, Gina |
| 3. Check Comparison Decisions | Alex, Majilong, Sarah, Chloe, Abhishek, Jin, Leo, Jordan, Marcus, Kenji, Casey, Hannah, Victor |
| 4. Import Existing Records | Jordan, Abhishek, Jin, Marcus, David, Riley, Priya, Avery, Gina |
| 5. Replay Records | David, Priya, Taylor, Dr. Lee, Avery |
| 6. Generate a Report | Morgan, Dr. Elena, Tom, Ivan, Quinn, Alex, Majilong, Leo, David, Kenji |
| Future Version | Sam, Diego, Victor (corrections and deletions); Riley, Priya (reported counts); Quinn (many policies); Avery, Taylor (replay options); Majilong (dashboard) |
| Non-functional Requirements | Ben, Lina, Casey, Taylor, Dr. Lee |
