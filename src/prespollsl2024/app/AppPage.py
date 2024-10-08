import json
import os
import tempfile
import time
import urllib.parse

from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip, afx
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from twtr import Tweet, Twitter
from utils import JSONFile, Log, File

log = Log("AppPage")


HEIGHT = 1000
ASPECT_RATIO = 16 / 9
WIDTH = int(HEIGHT * ASPECT_RATIO)


def add_padding(image_path, output_path, padding=15):
    img = Image.open(image_path)
    width, height = img.size

    new_width = width + 2 * padding
    new_height = height + 2 * padding
    aspect_ratio_actual = new_width / new_height
    if aspect_ratio_actual < ASPECT_RATIO:
        new_width = int(new_height * ASPECT_RATIO)
    elif aspect_ratio_actual > ASPECT_RATIO:
        new_height = int(new_width / ASPECT_RATIO)

    padding_x = (new_width - width) // 2
    padding_y = (new_height - height) // 2

    new_img = Image.new("RGB", (new_width, new_height), "white")
    new_img.paste(img, (padding_x, padding_y))
    new_img.save(output_path)


class AppPage:
    # URL = "https://nuuuwan.github.io/election"
    URL = "http://localhost:3000/election"
    T_SLEEP_START = 20
    T_SLEEP_NEW = 3

    def __init__(
        self,
        election_type: str,
        date: str,
        n_results_display: str,
        driver: webdriver.Firefox = None,
    ):
        self.election_type = election_type
        self.date = date
        self.n_results_display = n_results_display
        self.driver = driver

    @property
    def url(self):
        return (
            AppPage.URL
            + "?"
            + urllib.parse.urlencode(
                dict(
                    electionType=self.election_type,
                    date=self.date,
                    nResultsDisplay=self.n_results_display,
                    lang="en",
                )
            )
        )

    @property
    def year(self):
        return self.date[:4]

    @property
    def id(self):
        return f"{self.n_results_display:03d}"

    @staticmethod
    def start_driver():
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Firefox(options=firefox_options)
        driver.set_window_size(WIDTH, HEIGHT)
        log.debug(f"🌏 Opening \"{AppPage.URL}\"...")
        driver.get(AppPage.URL)
        log.debug(f'😴 Sleeping for {AppPage.T_SLEEP_START}s...')
        time.sleep(AppPage.T_SLEEP_START)
        return driver

    @property
    def image_dir(self):
        image_dir = os.path.join(
            tempfile.gettempdir(), f'election-{self.date}', 'images'
        )
        os.makedirs(image_dir, exist_ok=True)
        return image_dir

    @property
    def hidden_data_dir(self):
        hidden_data_dir = os.path.join(
            tempfile.gettempdir(), f'election-{self.date}', 'hidden_data'
        )
        os.makedirs(hidden_data_dir, exist_ok=True)
        return hidden_data_dir

    def open_page(self):
        if not self.driver:
            self.driver = AppPage.start_driver()

        log.debug(f"🌏 Opening \"{self.url}\"...")
        self.driver.get(self.url)
        time.sleep(AppPage.T_SLEEP_NEW)
        log.debug(f'😴 Sleeping for {AppPage.T_SLEEP_NEW}s...')

        current_url = self.driver.current_url
        log.debug(f'{current_url=}')
        if self.url not in current_url:
            raise Exception(f"Expected {self.url} not in {current_url}")

    @property
    def image_path(self):
        return os.path.join(self.image_dir, f"{self.id}.png")

    def is_image_exists(self):
        return os.path.exists(self.image_path)

    def download_screenshot(self):
        image_path = self.image_path
        self.driver.save_screenshot(image_path)

        add_padding(image_path, image_path, padding=40)

        image_size_k = os.path.getsize(image_path) / 1_000
        log.info(f"Wrote screenshot to {image_path} ({image_size_k:.1f}KB)")

        return image_path

    def is_hidden_data_exists(self):
        hidden_data_path = os.path.join(
            self.hidden_data_dir, f"{self.id}.json"
        )
        return os.path.exists(hidden_data_path)

    def download_hidden_data(self):
        hidden_data_path = os.path.join(
            self.hidden_data_dir, f"{self.id}.json"
        )

        div_hidden_data = self.driver.find_element(
            By.ID, "prespoll_hidden_data"
        )
        hidden_data_json = div_hidden_data.get_attribute("innerHTML")
        hidden_data = json.loads(hidden_data_json)
        log.debug(f'{hidden_data=}')

        JSONFile(hidden_data_path).write(hidden_data)
        log.info(f'Wrote {hidden_data_path}')

        text_path = hidden_data_path + '.txt'
        File(text_path).write(hidden_data['tweet'])
        log.info(f'Wrote {text_path}')
        return hidden_data

    def tweet(self):
        self.open_page()
        image_path = self.download_screenshot()
        hidden_data = self.download_hidden_data()
        tweet_text = hidden_data['tweet']
        try:
            twitter = Twitter()
            tweet = Tweet(tweet_text).add_image(image_path)
            tweet_id = twitter.send(tweet)
            log.debug(f'{tweet_id=}')
            os.startfile('https://x.com/lk_elections')
        except Exception as e:
            log.error('Could not tweet: ' + str(e))

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
                driver=driver,
            )

            image_path = app_page.image_path
            if not app_page.is_image_exists():
                app_page.open_page()
                app_page.download_screenshot()
                driver = app_page.driver
            image_paths.append(image_path)
                

        if driver:
            driver.quit()
            log.debug('🛑 Quitting driver.')

        n_image_paths = len(image_paths)
        log.info(f"Downloaded {n_image_paths} screenshots.")

        return image_paths

    @staticmethod
    def compile_image_clips(
        image_paths,
        duration_start,
        duration_normal,
        duration_end,
        total_duration,
    ):
        image_clips = []
        n = len(image_paths)

        for i, image_path in enumerate(image_paths, start=1):
            duration = duration_normal
            if i == 1:
                duration = duration_start
            elif i == n:
                duration = duration_end

            image_clip = (
                ImageClip(image_path)
                .set_duration(duration)
                .set_start(total_duration)
            )
            image_clips.append(image_clip)
            total_duration += duration
        return image_clips, total_duration

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

        image_clips, total_duration = AppPage.compile_image_clips(
            image_paths,
            duration_start=5,
            duration_normal=0.5,
            duration_end=20,
            total_duration=0,
        )



        audio_path = os.path.join(
            "media", "audio", "bensound-onrepeat.mp3"
        )
        audio_clip = AudioFileClip(audio_path)
        audio_clip = afx.audio_loop(
            audio_clip, duration=total_duration
        ).audio_fadeout(20)

        video_clip = CompositeVideoClip(image_clips).set_audio(audio_clip)
        video_clip.write_videofile(video_path, fps=4)
        log.info(f'Wrote video to {video_path}')
        os.startfile(video_path)
