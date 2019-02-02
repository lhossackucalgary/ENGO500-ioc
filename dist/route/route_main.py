import logging
import os

def main():
    pass

if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/route.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Router started")
    main()
    logging.info("Router ended")
