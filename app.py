
import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Self-Healing DC Microgrid",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 31px;
    font-weight: 800;
    color: #19C6A7;
    margin-bottom: 0;
}
.sub-title {
    font-size: 15px;
    color: #AAB8C5;
    margin-top: 4px;
}
.section-title {
    font-size: 21px;
    font-weight: 700;
    margin-top: 15px;
}
div[data-testid="stMetric"] {
    background-color: rgba(100, 130, 150, 0.10);
    border: 1px solid rgba(150, 170, 190, 0.25);
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "event_log" not in st.session_state:
    st.session_state.event_log = [
        {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Event": "Simulation initialized",
            "Action": "Monitoring started",
            "Status": "NORMAL"
        }
    ]

if "last_state" not in st.session_state:
    st.session_state.last_state = None

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">⚡ AUTONOMOUS SELF-HEALING DC MICROGRID</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Disaster-Resilient Communities | '
    'Smart Energy Management Simulation</div>',
    unsafe_allow_html=True
)
st.divider()

st.info(
    "SOFTWARE PROTOTYPE • Simulated sensors • Automated control logic • "
    "Priority-based power management"
)

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.title("⚙️ Simulation Control Panel")
st.sidebar.caption("Adjust the operating conditions")

solar_power = st.sidebar.slider(
    "Solar generation (W)", 0, 600, 350, step=25
)

battery_soc = st.sidebar.slider(
    "Battery state of charge (%)", 0, 100, 80, step=5
)

battery_max_power = st.sidebar.slider(
    "Maximum battery output (W)", 0, 400, 250, step=25
)

st.sidebar.subheader("Load Demand")

hospital_demand = st.sidebar.slider(
    "Hospital / medical load (W)", 50, 300, 150, step=10
)

pump_demand = st.sidebar.slider(
    "Water pump (W)", 0, 250, 100, step=10
)

lighting_demand = st.sidebar.slider(
    "Emergency lighting (W)", 0, 200, 80, step=10
)

st.sidebar.subheader("Fault Injection")

fault_type = st.sidebar.selectbox(
    "Choose a fault condition",
    [
        "No fault",
        "Solar source failure",
        "Hospital branch fault",
        "Water pump branch fault",
        "Lighting branch fault",
        "System overload"
    ]
)

st.sidebar.caption(
    "Faults are simulated inputs. No real electrical fault is generated."
)

# --------------------------------------------------
# MICROGRID MODEL
# --------------------------------------------------
nominal_voltage = 48.0

loads = [
    {
        "name": "Hospital / Medical",
        "demand": hospital_demand,
        "priority": 1
    },
    {
        "name": "Water Pump",
        "demand": pump_demand,
        "priority": 2
    },
    {
        "name": "Emergency Lighting",
        "demand": lighting_demand,
        "priority": 3
    }
]

total_demand = sum(load["demand"] for load in loads)

# Simulate source failure
if fault_type == "Solar source failure":
    effective_solar = 0
else:
    effective_solar = solar_power

# Simplified battery availability model.
# This is not an electrochemical battery model.
if battery_soc <= 0:
    battery_available = 0
elif battery_soc < 20:
    battery_available = battery_max_power * battery_soc / 20
else:
    battery_available = battery_max_power

# Use available solar first, then battery for the remaining demand.
solar_used = min(effective_solar, total_demand)
remaining_demand = max(0, total_demand - solar_used)
battery_used = min(battery_available, remaining_demand)

available_power = effective_solar + battery_available
dispatch_power = solar_used + battery_used

# Faulty branches are isolated in the conceptual model.
faulty_branches = {
    "Hospital branch fault": "Hospital / Medical",
    "Water pump branch fault": "Water Pump",
    "Lighting branch fault": "Emergency Lighting"
}

isolated_branch = faulty_branches.get(fault_type)

# A simplified overload condition is triggered when requested
# demand exceeds the configured solar plus battery capability.
overload_detected = (
    fault_type == "System overload"
    or total_demand > available_power
)

# --------------------------------------------------
# PRIORITY-BASED LOAD ALLOCATION
# --------------------------------------------------
remaining_power = dispatch_power
results = []

for load in loads:
    demand = load["demand"]
    name = load["name"]

    if name == isolated_branch:
        supplied = 0
        status = "ISOLATED"
    else:
        supplied = min(demand, remaining_power)
        remaining_power -= supplied

        if supplied >= demand:
            status = "SUPPLIED"
        elif supplied > 0:
            status = "PARTIAL"
        else:
            status = "UNSUPPLIED"

    results.append({
        "Load": name,
        "Priority": load["priority"],
        "Demand (W)": demand,
        "Supplied (W)": round(supplied, 1),
        "Unserved (W)": round(demand - supplied, 1),
        "Status": status
    })

total_supplied = sum(item["Supplied (W)"] for item in results)
unserved_power = max(0, total_demand - total_supplied)
current_estimate = total_supplied / nominal_voltage

if fault_type == "No fault" and unserved_power == 0:
    system_status = "NORMAL"
