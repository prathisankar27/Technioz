# ⚡ Autonomous Self-Healing Smart DC Microgrid

### Disaster-Resilient Energy Management System

## 📌 Project Overview

The **Autonomous Self-Healing Smart DC Microgrid** is a Python-based software simulation designed to improve power reliability during disasters and electrical faults. It demonstrates how a smart microgrid can monitor energy availability, detect simulated faults, isolate affected loads, and prioritize electricity supply to essential services.

The project uses an interactive dashboard to simulate solar generation, battery storage, energy demand, and fault conditions.

## 🎯 Problem Statement

During disasters such as floods and cyclones, power outages can disrupt hospitals, water pumps, emergency lighting, and other essential services. Conventional power systems may take time to identify faults and restore supply.

This project demonstrates a smart microgrid approach to managing available energy and prioritizing critical loads during simulated faults.

## 💡 Proposed Solution

The simulation models a DC microgrid using solar power, battery storage, and intelligent load management. Users can change system parameters and introduce faults through an interactive dashboard to observe the system's response.

## ✨ Key Features

- **Solar Power Simulation:** Adjust solar power generation.
- **Battery Management:** Monitor battery state of charge and simulated discharge.
- **Fault Simulation:** Test solar failure, branch faults, and system overload scenarios.
- **Priority-Based Load Management:** Prioritize hospital loads, water pumps, and emergency lighting.
- **Interactive Dashboard:** View system status, energy balance, and power distribution.
- **Event Monitoring:** Review simulated system events.
- **CSV Export:** Download event logs for analysis.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Data visualization tools supported by Streamlit

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd autonomous-self-healing-dc-microgrid
```

Replace the placeholder with your actual repository URL.

### 2. Install Dependencies

```bash
pip install streamlit pandas
```

### 3. Run the Application

```bash
streamlit run app.py
```

### 4. Open the Dashboard

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 🧪 Simulation Scenarios

1. **Normal Operation:** Observe power generation and load supply.
2. **Solar Source Failure:** Simulate the loss of solar generation.
3. **Hospital Branch Fault:** Simulate isolation of the affected hospital branch.
4. **Water Pump Branch Fault:** Observe the response to a branch fault.
5. **Lighting Branch Fault:** Simulate an emergency lighting branch fault.
6. **System Overload:** Explore the dashboard's overload scenario.

## 🌍 Sustainable Development Goals

- **SDG 7 – Affordable and Clean Energy:** Supports renewable energy integration and reliable energy access.
- **SDG 9 – Industry, Innovation and Infrastructure:** Demonstrates intelligent and resilient energy infrastructure.
- **SDG 11 – Sustainable Cities and Communities:** Explores energy resilience for disaster-affected communities.

## 🔮 Future Improvements

- Integration with real-time sensors and microcontrollers.
- More accurate DC microgrid power-flow and battery models.
- Improved fault detection and protection coordination.
- Renewable energy forecasting.
- Hardware-in-the-loop testing.

## ⚠️ Disclaimer

This project is an educational software prototype. Solar generation, battery behavior, electrical faults, and load management are simulated. The system has not been validated for real-world electrical protection or direct connection to a power grid.

**Project Purpose**

To demonstrate how intelligent energy monitoring, simulated fault isolation, and priority-based power management can contribute to disaster-resilient communities.

