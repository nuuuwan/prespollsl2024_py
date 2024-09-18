import os
from prespollsl2024 import ECData


def main():
    ec_data_list =  ECData.list_from_test()
    ECData.build_tsv(ec_data_list, os.path.join('data', 'derived', 'test-2024.tsv'))


if __name__ == "__main__":
    main()
