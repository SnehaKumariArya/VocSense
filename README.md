# VocSense: Bio-Electronic Silent Speech Recognition Neckband

VocSense is a wearable bio-electronic silent speech recognition (SSR) neckband engineered for individuals with speech-motor impairments (aphonia, ALS, post-laryngectomy) and hands-free tactical covert communication.

By capturing submental surface electromyographic (sEMG) microvolt potentials alongside dynamic laryngeal kinematic strain, VocSense decodes unspoken phonetic intent using on-device quantized Edge AI (<15ms latency) without requiring vocal fold vibration, sound emission, or cloud connectivity.

## Technical Architecture Diagrams

### 1. Master System Hardware & Signal Flow

```
+---------------------------------------------------------------------------------------------------+
|                                      VOCSENSE HARDWARE ARCHITECTURE                               |
+---------------------------------------------------------------------------------------------------+
                                                                                                     
    SUBMENTAL THROAT SENSORS             ANALOG SIGNAL CONDITIONING            COMPUTE & EDGE AI POD 
  +--------------------------+          +---------------------------+        +-----------------------+
  |  Dry Ag/AgCl sEMG Nodes  | -------> |   AD8232 / MyoWare 2.0    | -----> |   ESP32-WROOM-32 MCU  |
  | (Digastric/Thyrohyoid)   |          |  High-CMRR Pre-Amp (>100dB)|        |  (Dual-Core 240 MHz)  |
  +--------------------------+          +---------------------------+        |                       |
                                                                             |  TensorFlow Lite Micro|
  +--------------------------+                                               |   INT8 Neural Engine  |
  | Piezoresistive Strain    | --------------------------------------------> |      (<15ms Latency)   |
  | Kinematic Sensor Strips  |                                               +-----------+-----------+
  +--------------------------+                                                           |           
                                                                                         |           
  +--------------------------+          +---------------------------+                    |           
  | MPU-6050 / BMI160        | -------> | Dynamic Head & Walk Motion| -------------------+           
  |  6-DOF IMU Sensor Pod    |          | Cancellation DSP Pipeline |                                
  +--------------------------+          +---------------------------+                                
                                                                                         |           
                                                                                         v           
                                                                             +-----------------------+
  +--------------------------+          +---------------------------+        | DUAL AUDIO SYNTHESIS  |
  | 3.7V 500mAh Li-Po Cell   | -------> | TP4056 PMIC + AMS1117 LDO | -----> | 1. 1.5W Micro-Speaker |
  | (14+ Hour Battery Autonomy)         | USB-C Fast-Charging Module|        | 2. BLE 5.0 Wireless   |
  +--------------------------+          +---------------------------+        +-----------------------+

```

### 2. Signal Processing & Neural Inference Pipeline (Mermaid Diagram)

