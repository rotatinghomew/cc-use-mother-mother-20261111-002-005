from __future__ import annotations
import hashlib
import json
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

class DomainError(ValueError): pass
class ConflictError(DomainError): pass
class TransitionError(DomainError): pass

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def fingerprint(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()

def normalize_text(value: Any, field_name: str, limit: int = 500) -> str:
    if value is None: return ""
    if not isinstance(value, (str, int, float)): raise DomainError(f"{field_name} must be scalar")
    result = " ".join(str(value).split())
    if len(result) > limit: raise DomainError(f"{field_name} exceeds {limit}")
    return result

def normalize_number(value: Any, field_name: str, low: float = -1e12, high: float = 1e12) -> float:
    if isinstance(value, bool): raise DomainError(f"{field_name} must be numeric")
    try: result = float(value)
    except (TypeError, ValueError): raise DomainError(f"{field_name} must be numeric") from None
    if not low <= result <= high: raise DomainError(f"{field_name} outside range")
    return result

def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool): return value
    text = normalize_text(value, "boolean", 20).casefold()
    if text in {"1","true","yes","y","是"}: return True
    if text in {"0","false","no","n","否",""}: return False
    raise DomainError("invalid boolean")

def deep_get(value: Mapping[str, Any], dotted: str, default: Any = None) -> Any:
    current: Any = value
    for part in dotted.split("."):
        if not isinstance(current, Mapping) or part not in current: return default
        current = current[part]
    return current

def deep_set(value: dict[str, Any], dotted: str, item: Any) -> None:
    parts = dotted.split(".")
    current = value
    for part in parts[:-1]: current = current.setdefault(part, {})
    current[parts[-1]] = item

def unique(values: Iterable[Any]) -> list[Any]:
    seen=set(); result=[]
    for value in values:
        marker=stable_json(value)
        if marker not in seen: seen.add(marker); result.append(value)
    return result

def chunks(values: Sequence[Any], size: int) -> Iterator[Sequence[Any]]:
    if size <= 0: raise DomainError("chunk size must be positive")
    for index in range(0, len(values), size): yield values[index:index+size]

@dataclass(slots=True)
class Event:
    event_id: str
    run_id: str
    stage: str
    kind: str
    detail: dict[str, Any]
    created_at: str = field(default_factory=utc_now)

@dataclass(slots=True)
class ProcessingContext:
    run_id: str
    case_id: str
    payload: dict[str, Any]
    state: str = "received"
    revision: int = 0
    flags: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)

    def emit(self, stage: str, kind: str, **detail: Any) -> Event:
        event=Event(uuid.uuid4().hex, self.run_id, stage, kind, detail)
        self.events.append(event); return event

    def flag(self, value: str) -> None:
        text=normalize_text(value, "flag", 120)
        if text and text not in self.flags: self.flags.append(text); self.flags.sort()

    def advance(self, stage: str) -> None:
        stage=normalize_text(stage, "stage", 100)
        if self.state != stage: self.state=stage; self.revision += 1
        self.emit(stage, "stage_completed", revision=self.revision)

    def add_evidence(self, stage: str, rule: str, source: str, target: str, value: Any) -> None:
        self.evidence.append({"stage":stage,"rule":rule,"source":source,"target":target,"digest":fingerprint(value)})

    def snapshot(self) -> dict[str, Any]:
        return {"run_id":self.run_id,"case_id":self.case_id,"payload":self.payload,"state":self.state,
                "revision":self.revision,"flags":self.flags,"metrics":self.metrics,"evidence":self.evidence,
                "events":[asdict(event) for event in self.events]}

