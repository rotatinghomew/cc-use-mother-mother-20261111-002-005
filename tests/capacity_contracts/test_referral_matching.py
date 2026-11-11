from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from oncology_capacity_exchange.service import ApplicationService
from oncology_capacity_exchange.runtime import DomainError, SQLiteLedger, fingerprint

class BusinessGroup3Tests(unittest.TestCase):
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
                "tags":["synthetic",f"group-3"],"source_system":"offline-test","revision":seed%3}

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

    def test_business_case_300(self):
        record=self.make_record(300, status='new')
        result=self.service.execute(record, request_key="case-3-0")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_301(self):
        record=self.make_record(301, status='active')
        result=self.service.execute(record, request_key="case-3-1")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_302(self):
        record=self.make_record(302, status='pending')
        result=self.service.execute(record, request_key="case-3-2")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_303(self):
        record=self.make_record(303, status='closed')
        result=self.service.execute(record, request_key="case-3-3")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_304(self):
        record=self.make_record(304, status='new')
        result=self.service.execute(record, request_key="case-3-4")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_305(self):
        record=self.make_record(305, status='active')
        result=self.service.execute(record, request_key="case-3-5")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_306(self):
        record=self.make_record(306, status='pending')
        result=self.service.execute(record, request_key="case-3-6")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_307(self):
        record=self.make_record(307, status='closed')
        result=self.service.execute(record, request_key="case-3-7")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_308(self):
        record=self.make_record(308, status='new')
        result=self.service.execute(record, request_key="case-3-8")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_309(self):
        record=self.make_record(309, status='active')
        result=self.service.execute(record, request_key="case-3-9")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_310(self):
        record=self.make_record(310, status='pending')
        result=self.service.execute(record, request_key="case-3-10")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_311(self):
        record=self.make_record(311, status='closed')
        result=self.service.execute(record, request_key="case-3-11")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_312(self):
        record=self.make_record(312, status='new')
        result=self.service.execute(record, request_key="case-3-12")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_313(self):
        record=self.make_record(313, status='active')
        result=self.service.execute(record, request_key="case-3-13")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_314(self):
        record=self.make_record(314, status='pending')
        result=self.service.execute(record, request_key="case-3-14")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_315(self):
        record=self.make_record(315, status='closed')
        result=self.service.execute(record, request_key="case-3-15")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_316(self):
        record=self.make_record(316, status='new')
        result=self.service.execute(record, request_key="case-3-16")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_317(self):
        record=self.make_record(317, status='active')
        result=self.service.execute(record, request_key="case-3-17")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_318(self):
        record=self.make_record(318, status='pending')
        result=self.service.execute(record, request_key="case-3-18")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_319(self):
        record=self.make_record(319, status='closed')
        result=self.service.execute(record, request_key="case-3-19")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_320(self):
        record=self.make_record(320, status='new')
        result=self.service.execute(record, request_key="case-3-20")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_321(self):
        record=self.make_record(321, status='active')
        result=self.service.execute(record, request_key="case-3-21")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_322(self):
        record=self.make_record(322, status='pending')
        result=self.service.execute(record, request_key="case-3-22")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_323(self):
        record=self.make_record(323, status='closed')
        result=self.service.execute(record, request_key="case-3-23")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_324(self):
        record=self.make_record(324, status='new')
        result=self.service.execute(record, request_key="case-3-24")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_325(self):
        record=self.make_record(325, status='active')
        result=self.service.execute(record, request_key="case-3-25")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_326(self):
        record=self.make_record(326, status='pending')
        result=self.service.execute(record, request_key="case-3-26")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_327(self):
        record=self.make_record(327, status='closed')
        result=self.service.execute(record, request_key="case-3-27")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_328(self):
        record=self.make_record(328, status='new')
        result=self.service.execute(record, request_key="case-3-28")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_329(self):
        record=self.make_record(329, status='active')
        result=self.service.execute(record, request_key="case-3-29")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_330(self):
        record=self.make_record(330, status='pending')
        result=self.service.execute(record, request_key="case-3-30")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_331(self):
        record=self.make_record(331, status='closed')
        result=self.service.execute(record, request_key="case-3-31")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_332(self):
        record=self.make_record(332, status='new')
        result=self.service.execute(record, request_key="case-3-32")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_333(self):
        record=self.make_record(333, status='active')
        result=self.service.execute(record, request_key="case-3-33")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])

if __name__ == "__main__": unittest.main()
