
PROMPT:

- proposal-v4-structure.md, confirm understanding, do nothing

- for yolo mode, how many steps are there for mvp1, only provide list with one line description

- go yolo mode and complete mvp1 without my input/permission
only keep displaying current action logs and next steps

- befor going to MVP 1.1 prompt engineering, please make sure MVP 1 is completed and tested according to relevent epics and tasks criterias.

if ruquired run backend / frontend servers and after testing stop it
perform lint and mypy test and fix

user yolo mode, no need my permissions

=====
PROMPT:

 [jd-mvp4.csv]
list down all epics alongside tasks with title. only list nothing else

=====
PROMPT:

if epic number
task 1
task 2
task 3


if any thing not configured according to new design  [proposal-v4-structure.md] then implement/update accordingly one by one in YOLO Mode Exceptions & Rules and [AGENT.md] (job-discovery/AGENT.md) rules

=====
PROMPT:
Step 1: 
on the basis of updated file [proposal-v4-structure.md]
do i need to re implement or update again any epic of following alongside with edge cases:

[jd-mvp-cross.csv]

if required update csv according to [AGENT.md] rules 
- also update [PLAN.md] ,  [EPICS-AND-STORIES.md]

Step 2: 
[jd-mvp-cross.csv]
now change code according to YOLO Mode Exceptions & Rules and 
[AGENT.md]  for updated above tickts implement/update one by one implementation periorities wise,according to updated [proposal-v4-structure.md]

Step 3:
[AGENT.md]

create one prompt for above changes so that other llm can re confirm implementation is correct and working as expected:
only provide me prompt in copy/paste format in markdown

Step 4: 
[PROMPT] run in other LLM to check implementation is correct and working as expected:


=====
PROMPT:

Audit the entire codebase in YOLO mode using docs/jira-tickets, AGENT.md, and docs/proposal-v4-structure.md.

Step 1: List all epics and their associated ticket titles, ordered by implementation priority. Step 2: Iterate through each epic one by one. For each epic, thoroughly audit the current codebase to verify proper functionality and alignment with the rules in AGENT.md and the architecture in docs/proposal-v4-structure.md. Immediately implement or update any missing or incomplete tasks required for that epic.

=====
PROMPT:


=====
PROMPT:


=====
PROMPT:

