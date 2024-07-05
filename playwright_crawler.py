# import asyncio
# from playwright.async_api import async_playwright, expect

# async def fetch_page_content():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         await page.goto('https://ghc.anitab.org/pricing')
#         await page.wait_for_load_state('networkidle')  # Wait for network to be idle
#         await asyncio.sleep(5)  # Additional wait to ensure all elements are loaded
#         await expect(page.get_by_role("heading", name="General In Person")).to_be_visible()
#         element = await page.query_selector('h4:has-text("General In Person")')
#         element_content = await element.inner_html() if element else "Element not found"
#         print(element_content)
#         # await expect(page.get_by_role("heading", name="General In Person")).to_be_visible()
#         # content = await page.content()
#         # print(content)
#         await browser.close()

# asyncio.run(fetch_page_content())

import asyncio
from playwright.async_api import async_playwright, expect
import logging

async def fetch_page_content():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto('https://ghc.anitab.org/pricing')
            await page.wait_for_load_state('networkidle')  # Wait for network to be idle
            await asyncio.sleep(5)  # Additional wait to ensure all elements are loaded
            await expect(page.get_by_role("heading", name="Academic In Person")).to_be_visible()
            element = await page.query_selector('h4:has-text("Academic In Person")')
            if element:
                # Get the parent div of the element to check for "SOLD OUT"
                parent_div = await element.evaluate_handle('element => element.closest(".pricing")')
                if parent_div:
                    sold_out_element = await parent_div.query_selector('p:has-text("SOLD OUT")')
                    if sold_out_element:
                        logging.info("The Academic In Person ticket is SOLD OUT.")
                        return False
                    else:
                        register_element = await parent_div.query_selector('a.btn')
                        if register_element:
                            logging.info("The Academic In Person ticket is available for registration.")
                            return True
                        else:
                            error_str = "Element 'SOLD OUT' or 'Register' is not found"
                            logging.info(error_str)
                            return error_str
            else:
                error_str = "Element 'Academic In Person' not found"
                logging.error(error_str)
                return error_str                
        except Exception as e:
            logging.error(f"Error during fetch_page_content: {str(e)}")
            return f"Error: {str(e)}"
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_page_content())