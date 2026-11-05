# User Stories Design

Who is the user. 
What do they want to do with the tool. 
What needs and desires do they want for the tool. 
What is their skill level.


### Abhishek

1. Abhishek compares a new robot control model against a baseline in simulation. He wants a tool to read his automated logs and act as a strict referee against lucky streaks. He needs a lightweight checker to prevent false success claims without the overhead of heavy study-planning frameworks. Abhishek is an expert in Python but relies on established statistical methods.

2. Sarah tests a new manipulation policy on a physical robot. She wants a CLI tool to log each try and tell her exactly when to stop, minimizing manual scene resets. She needs a lightweight referee that translates raw stats into simple "stop" or "keep going" signals. Sarah knows Python but isn't a statistician.

3. David evaluates robot programs using public RoboArena datasets. He wants to automatically feed bulk trial records into a script to find exactly when a policy proved superior. He needs a tool that handles data imports and generates clean, publish-ready tables with error bars. David is highly proficient in Python scripting.