测试：python3 -m unittest discover -s tests/capacity_contracts -p 'test_*.py'
构建：python3 -m compileall -q oncology_capacity_exchange
验收：python3 -m oncology_capacity_exchange.bin.capacity_sync fixtures/demo.json --db /tmp/oncology_capacity_exchange-acceptance.sqlite3
