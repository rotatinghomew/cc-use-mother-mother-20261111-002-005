from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from oncology_capacity_exchange.service import ApplicationService
from oncology_capacity_exchange.runtime import DomainError, SQLiteLedger, fingerprint

class BusinessGroup1Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.db=Path(self.temp.name)/"state.sqlite3"
        self.service=ApplicationService(self.db)

    def tearDown(self):
        self.temp.cleanup()

    def make_record(self, seed: int, status: str="new"):
        return {"case_id":f"case-{seed}","subject_id":f"subject-{seed%11}","category":"screening",
                "region":f"region-{seed%5}","event_date":"2026-11-11","status":status,
                "count":seed+1,"total":seed+10,"attributes":{"seed":seed},
                "tags":["synthetic",f"group-1"],"source_system":"offline-test","revision":seed%3}

    def test_idempotent_replay(self):
        record=self.make_record(1)
        first=self.service.execute(record,request_key="same")
        second=self.service.execute(record,request_key="same")
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(first["run_id"],second["run_id"])

    def test_missing_case_rejected(self):
        with self.assertRaises(DomainError): self.service.execute({"status":"new"})

    def test_batch_partial_failure(self):
        result=self.service.execute_many([self.make_record(2),{"status":"new"},self.make_record(3)])
        self.assertEqual(result["accepted_count"],2)
        self.assertEqual(result["failure_count"],1)

    def test_ledger_roundtrip(self):
        result=self.service.execute(self.make_record(4),request_key="roundtrip")
        loaded=SQLiteLedger(self.db).load(result["run_id"])
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.case_id,"case-4")

    def test_business_case_100(self):
        record=self.make_record(100, status='new')
        result=self.service.execute(record, request_key="case-1-0")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_101(self):
        record=self.make_record(101, status='active')
        result=self.service.execute(record, request_key="case-1-1")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_102(self):
        record=self.make_record(102, status='pending')
        result=self.service.execute(record, request_key="case-1-2")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_103(self):
        record=self.make_record(103, status='closed')
        result=self.service.execute(record, request_key="case-1-3")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_104(self):
        record=self.make_record(104, status='new')
        result=self.service.execute(record, request_key="case-1-4")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_105(self):
        record=self.make_record(105, status='active')
        result=self.service.execute(record, request_key="case-1-5")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_106(self):
        record=self.make_record(106, status='pending')
        result=self.service.execute(record, request_key="case-1-6")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_107(self):
        record=self.make_record(107, status='closed')
        result=self.service.execute(record, request_key="case-1-7")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_108(self):
        record=self.make_record(108, status='new')
        result=self.service.execute(record, request_key="case-1-8")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_109(self):
        record=self.make_record(109, status='active')
        result=self.service.execute(record, request_key="case-1-9")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_110(self):
        record=self.make_record(110, status='pending')
        result=self.service.execute(record, request_key="case-1-10")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_111(self):
        record=self.make_record(111, status='closed')
        result=self.service.execute(record, request_key="case-1-11")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_112(self):
        record=self.make_record(112, status='new')
        result=self.service.execute(record, request_key="case-1-12")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_113(self):
        record=self.make_record(113, status='active')
        result=self.service.execute(record, request_key="case-1-13")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_114(self):
        record=self.make_record(114, status='pending')
        result=self.service.execute(record, request_key="case-1-14")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_115(self):
        record=self.make_record(115, status='closed')
        result=self.service.execute(record, request_key="case-1-15")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_116(self):
        record=self.make_record(116, status='new')
        result=self.service.execute(record, request_key="case-1-16")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_117(self):
        record=self.make_record(117, status='active')
        result=self.service.execute(record, request_key="case-1-17")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_118(self):
        record=self.make_record(118, status='pending')
        result=self.service.execute(record, request_key="case-1-18")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_119(self):
        record=self.make_record(119, status='closed')
        result=self.service.execute(record, request_key="case-1-19")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_120(self):
        record=self.make_record(120, status='new')
        result=self.service.execute(record, request_key="case-1-20")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_121(self):
        record=self.make_record(121, status='active')
        result=self.service.execute(record, request_key="case-1-21")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_122(self):
        record=self.make_record(122, status='pending')
        result=self.service.execute(record, request_key="case-1-22")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_123(self):
        record=self.make_record(123, status='closed')
        result=self.service.execute(record, request_key="case-1-23")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_124(self):
        record=self.make_record(124, status='new')
        result=self.service.execute(record, request_key="case-1-24")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_125(self):
        record=self.make_record(125, status='active')
        result=self.service.execute(record, request_key="case-1-25")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_126(self):
        record=self.make_record(126, status='pending')
        result=self.service.execute(record, request_key="case-1-26")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_127(self):
        record=self.make_record(127, status='closed')
        result=self.service.execute(record, request_key="case-1-27")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_128(self):
        record=self.make_record(128, status='new')
        result=self.service.execute(record, request_key="case-1-28")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_129(self):
        record=self.make_record(129, status='active')
        result=self.service.execute(record, request_key="case-1-29")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_130(self):
        record=self.make_record(130, status='pending')
        result=self.service.execute(record, request_key="case-1-30")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_131(self):
        record=self.make_record(131, status='closed')
        result=self.service.execute(record, request_key="case-1-31")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_132(self):
        record=self.make_record(132, status='new')
        result=self.service.execute(record, request_key="case-1-32")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_133(self):
        record=self.make_record(133, status='active')
        result=self.service.execute(record, request_key="case-1-33")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])

if __name__ == "__main__": unittest.main()
