from __future__ import annotations
import json
import uuid
from pathlib import Path
from typing import Any, Mapping
from oncology_capacity_exchange.runtime import DomainError, ProcessingContext, SQLiteLedger, fingerprint, normalize_text
from oncology_capacity_exchange.robots.site_probe import build_processor as site_probe_factory
from oncology_capacity_exchange.inventory.calendar_slots import build_processor as calendar_slots_factory
from oncology_capacity_exchange.normalization.capacity_units import build_processor as capacity_units_factory
from oncology_capacity_exchange.matching.referral_fit import build_processor as referral_fit_factory
from oncology_capacity_exchange.holds.lease_book import build_processor as lease_book_factory
from oncology_capacity_exchange.reconciliation.site_receipts import build_processor as site_receipts_factory
from oncology_capacity_exchange.resilience.circuit_state import build_processor as circuit_state_factory
from oncology_capacity_exchange.operations.network_view import build_processor as network_view_factory

PROCESSOR_FACTORIES = [site_probe_factory, calendar_slots_factory, capacity_units_factory, referral_fit_factory, lease_book_factory, site_receipts_factory, circuit_state_factory, network_view_factory]

class ApplicationService:
    def __init__(self, database: str | Path):
        self.ledger=SQLiteLedger(database)
        self.processors=[factory() for factory in PROCESSOR_FACTORIES]

    def validate_input(self, record: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(record, Mapping): raise DomainError("record must be object")
        result=dict(record)
        result["case_id"]=normalize_text(result.get("case_id"),"case_id",96)
        if not result["case_id"]: raise DomainError("case_id is required")
        result.setdefault("subject_id",result["case_id"])
        result.setdefault("category","screening")
        result.setdefault("region","synthetic-region")
        result.setdefault("event_date","2026-11-11")
        result.setdefault("status","new")
        result.setdefault("count",1)
        result.setdefault("total",1)
        result.setdefault("attributes",{"source":"synthetic"})
        result.setdefault("tags",["offline","fixture"])
        result.setdefault("source_system","local-fixture")
        result.setdefault("revision",0)
        return result

    def execute(self, record: Mapping[str, Any], request_key: str | None=None) -> dict[str, Any]:
        normalized=self.validate_input(record)
        normalized=self.architecture_preflight(normalized)
        key=request_key or fingerprint(normalized)
        recalled=self.ledger.recalled(key)
        if recalled is not None: return recalled | {"replayed":True}
        ctx=ProcessingContext(uuid.uuid4().hex,normalized["case_id"],normalized)
        ctx.emit("received","run_started",project='oncology_capacity_exchange')
        try:
            for processor in self.architecture_plan(ctx):
                processor.process(ctx)
                self.ledger.save(ctx)
        except Exception as exc:
            self.ledger.dead_letter(ctx,ctx.state,str(exc),normalized)
            raise
        self.architecture_finalize(ctx)
        ctx.advance("completed")
        self.ledger.save(ctx)
        response={"project":'oncology_capacity_exchange',"run_id":ctx.run_id,"case_id":ctx.case_id,"state":ctx.state,
                  "revision":ctx.revision,"flags":ctx.flags,"metrics":ctx.metrics,"evidence_count":len(ctx.evidence),
                  "event_count":len(ctx.events),"payload":ctx.payload,"replayed":False}
        self.ledger.remember(key,ctx.run_id,response)
        return response

    def architecture_preflight(self, record):
        record=dict(record)
        count=max(0,int(record.get("count",0)))
        record["capacity_book"]={"advertised":count,"held":0,"confirmed":0,"leases":[],"circuit":"closed"}
        return record

    def architecture_plan(self, ctx):
        capacity=ctx.payload["capacity_book"]
        if capacity["advertised"] <= 0: capacity["circuit"]="open"; ctx.flag("capacity:unavailable")
        return list(self.processors)

    def architecture_finalize(self, ctx):
        book=ctx.payload["capacity_book"]
        if book["circuit"]=="closed":
            lease={"lease_id":fingerprint({"case":ctx.case_id,"revision":ctx.revision})[:16],"units":min(1,book["advertised"]),"state":"confirmed"}
            book["leases"].append(lease); book["held"]=lease["units"]; book["confirmed"]=lease["units"]
        ctx.metrics["remaining_capacity"]=book["advertised"]-book["confirmed"]
        ctx.emit("capacity_lease","book_reconciled",book=book)

    def execute_many(self, records: list[Mapping[str, Any]]) -> dict[str, Any]:
        outputs=[]; failures=[]
        for index, record in enumerate(records):
            try: outputs.append(self.execute(record,request_key=f"batch:{index}:{fingerprint(record)}"))
            except Exception as exc: failures.append({"index":index,"error":str(exc)})
        return {"accepted":outputs,"failures":failures,"accepted_count":len(outputs),"failure_count":len(failures)}

def run_fixture(fixture: str | Path, database: str | Path) -> dict[str, Any]:
    data=json.loads(Path(fixture).read_text(encoding="utf-8"))
    service=ApplicationService(database)
    if isinstance(data,list): return service.execute_many(data)
    return service.execute(data)