class SQLiteLedger:
    def __init__(self, path: str | Path):
        self.path=str(path); self.lock=threading.RLock(); self.initialize()

    def connect(self) -> sqlite3.Connection:
        con=sqlite3.connect(self.path, timeout=20, isolation_level=None)
        con.row_factory=sqlite3.Row
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("PRAGMA busy_timeout=20000")
        return con

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self.lock:
            con=self.connect()
            try:
                con.execute("BEGIN IMMEDIATE"); yield con; con.execute("COMMIT")
            except Exception:
                con.execute("ROLLBACK"); raise
            finally: con.close()

    def initialize(self) -> None:
        with self.connect() as con:
            con.executescript("""
            CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, case_id TEXT NOT NULL, state TEXT NOT NULL,
              revision INTEGER NOT NULL, payload_json TEXT NOT NULL, flags_json TEXT NOT NULL,
              metrics_json TEXT NOT NULL, evidence_json TEXT NOT NULL, checksum TEXT NOT NULL, updated_at TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS runs_case ON runs(case_id, updated_at);
            CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, stage TEXT NOT NULL,
              kind TEXT NOT NULL, detail_json TEXT NOT NULL, created_at TEXT NOT NULL,
              FOREIGN KEY(run_id) REFERENCES runs(run_id));
            CREATE TABLE IF NOT EXISTS idempotency(request_key TEXT PRIMARY KEY, run_id TEXT NOT NULL,
              response_json TEXT NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS checkpoints(run_id TEXT NOT NULL, stage TEXT NOT NULL, revision INTEGER NOT NULL,
              snapshot_json TEXT NOT NULL, created_at TEXT NOT NULL, PRIMARY KEY(run_id, stage));
            CREATE TABLE IF NOT EXISTS dead_letters(item_id TEXT PRIMARY KEY, run_id TEXT, stage TEXT NOT NULL,
              reason TEXT NOT NULL, body_json TEXT NOT NULL, attempts INTEGER NOT NULL, next_attempt REAL NOT NULL,
              created_at TEXT NOT NULL);
            """)

    def save(self, ctx: ProcessingContext, expected_revision: int | None = None) -> None:
        snap=ctx.snapshot(); checksum=fingerprint(snap)
        with self.transaction() as con:
            old=con.execute("SELECT revision FROM runs WHERE run_id=?",(ctx.run_id,)).fetchone()
            if expected_revision is not None and (old is None or old["revision"] != expected_revision):
                raise ConflictError("revision conflict")
            con.execute("""INSERT INTO runs VALUES(?,?,?,?,?,?,?,?,?,?)
              ON CONFLICT(run_id) DO UPDATE SET case_id=excluded.case_id,state=excluded.state,
              revision=excluded.revision,payload_json=excluded.payload_json,flags_json=excluded.flags_json,
              metrics_json=excluded.metrics_json,evidence_json=excluded.evidence_json,
              checksum=excluded.checksum,updated_at=excluded.updated_at""",
              (ctx.run_id,ctx.case_id,ctx.state,ctx.revision,stable_json(ctx.payload),stable_json(ctx.flags),
               stable_json(ctx.metrics),stable_json(ctx.evidence),checksum,utc_now()))
            for event in ctx.events:
                con.execute("INSERT OR IGNORE INTO events VALUES(?,?,?,?,?,?)",
                  (event.event_id,event.run_id,event.stage,event.kind,stable_json(event.detail),event.created_at))
            con.execute("INSERT OR REPLACE INTO checkpoints VALUES(?,?,?,?,?)",
              (ctx.run_id,ctx.state,ctx.revision,stable_json(snap),utc_now()))

    def load(self, run_id: str) -> ProcessingContext | None:
        with self.connect() as con:
            row=con.execute("SELECT * FROM runs WHERE run_id=?",(run_id,)).fetchone()
            if row is None: return None
            ctx=ProcessingContext(row["run_id"],row["case_id"],json.loads(row["payload_json"]),row["state"],row["revision"],
                json.loads(row["flags_json"]),json.loads(row["metrics_json"]),json.loads(row["evidence_json"]),[])
            events=con.execute("SELECT * FROM events WHERE run_id=? ORDER BY created_at,event_id",(run_id,)).fetchall()
            ctx.events=[Event(e["event_id"],e["run_id"],e["stage"],e["kind"],json.loads(e["detail_json"]),e["created_at"]) for e in events]
            return ctx

    def remember(self, key: str, run_id: str, response: Mapping[str, Any]) -> None:
        with self.transaction() as con:
            con.execute("INSERT OR REPLACE INTO idempotency VALUES(?,?,?,?)",(key,run_id,stable_json(response),utc_now()))

    def recalled(self, key: str) -> dict[str, Any] | None:
        with self.connect() as con:
            row=con.execute("SELECT response_json FROM idempotency WHERE request_key=?",(key,)).fetchone()
            return json.loads(row[0]) if row else None

    def dead_letter(self, ctx: ProcessingContext | None, stage: str, reason: str, body: Mapping[str, Any], attempts: int=1) -> str:
        item=uuid.uuid4().hex
        with self.transaction() as con:
            con.execute("INSERT INTO dead_letters VALUES(?,?,?,?,?,?,?,?)",
              (item,ctx.run_id if ctx else None,stage,normalize_text(reason,"reason",500),stable_json(body),attempts,time.time()+min(3600,2**attempts),utc_now()))
        return item

    def due_dead_letters(self, now_value: float | None=None, limit: int=100) -> list[dict[str, Any]]:
        now_value=time.time() if now_value is None else now_value
        with self.connect() as con:
            rows=con.execute("SELECT * FROM dead_letters WHERE next_attempt<=? ORDER BY next_attempt LIMIT ?",(now_value,limit)).fetchall()
            return [dict(row) | {"body":json.loads(row["body_json"])} for row in rows]

