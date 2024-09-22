from prespollsl2024.app import AppPage

if __name__ == "__main__":
    AppPage.make_video(
        election_type="Presidential",
        # date="2019-11-16",
        # date="2015-01-08",
        # date="2005-11-17",
        date="2024-09-21",
        start_n_results_display=1,
        end_n_results_display=182,
    )
'''
I've been working on a simple app to show #PresPollSL2024 results in realtime.

Here's the MVP https://nuuuwan.github.io/prespoll

I'm not going to explain how to use it, because it should be self-explanatory.

Comment on what to add/delete/update, and any other feedback.

Also, (obviously) the data for 2024 is test data, and fake.
'''
