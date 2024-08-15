from prespollsl2024 import AppPage

if __name__ == "__main__":
    AppPage.make_video(
        election_type="presidential",
        date="2019-11-16",
        start_n_results_display=0,
        end_n_results_display=182,
    )
