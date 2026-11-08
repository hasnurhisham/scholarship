import json
import operator
import streamlit as st

DEFAULT_RULES = [
 {"name":"Top merit candidate","priority":100,"conditions":[["cgpa",">=",3.7],["co_curricular_score",">=",80],["family_income","<=",8000],["disciplinary_actions","==",0]],"action":{"decision":"AWARD_FULL","reason":"Excellent academic & co-curricular performance, with acceptable need"}},
 {"name":"Good candidate - partial scholarship","priority":80,"conditions":[["cgpa",">=",3.3],["co_curricular_score",">=",60],["family_income","<=",12000],["disciplinary_actions","<=",1]],"action":{"decision":"AWARD_PARTIAL","reason":"Good academic & involvement record with moderate need"}},
 {"name":"Need-based review","priority":70,"conditions":[["cgpa",">=",2.5],["family_income","<=",4000]],"action":{"decision":"REVIEW","reason":"High need but borderline academic score"}},
 {"name":"Low CGPA – not eligible","priority":95,"conditions":[["cgpa","<",2.5]],"action":{"decision":"REJECT","reason":"CGPA below minimum scholarship requirement"}},
 {"name":"Serious disciplinary record","priority":90,"conditions":[["disciplinary_actions",">=",2]],"action":{"decision":"REJECT","reason":"Too many disciplinary records"}}
]
OPS = {">=":operator.ge,"<=":operator.le,">":operator.gt,"<":operator.lt,"==":operator.eq,"!=":operator.ne}
FIELDS = {"cgpa","family_income","co_curricular_score","community_service_hours","semester","disciplinary_actions"}

def validate_rules(rules):
    if not isinstance(rules,list) or not rules:
        raise ValueError('Rules must be a non-empty JSON array.')
    names=set()
    for i,rule in enumerate(rules,1):
        if not isinstance(rule,dict) or not isinstance(rule.get('name'),str) or not rule['name'].strip():
            raise ValueError(f'Rule {i}: invalid name.')
        if rule['name'] in names:
            raise ValueError(f'Duplicate rule name: {rule["name"]}')
        names.add(rule['name'])
        if type(rule.get('priority')) not in (int,float):
            raise ValueError(f'Rule {i}: priority must be numeric.')
        conditions=rule.get('conditions')
        if not isinstance(conditions,list) or not conditions:
            raise ValueError(f'Rule {i}: conditions must be a non-empty list.')
        for cond in conditions:
            if not isinstance(cond,list) or len(cond)!=3 or cond[0] not in FIELDS or cond[1] not in OPS or type(cond[2]) not in (int,float):
                raise ValueError(f'Rule {i}: invalid condition {cond!r}.')
        action=rule.get('action')
        if not isinstance(action,dict) or not isinstance(action.get('decision'),str) or not isinstance(action.get('reason'),str):
            raise ValueError(f'Rule {i}: action needs decision and reason strings.')
    return rules

def evaluate(applicant,rules):
    matches=[]
    trace=[]
    for index,rule in enumerate(rules):
        checks=[]
        for field,op,threshold in rule['conditions']:
            actual=applicant[field]
            passed=OPS[op](actual,threshold)
            checks.append({'condition':f'{field} ({actual}) {op} {threshold}','passed':passed})
        matched=all(item['passed'] for item in checks)
        trace.append({'rule':rule['name'],'priority':rule['priority'],'matched':matched,'checks':checks})
        if matched:
            matches.append((index,rule))
    matches.sort(key=lambda pair:(-pair[1]['priority'],pair[0]))
    return (matches[0][1] if matches else None),trace

st.set_page_config(page_title='Scholarship Rule Engine',page_icon='🎓',layout='wide')
st.title('🎓 Scholarship Advisory Rule-Based System')
st.caption('Transparent, configurable IF–THEN decision support • Recommendations require committee approval')
with st.sidebar:
    st.header('Rule configuration')
    st.caption('Edit the JSON to test alternative policies. The default is the exact five-rule assignment configuration.')
    raw=st.text_area('JSON rule editor',value=json.dumps(DEFAULT_RULES,ensure_ascii=False,indent=2),height=450)
    try:
        rules=validate_rules(json.loads(raw))
        st.success(f'{len(rules)} valid rules loaded')
    except (json.JSONDecodeError,ValueError) as exc:
        rules=None
        st.error(str(exc))
    st.download_button('Download default JSON',json.dumps(DEFAULT_RULES,ensure_ascii=False,indent=2),file_name='rules.json',mime='application/json')

st.subheader('Applicant profile')
with st.form('applicant'):
    c1,c2,c3=st.columns(3)
    cgpa=c1.number_input('CGPA',0.0,4.0,3.75,0.01)
    income=c2.number_input('Monthly family income (RM)',0,1000000,5000,100)
    cocurricular=c3.number_input('Co-curricular score (0–100)',0,100,85)
    hours=c1.number_input('Community service hours',0,100000,20)
    semester=c2.number_input('Current semester',1,30,4)
    discipline=c3.number_input('Disciplinary actions',0,100,0)
    submitted=st.form_submit_button('Evaluate scholarship',type='primary',use_container_width=True)

if submitted:
    if rules is None:
        st.error("Please fix the JSON configuration before evaluation.")
    else:
        applicant = {
            "cgpa": cgpa,
            "family_income": income,
            "co_curricular_score": cocurricular,
            "community_service_hours": hours,
            "semester": semester,
            "disciplinary_actions": discipline
        }

        winner, trace = evaluate(applicant, rules)

        st.divider()
        st.subheader("Decision and explanation")

        if winner is not None:
            decision = winner["action"]["decision"]
            reason = winner["action"]["reason"]

            if decision == "REJECT":
                st.error(f"Recommendation: {decision}")
            elif decision == "REVIEW":
                st.warning(f"Recommendation: {decision}")
            else:
                st.success(f"Recommendation: {decision}")

            st.write(f"**Matched rule:** {winner['name']}")
            st.write(f"**Priority:** {winner['priority']}")
            st.write(f"**Reason:** {reason}")

        else:
            st.warning(
                "NO_MATCH — No supplied rule applies. "
                "Refer to the scholarship committee for manual assessment."
            )

        st.write("**Rule evaluation audit trail**")

        for item in sorted(trace, key=lambda x: -x["priority"]):
            with st.expander(
                f"{'✅' if item['matched'] else '❌'} "
                f"{item['rule']} | Priority {item['priority']}"
            ):
                for check in item["checks"]:
                    symbol = "✓" if check["passed"] else "✗"
                    st.write(f"{symbol} {check['condition']}")

        st.info(
            "Community service hours and semester are recorded "
            "but do not affect decisions under the supplied five rules."
        )

        st.download_button(
            "Download decision audit (JSON)",
            json.dumps({
                "applicant": applicant,
                "decision": winner["action"] if winner else {
                    "decision": "NO_MATCH",
                    "reason": "No rule matched"
                },
                "trace": trace
            }, indent=2),
            file_name="scholarship_audit.json",
            mime="application/json"
        )
