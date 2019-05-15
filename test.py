import unittest
import pandas as pd
import requests
import json
from services.utilities import utils_func
from copy import deepcopy


class MyTest(unittest.TestCase):
    def test_unit_breakdown(self):
        data = pd.read_csv("csv/initial_data.csv")

        gr = data.GR.values
        tvd = data.TVD.values

        data = {
            "GR": list(gr),
            "TVD": list(tvd)
        }

        headers = {'content-type': 'application/json'}
        url = 'http://127.0.0.1:9999/api/v1/unit-breakdown'

        res = requests.post(url, data=json.dumps(data), headers=headers)

        data = json.loads(res.text)

        df = pd.DataFrame(data["content"], columns=["Boundary_flag"])
        df.to_csv("./csv/debug_ub.csv", index=False)

        print(data)

    def test_expert_rule(self):
        data = pd.read_csv("csv/initial_data.csv")

        dct = {}

        for key, value in data.items():
            dct.update({key: list(value)})

        headers = {'content-type': 'application/json'}
        url = 'http://0.0.0.0:9999/api/v1/expert-rule'

        res = requests.post(url, data=json.dumps(dct), headers=headers)

        data = json.loads(res.text)

        data = data["content"]

        tmp = []
        for i in range(len(data["Uncertainty_flag"])):
            t = {}
            for key in data.keys():
                t.update({key: data[key][i]})

            tmp.append(deepcopy(t))

        utils_func.export_to_csv(tmp, "csv/T2X.csv")
        # df.to_csv("csv/T2X-df.csv", index=False)

        # print(data)

        # if data["success"]:
        #     headers = list(data["payload"][0].keys())
        #     print(data["payload"][0])
