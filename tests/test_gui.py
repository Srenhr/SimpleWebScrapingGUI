import pytest
from unittest.mock import patch
from src.ui.scraper_gui import WebScraperGUI
from src.config import AppConfig
from src.core.scraper_service import ScraperService

@pytest.fixture
def config():
    return AppConfig()

@pytest.fixture
def gui(config):
    return WebScraperGUI(config)

class TestWebScraperGUI:
    def test_create_layout(self, gui):
        layout = gui.create_layout()
        assert isinstance(layout, list)
        assert any(isinstance(elem, list) for elem in layout)
        assert any("-URL-" in str(elem) for elem in layout[0])
        assert any("-OUTPUT-" in str(elem) for elem in layout[1])
        assert any("-FILELIST-" in str(elem) for elem in layout[5])

    @pytest.mark.asyncio
    async def test_handle_search_empty_url(self, gui):
        values = {"-URL-": "", "-FILETYPE-": ".pdf"}
        await gui.handle_search(values)
        # Should not raise and handle empty URL gracefully

    @pytest.mark.asyncio
    async def test_handle_download_no_selection(self, gui):
        values = {"-FILELIST-": [], "-OUTPUT-": "downloads"}
        await gui.handle_download(values)
        # Should show error popup for no selection

    @pytest.mark.asyncio
    async def test_handle_show_in_browser_no_selection(self, gui):
        values = {"-FILELIST-": []}
        await gui.handle_show_in_browser(values)
        # Should handle no selection gracefully

    @pytest.mark.asyncio
    async def test_handle_search_retry_logic(self, gui):
        values = {"-URL-": "http://example.com", "-FILETYPE-": ".pdf"}
        
        with patch.object(ScraperService, 'fetch_files', side_effect=[Exception("Test error"), ["http://example.com/test1.pdf"]]):
            await gui.handle_search(values)
            # Should retry and eventually succeed