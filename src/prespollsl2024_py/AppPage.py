import os
import urllib.parse

from selenium import webdriver

from selenium.webdriver.firefox.options import Options


from utils import Log
import time

log = Log("AppPage")


class AppPage:
    URL = "https://nuuuwan.github.io/prespollsl2024"
    T_SLEEP_START = 20
    T_SLEEP_NEW = 1

    def __init__(
        self,
        election_type: str,
        date: str,
        n_results_display: str,
    ):
        self.election_type = election_type
        self.date = date
        self.n_results_display = n_results_display

    @property
    def url(self):
        return (
            AppPage.URL
            + "?"
            + urllib.parse.urlencode(
                dict(
                    election_type=self.election_type,
                    date=self.date,
                    nResultsDisplay=self.n_results_display,
                )
            )
        )

    @property
    def id(self):
        return (
            f"[{self.election_type}-{self.date}] {self.n_results_display:03d}"
        )

    @staticmethod
    def start_driver():
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Firefox(options=firefox_options)
        driver.set_window_size(1600, 900)
        log.debug(f"🌏 Opening {AppPage.URL}...")
        driver.get(AppPage.URL)
        log.debug(f'😴 Sleeping for {AppPage.T_SLEEP_START}s...')
        time.sleep(AppPage.T_SLEEP_START)
        return driver

    def download_screenshot(self, driver=None):
        did_create_driver = False
        if not driver:
            did_create_driver = True
            driver = AppPage.start_driver()

        log.debug(f"🌏 Opening {self.url}...")
        driver.get(self.url)
        time.sleep(AppPage.T_SLEEP_NEW)
        log.debug(f'😴 Sleeping for {AppPage.T_SLEEP_NEW}s...')
        image_path = os.path.join("images", f"{self.id}.png")
        driver.save_screenshot(image_path)
        if did_create_driver:
            driver.quit()
        log.info(f"Wrote screenshot to {image_path}")
        return image_path

    @staticmethod
    def download_screenshots(
        election_type: str,
        date: str,
        start_n_results_display: int,
        end_n_results_display: int,
    ):
        driver = AppPage.start_driver()
        for n_results_display in range(
            start_n_results_display, end_n_results_display + 1
        ):
            app_page = AppPage(
                election_type=election_type,
                date=date,
                n_results_display=n_results_display,
            )
            app_page.download_screenshot(driver)
        driver.quit()
        log.debug('🛑 Quitting driver.')


if __name__ == "__main__":
    AppPage.download_screenshots(
        election_type="presidential",
        date="2019-11-16",
        start_n_results_display=100,
        end_n_results_display=103,
    )