elif isolated_branch or fault_type == "Solar source failure":
    system_status = "FAULT RESPONSE"
else:
    system_status = "POWER LIMITED"

# --------------------------------------------------
# AUTOMATIC EVENT LOGGING
# --------------------------------------------------
current_state = (
    fault_type,
    solar_power,
    battery_soc,
    battery_max_power,
    hospital_demand,
    pump_demand,
    lighting_demand,
    system_status,
    total_supplied
)

if current_state != st.session_state.last_state:
    st.session_state.event_log.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Event": fault_type,
        "Action": (
            f"Solar {effective_solar} W; "
            f"power supplied {total_supplied:.0f} W"
        ),
        "Status": system_status
    })
    st.session_state.last_state = current_state

# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Live System Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Solar Available", f"{effective_solar:.0f} W")
c2.metric("Battery Power Used", f"{battery_used:.0f} W")
c3.metric("Total Load Demand", f"{total_demand:.0f} W")
c4.metric("Power Delivered", f"{total_supplied:.0f} W")

c5, c6, c7, c8 = st.columns(4)

c5.metric("Estimated DC Voltage", f"{nominal_voltage:.1f} V")
c6.metric("Estimated Load Current", f"{current_estimate:.2f} A")
c7.metric("Unserved Demand", f"{unserved_power:.0f} W")
c8.metric("Battery Charge", f"{battery_soc}%")

st.divider()

# --------------------------------------------------
# SYSTEM STATUS AND FAULT RESPONSE
# --------------------------------------------------
left, right = st.columns([1, 1])

with left:
    st.subheader("🛡️ System Health")

    if system_status == "NORMAL":
        st.success("NORMAL — All requested loads are supplied.")
    elif system_status == "FAULT RESPONSE":
        st.warning("FAULT RESPONSE — A source or branch fault is active.")
    else:
        st.error("POWER LIMITED — Available power is insufficient.")

    st.write(f"**Selected condition:** {fault_type}")

    if isolated_branch:
        st.warning(
            f"Controller action: isolate the {isolated_branch} branch."
        )
    elif fault_type == "Solar source failure":
        st.warning(
            "Solar source unavailable. Battery support is used "
            "subject to its configured power limit."
        )
    elif overload_detected:
        st.warning(
            "Demand exceeds available power or overload was injected. "
            "Loads are managed by priority."
        )
    else:
        st.write("No injected fault. Monitoring is active.")

with right:
    st.subheader("🔋 Energy Balance")

    energy_data = pd.DataFrame({
        "Category": [
            "Solar available",
            "Battery available",
            "Total demand",
            "Power delivered"
        ],
        "Power (W)": [
            effective_solar,
            battery_available,
            total_demand,
            total_supplied
        ]
    })

    st.bar_chart(
        energy_data.set_index("Category"),
        y="Power (W)"
    )

# --------------------------------------------------
# LOAD MANAGEMENT TABLE
# --------------------------------------------------
st.divider()
st.markdown(
    '<div class="section-title">🏥 Critical Load Management</div>',
    unsafe_allow_html=True
)

load_df = pd.DataFrame(results)
st.dataframe(load_df, use_container_width=True, hide_index=True)

st.caption(
    "Priority order: Hospital / Medical → Water Pump → Emergency Lighting. "
    "This order is a configurable demonstration assumption."
)

# --------------------------------------------------
# ARCHITECTURE
# --------------------------------------------------
st.divider()
st.markdown(
    '<div class="section-title">🔌 Microgrid Architecture</div>',
    unsafe_allow_html=True
)

st.markdown("""
```text
       SOLAR ENERGY SOURCE
                |
                v
          DC POWER BUS <------> BATTERY STORAGE
                |
                v
       SENSORS / MONITORING
                |
                v
       INTELLIGENT CONTROLLER
                |
         FAULT DETECTION
                |
        ISOLATION DECISION
                |
       PRIORITY-BASED CONTROL
                |
       +--------+---------+
       |        |         |
       v        v         v
    Hospital  Water     Emergency
               Pump     Lighting
```
""")

st.write(
    "The diagram represents the intended control architecture. "
    "The application calculates a simplified power balance and load allocation; "
    "it does not solve the electrical network or simulate real protection devices."
)

# --------------------------------------------------
# EVENT LOG
# --------------------------------------------------
st.divider()
st.markdown(
    '<div class="section-title">🧾 Fault & Event History</div>',
    unsafe_allow_html=True
)

log_df = pd.DataFrame(st.session_state.event_log)

st.dataframe(
    log_df.iloc[::-1],
    use_container_width=True,
    hide_index=True
)

col_a, col_b = st.columns(2)

with col_a:
    csv_data = log_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Event Log (CSV)",
        data=csv_data,
        file_name="microgrid_event_log.csv",
        mime="text/csv"
    )

with col_b:
    if st.button("🔄 Reset Event History"):
        st.session_state.event_log = []
        st.session_state.last_state = None
        st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "Autonomous Self-Healing Smart DC Microgrid | "
    "Software-only educational prototype | "
    "Not validated for real electrical protection or grid operation."
)
