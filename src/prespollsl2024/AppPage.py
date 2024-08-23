import os
import tempfile
import time
import urllib.parse

from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip, afx
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import Log

log = Log("AppPage")


class AppPage:
    URL = "http://localhost:3000/prespollsl2024"
    T_SLEEP_START = 10
    T_SLEEP_NEW = 2

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
    def year(self):
        return self.date[:4]

    @property
    def id(self):
        return (
            f"{self.election_type}-{self.year}-{self.n_results_display:03d}"
        )

    @staticmethod
    def start_driver():
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Firefox(options=firefox_options)
        driver.set_window_size(1600, 1200)
        log.debug(f"🌏 Opening {AppPage.URL}...")
        driver.get(AppPage.URL)
        log.debug(f'😴 Sleeping for {AppPage.T_SLEEP_START}s...')
        time.sleep(AppPage.T_SLEEP_START)
        return driver

    @property
    def image_dir(self):
        image_dir = os.path.join(tempfile.gettempdir(), f'election-{self.date}')
        os.makedirs(image_dir, exist_ok=True)
        os.startfile(image_dir)
        return image_dir

    def download_screenshot(self, driver=None):
        image_path = os.path.join(self.image_dir, f"{self.id}.png")
        if os.path.exists(image_path):
            log.warn(f"Skipping {image_path}")
            return image_path, driver

        if not driver:
            driver = AppPage.start_driver()

        log.debug(f"🌏 Opening {self.url}...")
        driver.get(self.url)
        time.sleep(AppPage.T_SLEEP_NEW)
        log.debug(f'😴 Sleeping for {AppPage.T_SLEEP_NEW}s...')

        pre_image_path = os.path.join(self.image_dir, f"pre-{self.id}.png")
        driver.save_screenshot(pre_image_path)

        img = Image.open(pre_image_path)
        width = 1600
        height = 850
        img = img.crop((0, 0, width, height))
        img.save(image_path)

        log.info(f"Wrote screenshot to {image_path}")
        return image_path, driver

    @staticmethod
    def download_screenshots(
        election_type: str,
        date: str,
        start_n_results_display: int,
        end_n_results_display: int,
    ):
        driver = None
        image_paths = []
        for n_results_display in range(
            start_n_results_display, end_n_results_display + 1
        ):
            app_page = AppPage(
                election_type=election_type,
                date=date,
                n_results_display=n_results_display,
            )
            image_path, driver = app_page.download_screenshot(driver)
            image_paths.append(image_path)

        if driver:
            driver.quit()
            log.debug('🛑 Quitting driver.')

        n_image_paths = len(image_paths)
        log.info(f"Downloaded {n_image_paths} screenshots.")

        return image_paths

    @staticmethod
    def make_video(
        election_type: str,
        date: str,
        start_n_results_display: int,
        end_n_results_display: int,
    ):
        image_paths = AppPage.download_screenshots(
            election_type=election_type,
            date=date,
            start_n_results_display=start_n_results_display,
            end_n_results_display=end_n_results_display,
        )
        year = date[:4]
        video_path = os.path.join(
            "media", "video", f"{election_type}-{year}.mp4"
        )

        image_clips = []
        n = len(image_paths)
        start = 0
        DURATION_START = 5
        DURATION_NORMAL = 2
        DURATION_END = 20
        for i, image_path in enumerate(image_paths, start=1):
            duration = DURATION_NORMAL
            if i == 1:
                duration = DURATION_START
            elif i == n:
                duration = DURATION_END

            image_clip = (
                ImageClip(image_path).set_duration(duration).set_start(start)
            )
            image_clips.append(image_clip)
            start += duration

        audio_path = os.path.join("media", "audio", "bensound-newfrontier.mp3")
        audio_clip = AudioFileClip(audio_path)
        audio_clip = afx.audio_loop(audio_clip, duration=start).audio_fadeout(
            DURATION_END
        )

        video_clip = CompositeVideoClip(image_clips).set_audio(audio_clip)
        video_clip.write_videofile(video_path, fps=1)
        log.info(f'Wrote video to {video_path}')
