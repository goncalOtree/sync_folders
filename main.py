from sync import sync
import logging
import argparse
import time

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Synchronize two folders at a specified interval."
    )

    parser.add_argument(
        "source_folder",
        type=str,
        help="The path to the source folder.",
    )
    parser.add_argument(
        "replica_folder",
        type=str,
        help="The path to the replica folder.",
    )
    parser.add_argument(
        "log_file",
        type=str,
        help="The name of the log file.",
    )
    parser.add_argument(
        "--i",
        type=int,
        dest='interval',
        default=5,
        help="The time interval (in seconds) between synchronizations. Defaults to 60.",
    )

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()

    
    if args.interval <= 0:
        raise ValueError("Interval must be a positive integer.")
    
    logging.basicConfig(filename=args.log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)


    while(True):
        sync(args.source_folder,args.replica_folder,logger)
        time.sleep(args.interval)