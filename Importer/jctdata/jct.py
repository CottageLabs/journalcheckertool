from datetime import datetime
from jctdata.jac import jac_index_data
from jctdata.iac import iac_index_data
from jctdata.lib.strfdelta import strfdelta


def gather_index_data():
    dt0 = datetime.utcnow()
    jac_index_data()
    dt1 = datetime.utcnow()
    iac_index_data()
    dt2 = datetime.utcnow()
    jac_delta = dt1 - dt0
    iac_delta = dt2 - dt1
    total_delta = dt2 - dt0
    print("Started at: {dt}".format(dt=dt0))
    print("completed at: {dt}".format(dt=dt2))
    print("Time taken for jac data: {d}".format(d=strfdelta(jac_delta, "%D days %H:%M:%S")))
    print("Time taken for 1ac data: {d}".format(d=strfdelta(iac_delta, "%D days %H:%M:%S")))
    print("Time taken for all data: {d}".format(d=strfdelta(total_delta, "%D days %H:%M:%S")))


if __name__ == "__main__":
    print(datetime.utcnow())
    gather_index_data()
    print(datetime.utcnow())