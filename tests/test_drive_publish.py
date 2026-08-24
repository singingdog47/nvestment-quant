from company_intel.drive_publish import publish_directory


def test_intelligence_drive_writeback_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("INTELLIGENCE_DRIVE_WRITEBACK", raising=False)
    monkeypatch.setenv("GDRIVE_SERVICE_ACCOUNT_JSON", '{"type":"service_account"}')
    monkeypatch.setenv("GDRIVE_FOLDER_ID", "folder")
    result = publish_directory("does-not-matter")
    assert result["status"] == "skipped"
    assert "not enabled" in result["reason"]


def test_enabled_writeback_without_drive_secrets_skips_cleanly(monkeypatch):
    monkeypatch.setenv("INTELLIGENCE_DRIVE_WRITEBACK", "true")
    monkeypatch.delenv("GDRIVE_SERVICE_ACCOUNT_JSON", raising=False)
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_JSON", raising=False)
    monkeypatch.delenv("GDRIVE_FOLDER_ID", raising=False)
    monkeypatch.delenv("GOOGLE_DRIVE_FOLDER_ID", raising=False)
    result = publish_directory("does-not-matter")
    assert result == {"status": "skipped", "reason": "Drive secrets not set"}
