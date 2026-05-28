import csv
import glob
import os

csv_files = glob.glob('/Users/qasirmehmood/Projects/qasir-proflle-2026/job-discovery/docs/jira-tickets/*.csv')

epics = {}
tasks_by_epic = {}

for f in csv_files:
    with open(f, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row:
                continue
            issue_id = (row.get('Issue id') or '').strip()
            if not issue_id:
                continue
            issue_type = (row.get('Issue Type') or '').strip()
            if issue_type == 'Epic':
                epics[issue_id] = row
            else:
                parent = (row.get('Parent') or '').strip()
                if parent not in tasks_by_epic:
                    tasks_by_epic[parent] = []
                tasks_by_epic[parent].append(row)

# Update PLAN.md
plan_path = '/Users/qasirmehmood/Projects/qasir-proflle-2026/job-discovery/docs/PLAN.md'
with open(plan_path, 'w', encoding='utf-8') as f:
    f.write("# Project Plan\n\nThis document is auto-generated from `docs/jira-tickets/*.csv`.\n\n## Epics\n\n")
    for epic_id in sorted(epics.keys()):
        f.write(f"- **{epic_id}**: {epics[epic_id].get('Summary', '')} (Epic)\n")

# Update EPICS-AND-STORIES.md
stories_path = '/Users/qasirmehmood/Projects/qasir-proflle-2026/job-discovery/EPICS-AND-STORIES.md'
with open(stories_path, 'w', encoding='utf-8') as f:
    f.write("# Epics and Stories\n\nThis document is auto-generated from `docs/jira-tickets/*.csv`.\n\n")
    for epic_id in sorted(epics.keys()):
        epic = epics[epic_id]
        f.write(f"## {epic_id}: {epic.get('Summary', '')}\n\n")
        desc = (epic.get('Description') or '').replace('\n', '\n')
        f.write(f"**Description:** {desc}\n\n")
        f.write(f"**Labels:** {epic.get('Labels', '')}\n\n")
        f.write("### Stories / Tasks\n\n")
        tasks = tasks_by_epic.get(epic_id, [])
        for task in sorted(tasks, key=lambda x: x.get('Issue id', '')):
            desc = (task.get('Description') or '').replace('\n', ' ')
            f.write(f"- **{task.get('Issue id', '')}**: {task.get('Summary', '')}\n")
            f.write(f"  - *Description*: {desc}\n")
        f.write("\n---\n\n")

print("Docs updated successfully.")
