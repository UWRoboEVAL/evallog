# Use Cases

Each use case describes one function of the tool. The use cases are extracted from the stories in `user_stories.md` and are listed in the order a user meets them.

## Use Case 1: Create a Study

### Who is the User?
*   **Persona/Role:** Study owner
*   **Context:** The researcher who owns an evaluation. They are about to compare one or more new policies against a baseline on one or more tasks, and they decide what is compared and how strict the conclusion must be. Examples: Alex (PhD student), Leo (ML engineer), Casey (hobbyist). Readers such as Morgan (lab professor) later rely on these rules being fixed in advance.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Name the baseline, the policies and the tasks to compare.
    *   Choose the metric (success or progress) and the error settings.
    *   Save the settings as a file that can be committed and reused.
*   **Operational Workflows:**
    *   *Standard Operations:* The user runs one command or one API call and accepts the defaults. The tool creates a study folder with a settings file and an empty trial table.
    *   *Edge/Exception Operations:* The tool rejects an invalid setting with a message that says what to fix. After the first trial is logged, the tool refuses a change to the settings; the user creates a new study instead.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   Defaults for every statistical setting, so a beginner can start without choosing any.
    *   One guarantee that covers all comparisons in the study together.
    *   Settings that are fixed before the first trial and stored with the results.
*   **Desires / Experience Preferences:** A plain-language explanation of each setting. The same settings file reused across studies, so every sweep is reproducible.

### What is Their Skill Level?
*   **Technical Proficiency:** Medium to High. They use Python, the command line and YAML files.
*   **Domain Knowledge:** They know robot policy evaluation. They know success rates and, at most, confidence intervals and p-values. They do not know sequential tests or multiple-comparison corrections.

### Inputs and Outputs
*   **Inputs:** Study name, baseline, policies, tasks, metric, alpha, delta, maximum trials, correction method.
*   **Outputs:** A study folder that holds the settings file (`study.yaml`) and an empty trial table (`trials.csv`).
*   **Transformation:** The tool fills any missing setting with its default, checks every setting, builds the list of comparisons (each policy against the baseline, on each task), and writes the study folder.

## Use Case 2: Log a Trial

### Who is the User?
*   **Persona/Role:** Operator
*   **Context:** The person or script that runs trials and records each outcome. Examples: Sam and Diego (undergraduate assistants who stand beside a real robot), Sarah, Chloe and Majilong (researchers who run their own trials), Leo and Jordan (engineers whose evaluation scripts log simulated rollouts).

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Record the outcome of one trial right after it finishes.
    *   Mark which trials form a pair, so two policies are compared under the same starting condition.
    *   Add a progress score and a failure reason when they have them.
*   **Operational Workflows:**
    *   *Standard Operations:* A human operator types one short command between scene resets. A script calls the Python API once per rollout. The tool saves the trial and confirms it.
    *   *Edge/Exception Operations:* The tool rejects an entry whose policy or task is not in the study (see Use Case 4). After a crash or power loss, every trial already recorded is still there.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   One entry takes a few seconds and very little typing.
    *   The command line and the Python API record a trial in the same way.
    *   Each trial is saved the moment it is recorded.
    *   Scores between 0 and 1 are accepted, not only pass or fail.
*   **Desires / Experience Preferences:** The failure reason is recorded in the same step as the outcome. A button on a simple dashboard can replace the command.

### What is Their Skill Level?
*   **Technical Proficiency:** Low to High. A human operator may not write Python and follows a written checklist. An engineer calls the API from an existing script.
*   **Domain Knowledge:** They can judge whether a trial succeeded. They may know no statistics.

### Inputs and Outputs
*   **Inputs:** Policy, task, outcome (success 0/1, or progress from 0 to 1), pair identifier; optionally a failure reason.
*   **Outputs:** One new row in the trial table, and a confirmation message.
*   **Transformation:** The tool checks the entry against the study settings, adds a trial identifier and a timestamp, and appends the row to the trial table.

## Use Case 3: Correct a Trial Entry

### Who is the User?
*   **Persona/Role:** Operator
*   **Context:** The person who recorded a trial and then notices a mistake in it. Examples: Sam and Diego, who sometimes type the wrong outcome during a long session. The study owner and the readers need the history to stay complete. Victor is a user to design against: he might delete a bad session to make his policy look good.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Fix a wrong outcome or a wrong name in an entry that is already recorded.
    *   Do this without asking the study owner, and continue the session.
