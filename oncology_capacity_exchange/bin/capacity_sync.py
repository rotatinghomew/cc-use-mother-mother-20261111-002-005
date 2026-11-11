from __future__ import annotations
import argparse
import json
from oncology_capacity_exchange.service import run_fixture

def main() -> int:
    parser=argparse.ArgumentParser(description='跨区域肿瘤诊疗容量采集交换站')
    parser.add_argument("fixture")
    parser.add_argument("--db",default="/tmp/oncology_capacity_exchange.sqlite3")
    args=parser.parse_args()
    result=run_fixture(args.fixture,args.db)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    return 0

if __name__ == "__main__": raise SystemExit(main())
