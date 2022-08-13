import os
from time import sleep

from epsolar_tracer.client import EPsolarTracerClient
from epsolar_tracer.enums.RegisterTypeEnum import RegisterTypeEnum

relevant_registers = {
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_VOLTAGE,
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_CURRENT,
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_POWER,
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_VOLTAGE,
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_CURRENT,
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_POWER,
    RegisterTypeEnum.CHARGING_MODE,
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_VOLTAGE,
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_CURRENT,
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_POWER,
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_VOLTAGE,
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_CURRENT,
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_POWER,
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_VOLTAGE,
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_CURRENT,
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_POWER,
    RegisterTypeEnum.TEMPERATURE_INSIDE_EQUIPMENT,
    RegisterTypeEnum.POWER_COMPONENTS_TEMPERATURE,
    RegisterTypeEnum.BATTERY_SOC,
    RegisterTypeEnum.BATTERYS_REAL_RATED_POWER,
    RegisterTypeEnum.BATTERY_STATUS,
    RegisterTypeEnum.CHARGING_EQUIPMENT_STATUS,
    RegisterTypeEnum.MAXIMUM_INPUT_VOLT_PV_TODAY,
    RegisterTypeEnum.MINIMUM_INPUT_VOLT_PV_TODAY,
    RegisterTypeEnum.MAXIMUM_BATTERY_VOLT_TODAY,
    RegisterTypeEnum.MINIMUM_BATTERY_VOLT_TODAY,
    RegisterTypeEnum.CONSUMED_ENERGY_TODAY,
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_MONTH,
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_YEAR,
    RegisterTypeEnum.TOTAL_CONSUMED_ENERGY,
    RegisterTypeEnum.GENERATED_ENERGY_TODAY,
    RegisterTypeEnum.GENERATED_ENERGY_THIS_MONTH,
    RegisterTypeEnum.GENERATED_ENERGY_THIS_YEAR,
    RegisterTypeEnum.TOTAL_GENERATED_ENERGY,
    RegisterTypeEnum.CARBON_DIOXIDE_REDUCTION,
    RegisterTypeEnum.BATTERY_CURRENT,
}

EPSOLAR_TTY_PORT = os.environ.get("EPSOLAR_TTY_PORT", "/dev/ttyUSB0")

ep_solar_client = EPsolarTracerClient(port=EPSOLAR_TTY_PORT)


def read_all():
    results = []
    for reg in relevant_registers:
        result = ep_solar_client.read_input(reg)
        results.append((reg, result))
    return results


def read_ep_solar():

    message = {}
    message["name"] = "ep_solar"

    message["pv"] = {}
    message["pv"]["u"] = ep_solar_client.read_input(RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_VOLTAGE).value
    message["pv"]["i"] = ep_solar_client.read_input(RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_CURRENT).value
    message["pv"]["p"] = ep_solar_client.read_input(RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_POWER).value

    message["battery"] = {}
    message["battery"]["u"] = ep_solar_client.read_input(RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_VOLTAGE).value
    message["battery"]["i"] = ep_solar_client.read_input(RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_CURRENT).value
    message["battery"]["p"] = ep_solar_client.read_input(RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_POWER).value
    message["battery"]["soc"] = ep_solar_client.read_input(RegisterTypeEnum.BATTERY_SOC).value

    message["load"] = {}
    message["load"]["u"] = ep_solar_client.read_input(RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_VOLTAGE).value
    message["load"]["i"] = ep_solar_client.read_input(RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_CURRENT).value
    message["load"]["p"] = ep_solar_client.read_input(RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_POWER).value

    return message


def ep_solar_connect():
    if ep_solar_client.connect():
        print(f"EPsolar connected to {EPSOLAR_TTY_PORT}")
        return True
    else:
        print(f"Error connecting to {EPSOLAR_TTY_PORT}")
        sleep(1)
        return False