*   **Operational Workflows:**
    *   *Standard Operations:* The operator runs a correction command that names the trial and gives the right value. The tool records the correction as a new row. The original entry stays visible.
    *   *Edge/Exception Operations:* The tool rejects a correction that names a trial that does not exist. A deletion or a restart made through the tool is recorded, so a trial cannot disappear silently.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   A correction that does not require editing the data file by hand.
    *   Both the original entry and the correction kept in the history.
    *   Later analysis that uses the corrected value.
    *   A record of every deletion and restart.
*   **Desires / Experience Preferences:** A short way to say "the last entry", because most mistakes are noticed right away.

### What is Their Skill Level?
*   **Technical Proficiency:** Low. They can type a short command but do not write Python.
*   **Domain Knowledge:** They can judge the outcome of a trial. They know no statistics.

### Inputs and Outputs
*   **Inputs:** The trial to correct (an identifier, or "the last entry"), the field to change, and the corrected value.
*   **Outputs:** One new correction row in the trial table, and a confirmation that shows the old value and the new value.
*   **Transformation:** The tool finds the original trial and appends a row that replaces it. Analysis uses the latest version of each trial.

## Use Case 4: Validate Trial Data

This is an implied use case. No user asks for it directly, but every logged trial and every imported file passes through it.

### Who is the User?
*   **Persona/Role:** Operator
*   **Context:** Anyone who puts data into a study, by hand or from a file. Examples: Sam and Lina (a mistyped policy name), Casey (a beginner who does not know how to set up valid trials), Priya (an imported file with bad rows). Gina is a user to design against: she might count easy tasks for her policy and hard tasks for the rival, or log trials for only one of the two policies.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Find out at once that an entry or a file is wrong.
    *   Learn what to fix.
*   **Operational Workflows:**
    *   *Standard Operations:* The check runs automatically whenever a trial is logged or a file is imported. Valid data passes without any message.
    *   *Edge/Exception Operations:* The tool rejects an unknown policy or task name and a score outside the allowed range. For an imported file, the tool lists exactly which rows are invalid. The tool warns when trials are unpaired, or when the two policies were not tested under matching conditions.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   Names checked against the policies and tasks in the study settings.
    *   Required fields and value ranges checked for every row.
    *   A warning for unpaired trials and for conditions that do not match between policies.
*   **Desires / Experience Preferences:** Error messages in plain words that say what went wrong and what to fix. Guidance on how to set up valid trials, such as the same starting positions for both policies.

### What is Their Skill Level?
*   **Technical Proficiency:** Low to High.
*   **Domain Knowledge:** They may be new to the tool and may know no statistics.

### Inputs and Outputs
*   **Inputs:** One trial entry or one imported table, and the study settings.
*   **Outputs:** The data is accepted, or the tool returns one message for each problem (rejection or warning).
*   **Transformation:** The tool compares each row with the trial table schema and with the study settings, then checks pairing across policies.

## Use Case 5: Check Comparison Decisions

### Who is the User?
*   **Persona/Role:** Study owner
*   **Context:** The person or pipeline that must know whether a comparison is settled. Examples: Alex, Majilong, Sarah and Chloe (they decide during a robot session whether to run more trials), Leo, Jordan and Marcus (their scripts and CI pipelines act on the result), Kenji (he decides each week whether a new checkpoint ships), Casey (a beginner who does not know how many trials are enough).

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   See the current decision for each comparison: the new policy is better, the baseline is better, there is no meaningful difference, or keep going.
    *   Stop collecting trials for comparisons that are settled, and spend the remaining time on the open ones.
    *   Use the decision in an automated pipeline, for example to block a pull request.
*   **Operational Workflows:**
    *   *Standard Operations:* After any trial, the user asks for the status. The tool shows one line per comparison with the decision, the number of trials and the interval. A script gets the same result from the Python API or from the exit code.
    *   *Edge/Exception Operations:* The user may check after every trial; this does not weaken the guarantee. When a comparison reaches the maximum number of trials without a decision, the tool reports it as inconclusive. When a comparison has no paired trials yet, the tool reports that it has no data.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   A decision for every comparison after every trial.
    *   A stated error rate that stays valid however often the results are checked.
    *   One guarantee that covers all comparisons together, with a choice between strict control and a looser setting for exploration.
    *   Support for both pass-or-fail outcomes and scores between 0 and 1.
    *   A machine-readable result for scripts and CI.
