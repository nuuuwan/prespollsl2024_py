import os
from prespollsl2024.app import AppPage
from utils import Log

log = Log('build_tweet')

def main():
    election_type='presidential'
    date='2019-11-16'
    start_n_results_display = 100
    end_n_results_display = 100

    driver = None
    app_page = None
    for n_results_display in range(start_n_results_display, end_n_results_display + 1):
        app_page = AppPage(election_type, date, n_results_display, driver)
        app_page.tweet()
        driver = app_page.driver


if __name__ == "__main__":
    main()