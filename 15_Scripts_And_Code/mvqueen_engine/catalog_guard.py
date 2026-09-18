"""MVQUEEN catalog pre-write safety guard. No Shopify writes."""
from typing import Dict, List
import re

PROTECTED_FIELDS = {
    "Handle","Product ID","Variant ID","SKU","Variant SKU","Inventory","Inventory Qty",
    "Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value",
    "Variant Inventory Qty","Variant Inventory Tracker","Variant Inventory Policy","Variant Fulfillment Service",
    "Variant Requires Shipping","Variant Taxable","Barcode","Image Src","Image Position","Gift Card",
}
CONTAMINATION = re.compile(r"\\b(OUHOE|MISS\\.?\\s*QUEEN|HOEGOA|FANZHEN|EELHOPE|COLOR\\s*FIT|WEST\\s*&\\s*MONTH|SUPPLIER|WHOLESALE|GENERIC)\\b", re.I)
REQUIRED = ("Title", "Body HTML")

def validate_row(row: Dict[str, str]) -> List[str]:
    issues=[]
    for field in REQUIRED:
        if not str(row.get(field,"")).strip(): issues.append(f"missing:{field}")
    text=" ".join(str(row.get(k,"")) for k in ("Title","Body HTML","Product Type","Tags","SEO Title","SEO Description"))
    if CONTAMINATION.search(text): issues.append("supplier-contamination")
    return issues

def validate_protected(before: Dict[str,str], after: Dict[str,str]) -> List[str]:
    return [f"protected-mutated:{k}" for k in PROTECTED_FIELDS if str(before.get(k,"")) != str(after.get(k,""))]

def validate_catalog(rows: List[Dict[str,str]]) -> Dict[str,object]:
    issues=[]
    for i,row in enumerate(rows,1):
        for issue in validate_row(row): issues.append(f"row:{i}:{issue}")
    titles=[str(r.get("Title","")).strip().lower() for r in rows if str(r.get("Title","")).strip()]
    duplicates=sorted({t for t in titles if titles.count(t)>1})
    if duplicates: issues.append("duplicate-titles")
    return {"ok": not issues, "issues": issues, "rows": len(rows)}
