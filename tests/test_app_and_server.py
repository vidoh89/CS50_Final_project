import asyncio

import pytest
import threading
import socket
from app_ui.navbar import Navbar
from app import app
from shiny import run_app
from playwright.async_api import Page, expect, async_playwright
import re
def get_free_port():
    """ Function to find an open(free) port , helps to prevent test from clashing."""
    sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # set socket Family and Socket type
    sock.bind(('127.0.0.1',0)) # Select port for testing
    port= sock.getsockname()[1] # Retrieve the assigned port
    sock.close()
    return port
@pytest.fixture(scope="module")
async def local_app_url():
    """
    Simulate local server for Navbar component
    """
    port = get_free_port()
    url = f"http://127.0.0.1:{port}" # test url for Playwright to visit

    # Run app with trailing shutdown <Daemon thread>
    thread = threading.Thread(
        target=run_app,
        args=(app,),
        kwargs= {"port":port,"launch_browser":False},
        daemon=True
    )
    thread.start()

    # Give server time to start
    await asyncio.sleep(2)

    yield url # yield url to give server time to initialize

@pytest.mark.asyncio
async def test_initial_ui_state(local_app_url:str):
    """
    Check that Navbar and default GDP panel load correctly
    :param local_app_url: test url
    :type local_app_url:str
    """
    # Ensure the browser launches in the current running loop
    async with async_playwright() as p:
        browser= await p.chromium.launch()
        try:
            page = await browser.new_page()
            await page.goto(local_app_url)
            # Wait for network to idle
            await page.wait_for_load_state("networkidle")

            # Verify Logo element displays on page
            await page.wait_for_selector(".Logo",timeout=5000,state="visible")

            # Verify slider appears as expected
            await page.wait_for_selector(".irs-handle",timeout=5000,state="visible")

            #Verify the title from (ui.page_navbar)
            await expect(page).to_have_title(re.compile(r"GDP Growth Rate"), timeout=10000)
        finally:
            await browser.close()