*Tip: Copy the code block below into [Mermaid Live Editor](https://mermaid.live) to rgender and download a high-resolution PNG image for your document submission.*

```
graph TD
    %% Sensor Inputs
    subgraph SENSORS ["1. Submental Sensor Transduction"]
        A1["Dry Ag/AgCl sEMG Electrodes<br/>(Anterior Digastric & Thyrohyoid)"]
        A2["Piezoresistive Strain Sensors<br/>(Laryngeal Kinematics)"]
        A3["MPU-6050 / BMI160 6-DOF IMU<br/>(Head Motion Cancellation)"]
    end

    %% Analog & DSP
    subgraph DSP ["2. Analog Front-End & DSP Pipeline"]
        B1["AD8232 / MyoWare 2.0 AFE<br/>High-CMRR Differential Boost"]
        B2["50 Hz Active Notch Filter<br/>Powerline Hum Removal"]
        B3["20 Hz - 450 Hz Bandpass Filter<br/>Neuromuscular Band Isolation"]
        B4["IMU Sensor Fusion<br/>Baseline Drift Subtraction"]
    end

    %% Edge AI Execution
    subgraph AI ["3. On-Device Edge AI Execution"]
        C1["ESP32 ADC Digitization<br/>(1 kHz Sampling Rate)"]
        C2["1D-CNN Feature Extractor<br/>(Spatial Muscle Contractions)"]
        C3["BiLSTM Sequence Model<br/>(Temporal Phonetic Transitions)"]
        C4["TFLite Micro INT8 Engine<br/>(<15 ms On-Chip Inference)"]
    end

    %% Output Synthesis
    subgraph OUTPUT ["4. Speech Synthesis & Telemetry"]
        D1["Direct Acoustic Output<br/>(Integrated 1.5W Micro-Speaker)"]
        D2["BLE 5.0 Data Stream<br/>(Tactile Earpiece / Mobile App)"]
        D3["Status Telemetry<br/>(Dual-Color Micro-LEDs)"]
    end

    %% Connections
    A1 --> B1
    A2 --> B3
    A3 --> B4
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> D1
    C4 --> D2
    C4 --> D3

    %% Styling
    style SENSORS fill:#f0f9ff,stroke:#0284c7,stroke-width:2px;
    style DSP fill:#fefce8,stroke:#eab308,stroke-width:2px;
    style AI fill:#ecfdf5,stroke:#10b981,stroke-width:2px;
    style OUTPUT fill:#faf5ff,stroke:#a855f7,stroke-width:2px;

```

## Hardware Component Master List & Specification

| Module Category | Selected Component | Subsystem Function | 
| ----- | ----- | ----- | 
| **sEMG Transduction** | Dry Sintered Ag/AgCl Contact Plates | Captures submental microvolt muscle potentials without conductive gel. | 
| **Analog Front-End** | AD8232 / MyoWare 2.0 Module | High-CMRR (>100 dB) differential bio-potential pre-amplifier. | 
| **Motion Tracking** | MPU-6050 / BMI160 6-DOF IMU | Dynamic motion tracking for neck rotational drift cancellation. | 
| **Kinematic Sensors** | Piezoresistive Strain Strips | Tracks physical throat expansion during tongue articulation. | 
| **Microcontroller** | ESP32-WROOM-32 / NodeMCU | Dual-core 240 MHz MCU executing TensorFlow Lite Micro INT8 model. | 
| **Power Management** | TP4056 PMIC + AMS1117 LDO | Controls USB-C charging, battery protection, and stable 3.3V power. | 
| **Power Supply** | 3.7V 500 mAh Li-Po Cell | Provides 14+ hours continuous operation (\~38 mA draw). | 
| **Acoustic Transducer** | 1.5W Class-D Micro-Speaker | Direct vocal synthesis playback of decoded speech tokens. | 
| **Wireless Transceiver** | Onboard ESP32 BLE 5.0 Module | Transmits encrypted phonetic tokens to paired earpieces/apps. | 
| **Enclosure & Chassis** | Silicone Collar + PLA 3D Pod | Ergonomic neckband chassis with micro-Velcro tensioning strap. | 

## Repository Structure

```
├── app.py                      # Interactive 3D Digital Twin Visualizer (Streamlit + Three.js)
├── step1_data_generator.py     # Synthetic sEMG & kinematic signal generation script
├── step2_dsp_pipeline.py       # Analog bandpass, 50Hz notch & IMU sensor fusion pipeline
├── step3_train_model.py        # 1D-CNN + BiLSTM architecture, training & INT8 TFLite quantization
├── requirements.txt            # Python dependencies
├── README.md                   # Technical documentation
└── docs/
    ├── architecture_diagram.png # Exported Mermaid system architecture flowchart
    └── sfic_pitch_deck.pdf      # Seva First Innovation Challenge Phase 2 Proposal Deck

```

## How to Run & Verify

### 1. Run 3D Hardware Twin Locally

```
git clone https://github.com/SnehaKumariArya/VocSense.git
cd VocSense
pip install -r requirements.txt
streamlit run app.py

```

### 2. Live Deployed Link

Access the online digital twin visualizer at: <https://vocsense.streamlit.app>
