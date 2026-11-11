# 🎓 Scholarship Advisory Rule-Based System

A Python-based scholarship advisory application developed using **Streamlit** for BSD3513 Artificial Intelligence – Lab Report 3.

The system applies predefined IF–THEN rules to evaluate scholarship applicants based on academic performance, financial background, co-curricular involvement, and disciplinary records. It generates transparent scholarship recommendations using a priority-based rule evaluation mechanism.

## Features

- **Applicant Assessment:** Collects CGPA, monthly family income, co-curricular score, community service hours, current semester, and disciplinary actions.
- **JSON Rule Editor:** Allows users to view and modify scholarship eligibility rules without changing the Python source code.
- **Rule-Based Inference Engine:** Evaluates applicant information against predefined conditions using logical AND operations.
- **Priority-Based Conflict Resolution:** Selects the highest-priority rule when multiple rules match.
- **Explainable Recommendations:** Displays the final decision, matched rule, priority, and corresponding reason.
- **Rule Evaluation Audit Trail:** Shows which rules and conditions were satisfied or not satisfied.
- **Downloadable Results:** Allows users to export the decision audit in JSON format.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development and rule evaluation |
| Streamlit | Interactive web application |
| JSON | Knowledge representation and rule configuration |
| VS Code | Development environment |
| GitHub | Source code hosting and version control |

## System Architecture

The system consists of three main components:

1. **Knowledge Base:** Stores five predefined scholarship rules in JSON format, including their conditions, priorities, and corresponding decisions.
2. **Inference Engine:** Evaluates applicant attributes against all rules. A rule matches only when all its conditions are satisfied. If multiple rules match, the highest-priority rule is selected.
3. **Streamlit User Interface:** Provides applicant input fields, an editable JSON rule configuration, scholarship recommendations, and an evaluation audit trail.

### Decision-Making Workflow

1. The user enters applicant information.
2. The system loads and validates the JSON rules.
3. The inference engine evaluates all predefined conditions.
4. Matching rules are identified and ranked according to priority.
5. The highest-priority matching rule determines the recommendation.
6. The system displays the decision, explanation, and audit trail.
7. If no rules match, the system returns `NO_MATCH`.

## Scholarship Rules

The application contains five predefined rules provided in the laboratory instructions.

| Rule | Priority | Decision |
|---|---:|---|
| Top merit candidate | 100 | AWARD_FULL |
| Low CGPA – not eligible | 95 | REJECT |
| Serious disciplinary record | 90 | REJECT |
| Good candidate – partial scholarship | 80 | AWARD_PARTIAL |
| Need-based review | 70 | REVIEW |

The default rules are preserved as specified in the assignment. Users may modify the JSON configuration to evaluate alternative scholarship policies.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/hasnurhisham/YOUR-REPOSITORY.git](https://github.com/hasnurhisham/scholarship.git
cd YOUR-REPOSITORY
```

Replace the example URL with your actual GitHub repository URL.

### 2. Install dependencies

Ensure Python 3 is installed, then run:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Run the application

```bash
python3 -m streamlit run app.py
```

The application will typically be accessible at:

`http://localhost:8501`

## How to Use

1. Open the Streamlit application.
2. Review the five default scholarship rules in the JSON editor.
3. Enter the applicant's information in the input form.
4. Click **Evaluate scholarship**.
5. View the generated recommendation, matched rule, priority, and explanation.
6. Expand the rule evaluation audit trail to inspect individual conditions.
7. Optionally, download the decision audit as a JSON file.

## Testing and Expected Results

The following test scenarios cover the five possible recommendation outcomes.

| Test Case | Expected Decision |
|---|---|
| Excellent academic and co-curricular performance | AWARD_FULL |
| Good academic and co-curricular performance | AWARD_PARTIAL |
| Financial need with borderline academic performance | REVIEW |
| Insufficient CGPA | REJECT |
| No matching eligibility conditions | NO_MATCH |

The application also supports validation of modified JSON rules and displays an error when the rule configuration is invalid.

## Application Screenshots

Include screenshots of:

- Applicant input form and JSON rule editor.
- Scholarship recommendation and explanation.
- Rule evaluation audit trail.
- Additional test case outputs.

Screenshots should demonstrate the application interface and its rule-based decision-making process.

## Deployment

**Live Streamlit Application:**  https://lab-report1-dfs-bfs.streamlit.app 

**GitHub Repository:** https://github.com/hasnurhisham/scholarship.git

## Limitations

The system relies on predefined scholarship eligibility rules and cannot independently evaluate exceptional applicant circumstances. Community service hours and current semester are collected but do not influence recommendations under the five default rules.

Therefore, the system is intended as a decision-support tool, and final scholarship decisions should remain subject to committee approval.
