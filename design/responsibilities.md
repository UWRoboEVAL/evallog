# System Responsibilities

Add the responsibilities from your use cases here. Then we group them into components together.

Start your IDs with a short prefix, such as IMP for import.

| ID | Responsibility | Use case | Owner |
|---|---|---|---|
| IMP-1 | Read a CSV file, with optional column renames | #11 | Suhang |
| IMP-2 | Read RoboArena sessions as trials, one per policy, paired by session | #11 | Suhang |
| IMP-3 | Replace policy aliases with standard names | #11, Paper counts | Suhang |
| IMP-4 | Check each row against the trial rules | #9, #11 | Hao (`schema.py`) |
| IMP-5 | Skip policies that are not in the study, and count them | #11 | Suhang |
| IMP-6 | Add all valid rows at once, in file order | #11 | Suhang |
| IMP-7 | Save invalid rows and their reasons to a separate file | #11 | Suhang |
| IMP-8 | Refuse a file that was already imported | #11 | Suhang |
| IMP-9 | Print the counts (imported, rejected, skipped, warned) and an exit code | #11 | Suhang |
| IMP-10 | Read a file of paper results | Paper counts | Suhang |
| IMP-11 | Check paper counts: trials above 0, successes between 0 and trials | Paper counts | Suhang |
| IMP-12 | Join paper results with our trials by policy name | Paper counts | Suhang |
