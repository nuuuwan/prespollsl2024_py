from prespollsl2024.app import AppPage

if __name__ == "__main__":
    AppPage.make_video(
        election_type="Parliamentary",
        date="2020-08-05",
        start_n_results_display=1,
        end_n_results_display=182,
    )

