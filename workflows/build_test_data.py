import os

from prespollsl2024 import ECData, TestData


def main():
    ec_data_list = TestData().build()
    ECData.store_list_to_dir(
        ec_data_list, os.path.join('data', 'fake', 'test')
    )


if __name__ == "__main__":
    main()