*   **Desires / Experience Preferences:** A highly visible "STOP" signal that can be read while handling hardware. The conclusion in plain words with a one-line reason.

### What is Their Skill Level?
*   **Technical Proficiency:** Medium to Expert. Most write Python every day.
*   **Domain Knowledge:** They know robot policy evaluation and success rates. Most treat the statistics as a black box and rely on the tool for the math.

### Inputs and Outputs
*   **Inputs:** The trial table and the study settings.
*   **Outputs:** For each comparison: the decision, the number of trials used, and the interval for the difference between the two policies.
*   **Transformation:** The tool pairs the trials of the two policies, computes an interval for their difference that is valid at any time and adjusted for the number of comparisons, and applies the decision rules.

## Use Case 6: Import Existing Records

### Who is the User?
*   **Persona/Role:** Integrator
*   **Context:** Someone who already has trial results that another program produced. Examples: Jordan, Abhishek, Jin and Marcus (CSV files and logs from their own evaluation scripts), David, Riley, Priya and Avery (public RoboArena records).

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Load a results file from their own evaluation script without rewriting the script or rerunning anything.
    *   Load public RoboArena records without converting them by hand.
    *   Treat one policy that appears under different names as one policy.
*   **Operational Workflows:**
    *   *Standard Operations:* The user points the import command at a file. The tool converts the records into trials and adds them to the study in their original order.
    *   *Edge/Exception Operations:* The tool does not import invalid rows and lists them (see Use Case 4). A policy name that matches an entry in the alias table is replaced by its standard name.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   Import of CSV files and of RoboArena records.
    *   The original order of the trials kept, so the records can be replayed (see Use Case 7).
    *   An alias table for policy names.
    *   Progress scores imported as well as pass-or-fail outcomes.
*   **Desires / Experience Preferences:** The import runs without a user present, inside an existing pipeline. The user does not have to learn a new data format.

### What is Their Skill Level?
*   **Technical Proficiency:** High to Expert. They build evaluation pipelines or work in Python notebooks.
*   **Domain Knowledge:** They know their own data and pipelines well. Their statistics knowledge ranges from basic to strong.

### Inputs and Outputs
*   **Inputs:** A CSV file or a RoboArena data dump; optionally an alias table for policy names.
*   **Outputs:** New rows in the trial table, and a summary of how many rows were imported and how many were rejected.
*   **Transformation:** The tool maps the source columns to the trial table schema, applies the alias table, validates each row, and appends the valid rows. One RoboArena A/B evaluation becomes two trials that share a pair identifier.

## Use Case 7: Replay Records

### Who is the User?
*   **Persona/Role:** Re-analyst
*   **Context:** Someone who studies or teaches from records that already exist, and runs no new trials. Examples: David and Priya (they want to know when a reliable conclusion could have been reached), Taylor and Dr. Lee (they show in class how a conclusion forms), Avery (a methods researcher who compares stopping rules).

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Replay recorded trials in their original order and see when each comparison reached a decision.
    *   Replay the same trials in many random orders and measure how early a decision arrives and how often it matches the result from all the data.
    *   Show the replay to a class, trial by trial.
*   **Operational Workflows:**
    *   *Standard Operations:* The user selects a study that holds recorded trials and chooses the order: the original order, or a number of random orders with a fixed seed. The tool feeds the trials one at a time to the same decision logic as Use Case 5 and reports the stopping points.
    *   *Edge/Exception Operations:* When a comparison never reaches a decision, the tool reports it as undecided together with the number of trials used.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   The same decision rules as live use, so the replay shows what a live user would have seen.
    *   Replay in the original order and in random orders.
    *   The stopping point of each comparison, and its agreement with the full-data result.
    *   Small example data that runs on a student laptop without large downloads.
*   **Desires / Experience Preferences:** A plot or animation that shows the evidence building up trial by trial. A simulated study with known true success rates, so the tool can be checked against the right answer.

### What is Their Skill Level?
*   **Technical Proficiency:** High to Expert. They work in Python scripts and Jupyter notebooks.
*   **Domain Knowledge:** They have a solid to expert statistics background. Students who watch the replay know Python basics and introductory statistics.

### Inputs and Outputs
*   **Inputs:** A trial table with recorded trials, the study settings, and the order option (original order, or a number of random orders and a seed).
*   **Outputs:** For each comparison: the trial at which a decision was reached, the decision, and whether it matches the full-data decision. For random orders: the distribution of stopping points.
*   **Transformation:** The tool sorts or shuffles the trials, runs the decision logic after each trial, and records the first trial at which each comparison is decided.

