"""MVQUEEN OS — Shopify Admin GraphQL client.

Safety contract:
- credentials only from environment
- GraphQL-first
- explicit API version
- reads allowed in dry-run
- writes blocked in dry-run
- transient retry/backoff
- mutation userErrors fail closed
- no credentials persisted or logged
"""
from __future__ import annotations
import json, os, random, time
from typing import Any, Dict, Iterable, Optional
import requests

SHOPIFY_STORE_DOMAIN=os.getenv("SHOPIFY_STORE_DOMAIN","").strip()
SHOPIFY_API_VERSION=os.getenv("SHOPIFY_API_VERSION","2026-07")
SHOPIFY_ACCESS_TOKEN=os.getenv("SHOPIFY_ACCESS_TOKEN","")
SHOPIFY_DRY_RUN=os.getenv("SHOPIFY_DRY_RUN","true").lower()=="true"
SHOPIFY_TIMEOUT_SECONDS=float(os.getenv("SHOPIFY_TIMEOUT_SECONDS","30"))
SHOPIFY_MAX_RETRIES=int(os.getenv("SHOPIFY_MAX_RETRIES","4"))

class ShopifyGraphQLError(RuntimeError): pass
class ShopifyUserError(RuntimeError): pass

class ShopifyGraphQLClient:
    def __init__(self,store_domain:Optional[str]=None,access_token:Optional[str]=None,api_version:Optional[str]=None,dry_run:Optional[bool]=None):
        self.store_domain=(store_domain or SHOPIFY_STORE_DOMAIN).strip()
        self.access_token=access_token or SHOPIFY_ACCESS_TOKEN
        self.api_version=api_version or SHOPIFY_API_VERSION
        self.dry_run=SHOPIFY_DRY_RUN if dry_run is None else dry_run
        if not self.store_domain: raise ValueError("SHOPIFY_STORE_DOMAIN is required")
        if not self.access_token: raise ValueError("SHOPIFY_ACCESS_TOKEN is required")
        self.endpoint=f"https://{self.store_domain}/admin/api/{self.api_version}/graphql.json"

    @property
    def headers(self)->Dict[str,str]:
        return {"Content-Type":"application/json","Accept":"application/json","X-Shopify-Access-Token":self.access_token}

    @property
    def max_attempts(self)->int: return max(1,SHOPIFY_MAX_RETRIES+1)

    def execute(self,query:str,variables:Optional[Dict[str,Any]]=None,*,write:bool=False)->Dict[str,Any]:
        if write and self.dry_run:
            return {"data":None,"dry_run":True,"query":query,"variables":variables or {}}
        payload={"query":query,"variables":variables or {}}
        last_error:Optional[Exception]=None
        for attempt in range(self.max_attempts):
            try:
                response=requests.post(self.endpoint,headers=self.headers,json=payload,timeout=SHOPIFY_TIMEOUT_SECONDS)
                if response.status_code in (429,500,502,503,504):
                    retry_after=response.headers.get("Retry-After")
                    delay=float(retry_after) if retry_after else min(2**attempt,16)+random.random()
                    time.sleep(delay); continue
                response.raise_for_status()
                body=response.json()
                if body.get("errors"): raise ShopifyGraphQLError(json.dumps(body["errors"],indent=2))
                return body
            except (requests.RequestException,ShopifyGraphQLError) as exc:
                last_error=exc
                if attempt==self.max_attempts-1: break
                time.sleep(min(2**attempt,16)+random.random())
        raise ShopifyGraphQLError(str(last_error or "Unknown Shopify GraphQL error"))

    def mutate(self,mutation:str,variables:Optional[Dict[str,Any]]=None)->Dict[str,Any]:
        body=self.execute(mutation,variables,write=True)
        if body.get("dry_run"): return body
        errors=_find_user_errors(body.get("data") or {})
        if errors: raise ShopifyUserError(json.dumps(errors,indent=2))
        return body

    def query_all(self,query:str,connection_path:Iterable[str],*,variables:Optional[Dict[str,Any]]=None,first:int=100)->list[Dict[str,Any]]:
        variables=dict(variables or {}); variables["first"]=first; variables["after"]=None
        results=[]
        while True:
            body=self.execute(query,variables); node=body.get("data")
            for key in connection_path: node=node[key]
            results.extend(node.get("nodes",[]))
            page_info=node.get("pageInfo",{})
            if not page_info.get("hasNextPage"): break
            variables["after"]=page_info.get("endCursor")
        return results

def _find_user_errors(data:Dict[str,Any])->list[Dict[str,Any]]:
    found=[]
    for payload in data.values():
        if isinstance(payload,dict) and isinstance(payload.get("userErrors"),list):
            found.extend(error for error in payload["userErrors"] if error)
    return found

def get_client(*,dry_run:Optional[bool]=None)->ShopifyGraphQLClient:
    return ShopifyGraphQLClient(dry_run=dry_run)
