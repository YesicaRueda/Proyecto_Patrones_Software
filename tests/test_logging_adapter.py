import os
from src.infrastructure.logging_adapter import StandardLoggingAdapter


def test_adapter_creates_log_file(tmp_path):
    log_file = tmp_path / "test.log"
    adapter = StandardLoggingAdapter(filename=str(log_file))

    adapter.write("mensaje de prueba", level="INFO")

    assert os.path.exists(log_file)

    with open(log_file, "r") as f:
        content = f.read()

    assert "mensaje de prueba" in content
    assert "INFO" in content