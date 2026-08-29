"""Smoke tests for catalog orchestration."""
import pandas as pd
from mvqueen_engine.catalog_processor.processor import process_dataframe


def test_process_dataframe_preserves_handle_and_enriches_catalog():
    source = pd.DataFrame([{"Handle": "test-product", "Title": "Test Product", "Body (HTML)": "", "Tags": "test"}])
    result = process_dataframe(source)
    assert result.loc[0, "Handle"] == "test-product"
    assert str(result.loc[0, "Title"]).strip()
    assert "SEO Title" in result.columns
    assert "SEO Description" in result.columns
    assert "metafield.custom.editorial_frame" in result.columns
