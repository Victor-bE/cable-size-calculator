
import streamlit as st
import math

# Cable data for copper (approximate resistance in ohm/meter)
copper_resistance = {
    1.5: 0.0121,
    2.5: 0.00741,
    4: 0.00461,
    6: 0.00308,
    10: 0.00183,
    16: 0.00115,
    25: 0.000727,
    35: 0.000524,
    50: 0.000387,
    70: 0.000268,
    95: 0.000193,
    120: 0.000153,
    150: 0.000124,
    185: 0.0000991,
    240: 0.0000754
}

# Current carrying capacity (simplified, conservative estimates in amperes)
cable_capacity = {
    1.5: 14,
    2.5: 20,
    4: 26,
    6: 34,
    10: 46,
    16: 61,
    25: 83,
    35: 105,
    50: 130,
    70: 165,
    95: 200,
    120: 230,
    150: 265,
    185: 300,
    240: 360
}

def calculate_current(power_kva, voltage, phase):
    power_w = power_kva * 1000
    if phase == 'Three Phase':
        current = power_w / (math.sqrt(3) * voltage)
    else:
        current = power_w / voltage
    return current

def calculate_voltage_drop(current, resistance, length, phase):
    total_length = length * 2
    if phase == 'Three Phase':
        return math.sqrt(3) * current * resistance * total_length
    else:
        return current * resistance * total_length

st.title("Copper Cable Size Calculator")

voltage = st.number_input("Voltage (V)", value=415)
phase = st.selectbox("Phase", ['Three Phase', 'Single Phase'])
length = st.number_input("Cable Length (meters, one-way)", value=50)
power = st.number_input("Load Power (kVA)", value=50.0)

if st.button("Calculate Cable Size"):
    current = calculate_current(power, voltage, phase)
    st.write(f"Calculated Current: {current:.2f} A")

    suitable_sizes = []
    for size, resistance in copper_resistance.items():
        volt_drop = calculate_voltage_drop(current, resistance, length, phase)
        volt_drop_percent = (volt_drop / voltage) * 100
        if current <= cable_capacity[size] and volt_drop_percent <= 5:
            suitable_sizes.append((size, cable_capacity[size], volt_drop, volt_drop_percent))

    if suitable_sizes:
        st.success("Suitable Cable Sizes:")
        for size, capacity, vdrop, vdrop_percent in suitable_sizes:
            st.write(f"{size} mm^2 - Rated {capacity} A - Voltage Drop: {vdrop:.2f} V ({vdrop_percent:.2f}%)")
    else:
        st.error("No suitable cable size found. Try reducing length or power.")
