"""Main file that will run the ETL process and output the data visualization."""

import sys
sys.path.append(".")

from common import etl_runner, data_viz_runner

def main():
    etl_runner.etl_main()
    data_viz_runner.data_viz_main()
    
if __name__ == '__main__':
    main()