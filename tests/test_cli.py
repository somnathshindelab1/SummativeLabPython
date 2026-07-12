import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CLITests(unittest.TestCase):
    def run_cli(self, *args, data_file):
        env = os.environ.copy()
        env["PROJECT_DATA_FILE"] = str(data_file)
        return subprocess.run(
            [sys.executable, "main.py", *args],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_add_user_project_task_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_file = Path(tmp_dir) / "project_data.json"

            user_result = self.run_cli(
                "add-user",
                "--name",
                "Alex",
                "--email",
                "alex@example.com",
                data_file=data_file,
            )
            self.assertEqual(user_result.returncode, 0, user_result.stderr)
            self.assertIn("Added user", user_result.stdout)

            project_result = self.run_cli(
                "add-project",
                "--user",
                "Alex",
                "--title",
                "CLI Tool",
                "--description",
                "Build a management CLI",
                data_file=data_file,
            )
            self.assertEqual(project_result.returncode, 0, project_result.stderr)
            self.assertIn("Added project", project_result.stdout)

            task_result = self.run_cli(
                "add-task",
                "--project",
                "CLI Tool",
                "--title",
                "Implement add-task",
                data_file=data_file,
            )
            self.assertEqual(task_result.returncode, 0, task_result.stderr)
            self.assertIn("Added task", task_result.stdout)

            summary_result = self.run_cli(
                "summarize-project",
                "--project",
                "CLI Tool",
                data_file=data_file,
            )
            self.assertEqual(summary_result.returncode, 0, summary_result.stderr)
            self.assertIn("Summary", summary_result.stdout)


if __name__ == "__main__":
    unittest.main()