class GenericRuleProcessor:
    stage="generic"; rules: list[dict[str, Any]]=[]
    def process(self, ctx: ProcessingContext) -> ProcessingContext:
        for rule in self.rules: self.apply_rule(ctx,rule)
        ctx.advance(self.stage); return ctx

    def apply_rule(self, ctx: ProcessingContext, rule: Mapping[str, Any]) -> None:
        source=str(rule["source"]); target=str(rule["target"]); value=deep_get(ctx.payload,source)
        if value is None or value == "":
            if rule.get("required"): ctx.flag(f"missing:{source}"); ctx.emit(self.stage,"required_missing",source=source)
            else: ctx.emit(self.stage,"optional_missing",source=source)
            return
        op=rule.get("op","text"); param=rule.get("param")
        try: result=self.transform(op,value,param,ctx)
        except DomainError as exc:
            ctx.flag(f"invalid:{source}"); ctx.emit(self.stage,"rule_failed",rule=rule["key"],error=str(exc)); return
        deep_set(ctx.payload,target,result); ctx.add_evidence(self.stage,str(rule["key"]),source,target,result)
        if rule.get("metric"):
            try: ctx.metrics[str(rule["metric"])]=float(result)
            except (TypeError,ValueError): pass
        ctx.emit(self.stage,"rule_applied",rule=rule["key"],target=target)

    def transform(self, op: str, value: Any, param: Any, ctx: ProcessingContext) -> Any:
        if op=="text": return normalize_text(value,"value",int(param or 500))
        if op=="lower": return normalize_text(value,"value",int(param or 500)).casefold()
        if op=="upper": return normalize_text(value,"value",int(param or 500)).upper()
        if op=="number": return normalize_number(value,"value",0,float(param or 1e12))
        if op=="integer": return int(normalize_number(value,"value",0,float(param or 1e12)))
        if op=="boolean": return normalize_bool(value)
        if op=="list": return unique(value if isinstance(value,list) else [part.strip() for part in normalize_text(value,"value").split(",") if part.strip()])
        if op=="code": return normalize_text(value,"value",80).replace(" ","_").upper()
        if op=="token": return fingerprint({"salt":param,"value":normalize_text(value,"value")})[:24]
        if op=="bucket":
            number=normalize_number(value,"value",0,float(param or 1000000)); width=max(1,float(param or 10)); return int(number//width)*width
        if op=="ratio":
            number=normalize_number(value,"value",0,float(param or 1000000)); return round(number/float(param or 100),6)
        if op=="status":
            text=normalize_text(value,"value",80).casefold(); allowed=[str(x).casefold() for x in (param or [])]
            if allowed and text not in allowed: raise DomainError("unsupported status")
            return text
        if op=="checksum": return fingerprint(value)
        if op=="window": return {"value":normalize_text(value,"value"),"window":int(param or 30)}
        raise DomainError(f"unknown operation {op}")
