import time

from pycomm3 import LogixDriver

from Communication.PLC import PLC
from Communication.PLCConfig import TRAFFIC_PLC_IP_ADDRESS
from MachineLearning.ModelTrainer import ModelTrainerFactory
from NetworkManager import NetworkManager

def main():
    network = NetworkManager()
    network.start()
    #only_train_model()
    #plc_comm()

def only_train_model():
    model_trainer = ModelTrainerFactory(1)
    model_trainer.train_test_model()

def plc_test():
    while True:
        with LogixDriver(TRAFFIC_PLC_IP_ADDRESS) as plc:
            plc.open()
            plc.write("MXP_DATA[5]", 1)
            print(plc.read("MXP_DATA[5]"))
def plc_comm():
    plc = PLC(TRAFFIC_PLC_IP_ADDRESS)
    plc.connect()
    iter = 1
    val = plc.read_tag("MON_X_EV.CURRENT_PHASE")
    print(f"Read{iter}: {val}")
    iter += 1
    while True:
        for i in range (0, 6):
            plc.write_tag("MXP_DATA[5]", i)
            print("Wrote: 1 to MPX_DATA{5}")
            time.sleep(10)

if __name__ == "__main__":
    main()