from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from oncology_capacity_exchange.service import ApplicationService
from oncology_capacity_exchange.runtime import DomainError, SQLiteLedger, fingerprint

class BusinessGroup5Tests(unittest.TestCase):
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
                "tags":["synthetic",f"group-5"],"source_system":"offline-test","revision":seed%3}

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

    def test_business_case_500(self):
        record=self.make_record(500, status='new')
        result=self.service.execute(record, request_key="case-5-0")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_501(self):
        record=self.make_record(501, status='active')
        result=self.service.execute(record, request_key="case-5-1")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_502(self):
        record=self.make_record(502, status='pending')
        result=self.service.execute(record, request_key="case-5-2")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_503(self):
        record=self.make_record(503, status='closed')
        result=self.service.execute(record, request_key="case-5-3")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_504(self):
        record=self.make_record(504, status='new')
        result=self.service.execute(record, request_key="case-5-4")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_505(self):
        record=self.make_record(505, status='active')
        result=self.service.execute(record, request_key="case-5-5")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_506(self):
        record=self.make_record(506, status='pending')
        result=self.service.execute(record, request_key="case-5-6")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_507(self):
        record=self.make_record(507, status='closed')
        result=self.service.execute(record, request_key="case-5-7")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_508(self):
        record=self.make_record(508, status='new')
        result=self.service.execute(record, request_key="case-5-8")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_509(self):
        record=self.make_record(509, status='active')
        result=self.service.execute(record, request_key="case-5-9")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_510(self):
        record=self.make_record(510, status='pending')
        result=self.service.execute(record, request_key="case-5-10")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_511(self):
        record=self.make_record(511, status='closed')
        result=self.service.execute(record, request_key="case-5-11")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_512(self):
        record=self.make_record(512, status='new')
        result=self.service.execute(record, request_key="case-5-12")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_513(self):
        record=self.make_record(513, status='active')
        result=self.service.execute(record, request_key="case-5-13")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_514(self):
        record=self.make_record(514, status='pending')
        result=self.service.execute(record, request_key="case-5-14")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_515(self):
        record=self.make_record(515, status='closed')
        result=self.service.execute(record, request_key="case-5-15")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_516(self):
        record=self.make_record(516, status='new')
        result=self.service.execute(record, request_key="case-5-16")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_517(self):
        record=self.make_record(517, status='active')
        result=self.service.execute(record, request_key="case-5-17")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_518(self):
        record=self.make_record(518, status='pending')
        result=self.service.execute(record, request_key="case-5-18")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_519(self):
        record=self.make_record(519, status='closed')
        result=self.service.execute(record, request_key="case-5-19")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_520(self):
        record=self.make_record(520, status='new')
        result=self.service.execute(record, request_key="case-5-20")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_521(self):
        record=self.make_record(521, status='active')
        result=self.service.execute(record, request_key="case-5-21")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_522(self):
        record=self.make_record(522, status='pending')
        result=self.service.execute(record, request_key="case-5-22")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_523(self):
        record=self.make_record(523, status='closed')
        result=self.service.execute(record, request_key="case-5-23")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_524(self):
        record=self.make_record(524, status='new')
        result=self.service.execute(record, request_key="case-5-24")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_525(self):
        record=self.make_record(525, status='active')
        result=self.service.execute(record, request_key="case-5-25")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_526(self):
        record=self.make_record(526, status='pending')
        result=self.service.execute(record, request_key="case-5-26")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_527(self):
        record=self.make_record(527, status='closed')
        result=self.service.execute(record, request_key="case-5-27")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_528(self):
        record=self.make_record(528, status='new')
        result=self.service.execute(record, request_key="case-5-28")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_529(self):
        record=self.make_record(529, status='active')
        result=self.service.execute(record, request_key="case-5-29")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_530(self):
        record=self.make_record(530, status='pending')
        result=self.service.execute(record, request_key="case-5-30")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_531(self):
        record=self.make_record(531, status='closed')
        result=self.service.execute(record, request_key="case-5-31")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_532(self):
        record=self.make_record(532, status='new')
        result=self.service.execute(record, request_key="case-5-32")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_533(self):
        record=self.make_record(533, status='active')
        result=self.service.execute(record, request_key="case-5-33")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])

if __name__ == "__main__": unittest.main()
