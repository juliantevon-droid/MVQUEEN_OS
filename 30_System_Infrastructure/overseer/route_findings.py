#!/usr/bin/env python3
"""Route enterprise crawler findings to MVQUEEN production specialists.

Read-only with respect to production systems. Generates an assignment manifest
for Overseer/QA/Release and never publishes to Shopify.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

ROUTES={
 "syntax":"qa","duplication":"data","config_drift":"shopify",
 "unfinished_work":"qa","brand_drift":"editorial","security":"security",
 "publishing_boundary":"release","catalog":"catalog","seo":"seo",
 "conversion":"conversion","accessibility":"accessibility",
 "performance":"performance","theme":"theme","mobile_ux":"mobile_ux",
 "merchandising":"merchandising","metafields":"data",
}
REVIEWERS={
 "security":["qa","release"],"release":["qa","security"],"shopify":["qa","release"],
 "theme":["qa","mobile_ux","accessibility"],"conversion":["qa","mobile_ux"],
 "editorial":["qa","seo"],"seo":["qa","editorial"],"catalog":["qa","data"],
 "data":["qa","catalog"],"merchandising":["qa","conversion"],
 "performance":["qa","mobile_ux"],"accessibility":["qa","mobile_ux"],
 "mobile_ux":["qa","conversion"],"qa":["release"],
}
BLOCKING={"BLOCKER","CRITICAL","HIGH"}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--input",default="build/enterprise_crawler/report.json")
 p.add_argument("--output",default="build/agents/assignments.json")
 a=p.parse_args()
 src=json.loads(Path(a.input).read_text())
 assignments=[]
 for i,f in enumerate(src.get("findings",[]),1):
  owner=ROUTES.get(f.get("category"),"qa")
  assignments.append({
   "finding_id":f"MVQ-FINDING-{i:05d}","owner":owner,
   "reviewers":REVIEWERS.get(owner,["qa"]),
   "severity":f.get("severity"),"category":f.get("category"),
   "path":f.get("path"),"message":f.get("message"),
   "confidence":f.get("confidence","review"),
   "conversion_impact":f.get("conversion_impact","none"),
   "state":"triage","production_blocking":f.get("severity") in BLOCKING,
   "required_flow":["specialist_analysis","recommendation","qa_verification","release_disposition","outcome_record"]
  })
 counts=Counter(x["owner"] for x in assignments)
 out={"schema_version":"1.0","source":a.input,"assignments":assignments,
      "owner_counts":dict(counts),
      "governance":"No assignment grants write authority; protected actions remain gated."}
 path=Path(a.output); path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({"assignments":len(assignments),"owner_counts":dict(counts)},indent=2))
if __name__=="__main__": main()
