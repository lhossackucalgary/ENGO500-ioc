"""
Main update file for simulator
Just initialized logger, calls update_crews() and update_robots()
"""
import logging
import os
from update_crews import update_crews
from update_robots import update_robots


def main():
    """
    Update crew and robot simulated information
    """
    try:
        update_crews()
        logging.info("Crews update complete.")
    except:
        logging.except("Crews update failed.")

    try:
        update_robots()
        logging.info("Robots updated complete.")
    except:
        logging.except("Robots update failed.")


if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/sim.log', filemode='a', level=logging.DEBUG,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Simulator started")
    main()
    logging.info("Simulator ended")
