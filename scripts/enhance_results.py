from pathlib import Path
from datetime import datetime, timezone
import csv, json, subprocess
ROOT=Path(__file__).resolve().parents[1]; docs=ROOT/'docs'; result=docs/'model_results.json'
D=json.loads(result.read_text()); m=D['model']
def read_csv(name):
    p=ROOT/'data'/name
    return list(csv.DictReader(p.open(encoding='utf-8-sig'))) if p.exists() else []
targets=read_csv('analyst_targets.csv'); sources=read_csv('source_documentation.csv')
horizons=[]
for r in targets:
    try: horizons.append(float(r.get('horizon_months','')))
    except ValueError: pass
analyst_years=(horizons[0]/12) if horizons and len(set(horizons))==1 else None
option_years=float(m['maturity_years']); gap=abs(option_years-analyst_years) if analyst_years is not None else None
try: commit=subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=ROOT,text=True).strip()
except Exception: commit='unavailable'
D['enhancements']={
 'horizon': None if analyst_years is None else {'option_years':option_years,'analyst_years':analyst_years,'gap_years':gap,'aligned':gap<=.25},
 'sources':sources,
 'build':{'model_version':'v3.0','generated_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'git_commit':commit}
}
result.write_text(json.dumps(D,indent=2),encoding='utf-8')
print('Enhanced docs/model_results.json with horizon, provenance, and build metadata.')
