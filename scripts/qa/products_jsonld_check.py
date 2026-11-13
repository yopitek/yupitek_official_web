#!/usr/bin/env python3
"""Validate JSON-LD (Product/FAQPage/BreadcrumbList/CollectionPage+ItemList) of built brand pages. Usage: products_jsonld_check.py <build_dir>
Exit 1 on errors. Warnings (Product without offers/review/aggregateRating) are listed but do not fail."""
import json,re,sys
from pathlib import Path
D=Path(sys.argv[1]); BR=("acr","flipperzero","hak5","sdrlab")
def blocks(h):
    for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        yield json.loads(s)
def flat(o):
    if isinstance(o,list):
        for x in o: yield from flat(x)
    elif isinstance(o,dict):
        if "@graph" in o: yield from flat(o["@graph"])
        else: yield o
errs=[];warns=[];n=0
for lang in ("en","zh-tw"):
  for b in BR:
    for p in sorted((D/lang/"products"/b).glob("*/index.html"))+[D/lang/"products"/b/"index.html"]:
        if not p.exists(): continue
        n+=1; h=p.read_text(errors="ignore"); k=str(p.relative_to(D))
        try: items=[i for bl in blocks(h) for i in flat(bl)]
        except Exception as e: errs.append((k,"invalid JSON "+str(e))); continue
        t={i.get("@type"):i for i in items}
        if p.parent.name!=b:  # product page
            P=t.get("Product")
            if not P: errs.append((k,"no Product")); 
            else:
                for f in ("name","image","description"):
                    if not P.get(f): errs.append((k,f"Product missing {f}"))
                if not (P.get("offers") or P.get("review") or P.get("aggregateRating")): warns.append((k,"Product has no offers/review/aggregateRating (not eligible for product rich result)"))
            F=t.get("FAQPage")
            if F:
                for q in F.get("mainEntity",[]):
                    if q.get("@type")!="Question" or not q.get("name") or not q.get("acceptedAnswer",{}).get("text"): errs.append((k,"bad FAQ item"))
        else:
            C=t.get("CollectionPage"); I=t.get("ItemList")
            if not C or not I: errs.append((k,"hub missing CollectionPage/ItemList"))
            elif not I.get("itemListElement"): errs.append((k,"empty ItemList"))
        B=t.get("BreadcrumbList")
        if not B: errs.append((k,"no BreadcrumbList"))
        else:
            pos=[e.get("position") for e in B["itemListElement"]]
            if pos!=list(range(1,len(pos)+1)): errs.append((k,f"breadcrumb positions {pos}"))
print("pages",n,"errors",len(errs),"warnings",len(warns))
for e in errs[:15]: print("ERR",e)
for w in warns[:3]: print("WARN", w)
sys.exit(1 if errs else 0)
