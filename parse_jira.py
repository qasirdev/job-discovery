import csv
import sys
import glob

file_order = [
    "docs/jira-tickets/jd-mvp3.0.csv",
    "docs/jira-tickets/jd-mvp3.1.csv",
    "docs/jira-tickets/jd-mvp3.2.csv",
    "docs/jira-tickets/jd-mvp-cross.csv",
    "docs/jira-tickets/jd-mvp-post3.csv",
    "docs/jira-tickets/jd-mvp4.csv",
    "docs/jira-tickets/jd-mvp5.csv"
]

print("## Implementation Priority List\n")

for filepath in file_order:
    print(f"### Source: `{filepath.split('/')[-1]}`\n")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            epics = {}
            tasks_by_epic = {}
            standalone_tasks = []
            
            for row in reader:
                issue_id = (row.get('Issue id') or '').strip()
                summary = (row.get('Summary') or '').strip()
                issue_type = (row.get('Issue Type') or '').strip()
                parent = (row.get('Parent') or '').strip()
                
                if issue_type == 'Epic':
                    epics[issue_id] = summary
                    tasks_by_epic[issue_id] = []
                elif issue_type == 'Task':
                    if parent and parent in tasks_by_epic:
                        tasks_by_epic[parent].append((issue_id, summary))
                    elif parent:
                        if parent not in tasks_by_epic:
                            tasks_by_epic[parent] = []
                        tasks_by_epic[parent].append((issue_id, summary))
                    else:
                        standalone_tasks.append((issue_id, summary))
            
            for epic_id, epic_summary in epics.items():
                print(f"- **{epic_id}**: {epic_summary} (Epic)")
                for task_id, task_summary in tasks_by_epic.get(epic_id, []):
                    print(f"  - [{task_id}] {task_summary}")
            
            for parent_id, tasks in tasks_by_epic.items():
                if parent_id not in epics and tasks:
                    print(f"- **Under Epic {parent_id}** (Defined elsewhere)")
                    for task_id, task_summary in tasks:
                        print(f"  - [{task_id}] {task_summary}")
                        
            if standalone_tasks:
                print("- **Standalone Tasks**")
                for task_id, task_summary in standalone_tasks:
                    print(f"  - [{task_id}] {task_summary}")
                    
            print()
    except Exception as e:
        print(f"Error reading {filepath}: {e}\n")

