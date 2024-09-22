from utils import Log

from prespollsl2024.app import AppPage

log = Log('build_tweet')


def main():
    election_type = 'Presidential'
    date = '2024-09-21'
    start_n_results_display = 29
    end_n_results_display = 29

    driver = None
    app_page = None
    for n_results_display in range(
        start_n_results_display, end_n_results_display + 1
    ):
        app_page = AppPage(election_type, date, n_results_display, driver)
        app_page.tweet()
        driver = app_page.driver


if __name__ == "__main__":
    main()
