from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from oncology_capacity_exchange.service import ApplicationService
from oncology_capacity_exchange.runtime import DomainError, SQLiteLedger, fingerprint

class BusinessGroup4Tests(unittest.TestCase):
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
                "tags":["synthetic",f"group-4"],"source_system":"offline-test","revision":seed%3}

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

    def test_business_case_400(self):
        record=self.make_record(400, status='new')
        result=self.service.execute(record, request_key="case-4-0")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_401(self):
        record=self.make_record(401, status='active')
        result=self.service.execute(record, request_key="case-4-1")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_402(self):
        record=self.make_record(402, status='pending')
        result=self.service.execute(record, request_key="case-4-2")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_403(self):
        record=self.make_record(403, status='closed')
        result=self.service.execute(record, request_key="case-4-3")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_404(self):
        record=self.make_record(404, status='new')
        result=self.service.execute(record, request_key="case-4-4")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_405(self):
        record=self.make_record(405, status='active')
        result=self.service.execute(record, request_key="case-4-5")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_406(self):
        record=self.make_record(406, status='pending')
        result=self.service.execute(record, request_key="case-4-6")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_407(self):
        record=self.make_record(407, status='closed')
        result=self.service.execute(record, request_key="case-4-7")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_408(self):
        record=self.make_record(408, status='new')
        result=self.service.execute(record, request_key="case-4-8")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_409(self):
        record=self.make_record(409, status='active')
        result=self.service.execute(record, request_key="case-4-9")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_410(self):
        record=self.make_record(410, status='pending')
        result=self.service.execute(record, request_key="case-4-10")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_411(self):
        record=self.make_record(411, status='closed')
        result=self.service.execute(record, request_key="case-4-11")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_412(self):
        record=self.make_record(412, status='new')
        result=self.service.execute(record, request_key="case-4-12")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_413(self):
        record=self.make_record(413, status='active')
        result=self.service.execute(record, request_key="case-4-13")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_414(self):
        record=self.make_record(414, status='pending')
        result=self.service.execute(record, request_key="case-4-14")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_415(self):
        record=self.make_record(415, status='closed')
        result=self.service.execute(record, request_key="case-4-15")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_416(self):
        record=self.make_record(416, status='new')
        result=self.service.execute(record, request_key="case-4-16")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_417(self):
        record=self.make_record(417, status='active')
        result=self.service.execute(record, request_key="case-4-17")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_418(self):
        record=self.make_record(418, status='pending')
        result=self.service.execute(record, request_key="case-4-18")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_419(self):
        record=self.make_record(419, status='closed')
        result=self.service.execute(record, request_key="case-4-19")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_420(self):
        record=self.make_record(420, status='new')
        result=self.service.execute(record, request_key="case-4-20")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_421(self):
        record=self.make_record(421, status='active')
        result=self.service.execute(record, request_key="case-4-21")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_422(self):
        record=self.make_record(422, status='pending')
        result=self.service.execute(record, request_key="case-4-22")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_423(self):
        record=self.make_record(423, status='closed')
        result=self.service.execute(record, request_key="case-4-23")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_424(self):
        record=self.make_record(424, status='new')
        result=self.service.execute(record, request_key="case-4-24")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_425(self):
        record=self.make_record(425, status='active')
        result=self.service.execute(record, request_key="case-4-25")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_426(self):
        record=self.make_record(426, status='pending')
        result=self.service.execute(record, request_key="case-4-26")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_427(self):
        record=self.make_record(427, status='closed')
        result=self.service.execute(record, request_key="case-4-27")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_428(self):
        record=self.make_record(428, status='new')
        result=self.service.execute(record, request_key="case-4-28")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_429(self):
        record=self.make_record(429, status='active')
        result=self.service.execute(record, request_key="case-4-29")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_430(self):
        record=self.make_record(430, status='pending')
        result=self.service.execute(record, request_key="case-4-30")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_431(self):
        record=self.make_record(431, status='closed')
        result=self.service.execute(record, request_key="case-4-31")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_432(self):
        record=self.make_record(432, status='new')
        result=self.service.execute(record, request_key="case-4-32")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_433(self):
        record=self.make_record(433, status='active')
        result=self.service.execute(record, request_key="case-4-33")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])

if __name__ == "__main__": unittest.main()
