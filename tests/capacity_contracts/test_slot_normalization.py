from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from oncology_capacity_exchange.service import ApplicationService
from oncology_capacity_exchange.runtime import DomainError, SQLiteLedger, fingerprint

class BusinessGroup2Tests(unittest.TestCase):
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
                "tags":["synthetic",f"group-2"],"source_system":"offline-test","revision":seed%3}

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

    def test_business_case_200(self):
        record=self.make_record(200, status='new')
        result=self.service.execute(record, request_key="case-2-0")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_201(self):
        record=self.make_record(201, status='active')
        result=self.service.execute(record, request_key="case-2-1")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_202(self):
        record=self.make_record(202, status='pending')
        result=self.service.execute(record, request_key="case-2-2")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_203(self):
        record=self.make_record(203, status='closed')
        result=self.service.execute(record, request_key="case-2-3")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_204(self):
        record=self.make_record(204, status='new')
        result=self.service.execute(record, request_key="case-2-4")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_205(self):
        record=self.make_record(205, status='active')
        result=self.service.execute(record, request_key="case-2-5")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_206(self):
        record=self.make_record(206, status='pending')
        result=self.service.execute(record, request_key="case-2-6")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_207(self):
        record=self.make_record(207, status='closed')
        result=self.service.execute(record, request_key="case-2-7")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_208(self):
        record=self.make_record(208, status='new')
        result=self.service.execute(record, request_key="case-2-8")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_209(self):
        record=self.make_record(209, status='active')
        result=self.service.execute(record, request_key="case-2-9")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_210(self):
        record=self.make_record(210, status='pending')
        result=self.service.execute(record, request_key="case-2-10")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_211(self):
        record=self.make_record(211, status='closed')
        result=self.service.execute(record, request_key="case-2-11")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_212(self):
        record=self.make_record(212, status='new')
        result=self.service.execute(record, request_key="case-2-12")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_213(self):
        record=self.make_record(213, status='active')
        result=self.service.execute(record, request_key="case-2-13")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_214(self):
        record=self.make_record(214, status='pending')
        result=self.service.execute(record, request_key="case-2-14")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_215(self):
        record=self.make_record(215, status='closed')
        result=self.service.execute(record, request_key="case-2-15")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_216(self):
        record=self.make_record(216, status='new')
        result=self.service.execute(record, request_key="case-2-16")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_217(self):
        record=self.make_record(217, status='active')
        result=self.service.execute(record, request_key="case-2-17")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_218(self):
        record=self.make_record(218, status='pending')
        result=self.service.execute(record, request_key="case-2-18")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_219(self):
        record=self.make_record(219, status='closed')
        result=self.service.execute(record, request_key="case-2-19")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_220(self):
        record=self.make_record(220, status='new')
        result=self.service.execute(record, request_key="case-2-20")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_221(self):
        record=self.make_record(221, status='active')
        result=self.service.execute(record, request_key="case-2-21")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_222(self):
        record=self.make_record(222, status='pending')
        result=self.service.execute(record, request_key="case-2-22")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_223(self):
        record=self.make_record(223, status='closed')
        result=self.service.execute(record, request_key="case-2-23")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_224(self):
        record=self.make_record(224, status='new')
        result=self.service.execute(record, request_key="case-2-24")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_225(self):
        record=self.make_record(225, status='active')
        result=self.service.execute(record, request_key="case-2-25")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_226(self):
        record=self.make_record(226, status='pending')
        result=self.service.execute(record, request_key="case-2-26")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_227(self):
        record=self.make_record(227, status='closed')
        result=self.service.execute(record, request_key="case-2-27")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_228(self):
        record=self.make_record(228, status='new')
        result=self.service.execute(record, request_key="case-2-28")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_229(self):
        record=self.make_record(229, status='active')
        result=self.service.execute(record, request_key="case-2-29")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_230(self):
        record=self.make_record(230, status='pending')
        result=self.service.execute(record, request_key="case-2-30")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_231(self):
        record=self.make_record(231, status='closed')
        result=self.service.execute(record, request_key="case-2-31")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_232(self):
        record=self.make_record(232, status='new')
        result=self.service.execute(record, request_key="case-2-32")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])
    def test_business_case_233(self):
        record=self.make_record(233, status='active')
        result=self.service.execute(record, request_key="case-2-33")
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["case_id"], record["case_id"])
        self.assertGreaterEqual(result["evidence_count"], 8)
        self.assertIn("business", result["payload"])

if __name__ == "__main__": unittest.main()
