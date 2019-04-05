import subprocess
import time
import os

# OPTIONS:
pylib = "/usr/local/bin/python3"

def loop(counter):
    if counter % 2 == 0:
        print("starting monitor")
        os.chdir(os.sep.join([".", "monitor"]))
        subprocess.run([pylib, os.sep.join([".", "monitor.py"])])
        os.chdir("..")
        print("starting route_algo12")
        os.chdir(os.sep.join([".", "route"]))
        subprocess.run([pylib, os.sep.join([".", "route_algo12.py"])])
        os.chdir("..")
    print("starting sim_main")
    os.chdir(os.sep.join([".", "sim"]))
    subprocess.run([pylib, os.sep.join([".", "sim_main.py"])])
    os.chdir("..")


def main():

    os.chdir(os.sep.join([".", "sim"]))
    #subprocess.run([pylib, os.sep.join([".", "del_sim.py"])])
    #print("starting init_sim")
    #subprocess.run([pylib, os.sep.join([".", "init_sim.py"])])
    print("starting sim_main")
    subprocess.run([pylib, os.sep.join([".", "sim_main.py"])])
    os.chdir("..")
    ctr = 0
    while True:
        loop(ctr)
        ctr = ctr + 1
        print("Loop completed. Pausing execution..")
        time.sleep(30)

if __name__ == '__main__':
    main()