## Use Case 8: Analyze Reported Counts

### Who is the User?
*   **Persona/Role:** Re-analyst
*   **Context:** Someone who reads published results and has only the numbers in the paper, not the raw trials. Examples: Riley (writes a survey of about ten papers), Priya (reviews conference submissions).

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   Enter counts such as "19/25 vs. 14/20" and get an interval for each result and a test of the difference.
    *   Put a paper's numbers next to trial-level results for the same policy and see whether they agree.
*   **Operational Workflows:**
    *   *Standard Operations:* The user enters one pair of counts, or a table of counts. The tool returns an interval for each result and a verdict for each claim: supported, not supported, or not enough data to tell.
    *   *Edge/Exception Operations:* When a paper does not report the number of trials, no interval can be computed. The tool excludes that row and lists it with the reason.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   Intervals and a test that work from counts alone.
    *   A clear verdict for each claim.
    *   A join between reported results and trial-level results on the policy name, using the alias table.
*   **Desires / Experience Preferences:** A whole survey table entered at once, not one comparison at a time. A table and a plot ready for a review or a related-work section.

### What is Their Skill Level?
*   **Technical Proficiency:** Medium to High. They work in Python notebooks.
*   **Domain Knowledge:** They know standard statistics well, including hypothesis tests and why small samples mislead.

### Inputs and Outputs
*   **Inputs:** Successes and number of trials for each reported result (one pair, or a table); optionally a study with trial-level results to compare against.
*   **Outputs:** An interval for each result, a test result and a verdict for each claim, and a list of excluded rows.
*   **Transformation:** The tool computes a fixed-sample interval for each count and an exact test for each difference. These results are not paired, so the tool does not use the sequential method of Use Case 5.

## Use Case 9: Generate a Report

### Who is the User?
*   **Persona/Role:** Reader
*   **Context:** Someone who makes a decision from the results and may never run the tool. Examples: Morgan and Dr. Elena (professors who judge whether a student's result is ready to submit), Tom (a product manager who approves a release), Ivan (a color-blind researcher who reads with a screen magnifier), Quinn (publishes results on a leaderboard). Study owners such as Alex, Majilong, Leo and David produce the report and paste parts of it into papers.

### What Do They Want to Do with the Tool?
*   **Primary Tasks:**
    *   See the conclusion, the trial count and the certainty of every comparison in one view.
    *   See the rules the study used and the method behind each conclusion.
    *   Take tables and plots into a paper, a review or a weekly meeting.
*   **Operational Workflows:**
    *   *Standard Operations:* The study owner runs the report command. The tool writes an HTML report and a CSV summary. The reader opens the report in a browser.
    *   *Edge/Exception Operations:* The report shows comparisons that are still undecided; it does not hide them. The report lists corrections and deletions, so a result that was tuned afterward stands out.

### What Needs and Desires Do They Have for the Tool?
*   **Functional Needs:**
    *   One row per comparison, with results per task and overall.
    *   A one-sentence conclusion in plain words, with the error rate stated.
    *   The study settings and the method shown in the report.
    *   Charts and tables that do not rely on color alone and stay readable when enlarged.
    *   A machine-readable summary (CSV) for existing dashboards.
*   **Desires / Experience Preferences:** Failure counts by reason for each policy. A results table that goes into a paper without retyping. A description of the method that can be cited.

### What is Their Skill Level?
*   **Technical Proficiency:** Low to Expert. Some readers do not read code and do not install software.
*   **Domain Knowledge:** It varies. A product manager knows the product but no statistics. A professor understands confidence intervals and p-values.

### Inputs and Outputs
*   **Inputs:** The trial table, the study settings, and the decisions from Use Case 5.
*   **Outputs:** An HTML report with a status table and an evidence plot, and a CSV summary.
*   **Transformation:** The tool collects the decision, trial count and interval of each comparison, draws how each interval narrowed over the trials, and writes the report files.

## Supporting Use Cases

These two are also implied. They have no data inputs or outputs, so they are described briefly.

*   **Install the tool.** Ben is a systems administrator for a lab whose robot computers have no internet access. He installs the tool from a downloaded package with a standard `pip install`. The tool needs few dependencies and supports Linux and macOS.
*   **Get started with examples.** Lina, Casey, Taylor and Dr. Lee start from a quick-start guide, examples they can copy, and small example data that runs on a laptop.
