from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class WorkflowSyntaxTests(unittest.TestCase):
    def test_all_workflows_are_valid_yaml_mappings(self):
        workflow_dir = ROOT / ".github" / "workflows"
        for path in workflow_dir.glob("*.yml"):
            with self.subTest(path=path.name):
                parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertIsInstance(parsed, dict)
                self.assertIn("jobs", parsed)

    def test_quark_signin_uses_off_peak_schedule_and_serverchan_notification(self):
        path = ROOT / ".github" / "workflows" / "quark_signin.yml"
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        schedule = parsed[True]["schedule"]
        cron_expressions = {item["cron"] for item in schedule}
        steps = parsed["jobs"]["sign-in"]["steps"]
        notification_step = next(
            step for step in steps if step["name"] == "发送 Server 酱通知"
        )

        self.assertEqual(
            cron_expressions,
            {"17 1 * * *", "43 1 * * *", "23 5 * * *", "47 5 * * *"},
        )
        self.assertIn("always()", notification_step["if"])
        self.assertEqual(
            notification_step["env"]["SERVERCHAN_SENDKEY"],
            "${{ secrets.SERVERCHAN_SENDKEY }}",
        )


if __name__ == "__main__":
    unittest.main()
