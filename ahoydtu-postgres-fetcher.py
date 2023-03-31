#!/usr/bin/env python3

import requests
import psycopg

# config
url = "https://example.com/"
basicauth = ('username', 'password')
conn = psycopg.connect(host="localhost", dbname="...", user="...", autocommit=True)

class AC:
    def __init__(
        self, voltage: float, current: float, power: float, frequency: float,
        power_factor: float, temperature: float, yield_total: float, yield_day: float,
        power_dc: float, efficiency: float, reactive_power: float,
        power_limit: float,
     ):
        self.voltage = voltage
        self.current = current
        self.power = power
        self.frequency = frequency
        self.power_factor = power_factor
        self.temperature = temperature
        self.yield_total = yield_total
        self.yield_day = yield_day
        self.power_dc = power_dc
        self.efficiency = efficiency
        self.reactive_power = reactive_power
        self.power_limit = power_limit

class Module:
    def __init__(
            self, voltage: float, current: float, power: float,
            yield_day: float, yield_total: float, irradiation: float,
    ) -> None:
        self.voltage = voltage
        self.current = current
        self.power = power
        self.yield_day = yield_day
        self.yield_total = yield_total
        self.irradiation = irradiation

class Data:
    def __init__(self, timestamp: int, ac: AC, a: Module, b: Module) -> None:
        self.timestamp = timestamp
        self.ac = ac
        self.a = a
        self.b = b

def fetch() -> Data:
    r = requests.get(url + '/api/live', auth = basicauth)
    json = r.json()
    # check json format
    assert json["menu"]
    assert json["generic"]
    assert json["inverter"]
    assert json["inverter"][0]
    assert json["inverter"][0]["ch_names"]
    assert json["inverter"][0]["ch_names"][0] == "AC"
    assert json["ch0_fld_units"]
    assert json["ch0_fld_units"][0] == "V"
    assert json["ch0_fld_units"][1] == "A"
    assert json["ch0_fld_units"][2] == "W"
    assert json["ch0_fld_units"][3] == "Hz"
    assert json["ch0_fld_units"][4] == ""
    assert json["ch0_fld_units"][5] == "°C"
    assert json["ch0_fld_units"][6] == "kWh"
    assert json["ch0_fld_units"][7] == "Wh"
    assert json["ch0_fld_units"][8] == "W"
    assert json["ch0_fld_units"][9] == "%"
    assert json["ch0_fld_units"][10] == "var"
    assert json["ch0_fld_names"]
    assert json["ch0_fld_names"][0] == "U_AC"
    assert json["ch0_fld_names"][1] == "I_AC"
    assert json["ch0_fld_names"][2] == "P_AC"
    assert json["ch0_fld_names"][3] == "F_AC"
    assert json["ch0_fld_names"][4] == "PF_AC"
    assert json["ch0_fld_names"][5] == "Temp"
    assert json["ch0_fld_names"][6] == "YieldTotal"
    assert json["ch0_fld_names"][7] == "YieldDay"
    assert json["ch0_fld_names"][8] == "P_DC"
    assert json["ch0_fld_names"][9] == "Efficiency"
    assert json["ch0_fld_names"][10] == "Q_AC"
    assert json["fld_units"]
    assert json["fld_units"][0] == "V"
    assert json["fld_units"][1] == "A"
    assert json["fld_units"][2] == "W"
    assert json["fld_units"][3] == "Wh"
    assert json["fld_units"][4] == "kWh"
    assert json["fld_units"][5] == "%"
    assert json["fld_names"]
    assert json["fld_names"][0] == "U_DC"
    assert json["fld_names"][1] == "I_DC"
    assert json["fld_names"][2] == "P_DC"
    assert json["fld_names"][3] == "YieldDay"
    assert json["fld_names"][4] == "YieldTotal"
    assert json["fld_names"][5] == "Irradiation"
    ac = json["inverter"][0]["ch"][0]
    a = json["inverter"][0]["ch"][1]
    b = json["inverter"][0]["ch"][2]
    ac = AC(
        voltage = ac[0],
        current = ac[1],
        power = ac[2],
        frequency = ac[3],
        power_factor = ac[4],
        temperature = ac[5],
        yield_total = ac[6],
        yield_day = ac[7],
        power_dc = ac[8],
        efficiency = ac[9],
        reactive_power = ac[10],
        power_limit = json["inverter"][0]["power_limit_read"],
    )
    a = Module(
        voltage = a[0],
        current = a[1],
        power = a[2],
        yield_day = a[3],
        yield_total = a[4],
        irradiation = a[5],
    )
    b = Module(
        voltage = b[0],
        current = b[1],
        power = b[2],
        yield_day = b[3],
        yield_total = b[4],
        irradiation = b[5],
    )
    timestamp = json["inverter"][0]["ts_last_success"]
    return Data(timestamp, ac, a, b)

def store(data: Data) -> None:
    cur = conn.cursor()
    cur.execute("""INSERT INTO measurements (
        timestamp, ac_voltage, ac_current, ac_power, ac_frequency,
        ac_power_factor, ac_temperature, ac_yield_total, ac_yield_day,
        ac_power_dc, ac_efficiency, ac_reactive_power, ac_power_limit,
        a_voltage, a_current, a_power, a_yield_day, a_yield_total, a_irradiation,
        b_voltage, b_current, b_power, b_yield_day, b_yield_total, b_irradiation
    ) VALUES (
        to_timestamp(%s), %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    ) ON CONFLICT DO NOTHING""", (
        data.timestamp, data.ac.voltage, data.ac.current, data.ac.power, data.ac.frequency,
        data.ac.power_factor, data.ac.temperature, data.ac.yield_total, data.ac.yield_day,
        data.ac.power_dc, data.ac.efficiency, data.ac.reactive_power, data.ac.power_limit,
        data.a.voltage, data.a.current, data.a.power, data.a.yield_day, data.a.yield_total, data.a.irradiation,
        data.b.voltage, data.b.current, data.b.power, data.b.yield_day, data.b.yield_total, data.b.irradiation,
    ))

def main() -> None:
    data = fetch()
    store(data)

if __name__ == "__main__":
    main()

