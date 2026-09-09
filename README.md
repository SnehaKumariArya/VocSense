# VocSense: Decoding Speech from Neck Muscle Activity
Bio-Electronic Silent Speech Recognition Neckband

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vocsense.streamlit.app)
[![Hardware Architecture](https://img.shields.io/badge/Hardware-ESP32%20%7C%20sEMG%20%7C%20IMU-0284c7)](#hardware-architecture)
[![ML Pipeline](https://img.shields.io/badge/Edge%20AI-TFLite%20Micro%20INT8-10b981)](#edge-ai--signal-processing)

**VocSense** is a non-invasive, wearable silent speech recognition (SSR) neckband engineered for individuals with speech-motor impairments (aphonia, ALS, post-laryngectomy) and hands-free tactical communication. 

By capturing submental surface electromyographic (sEMG) microvolt potentials alongside dynamic laryngeal kinematic strain, VocSense decodes unspoken phonetic articulation using on-device quantized Edge AI (<15ms latency) without requiring vocal fold vibration or cloud connectivity.

---

## Interactive 3D Digital Twin Visualizer

An interactive 3D digital twin of the hardware collar has been built using **Three.js** and deployed via **Streamlit**.

* **Live Web App:** [VocSense on Streamlit](https://vocsense.streamlit.app) *(or your deployed URL)*
* **Features:** 360° OrbitControls inspection, raycasted hardware component identification, and real-time technical specification HUD cards.

---

## Hardware Architecture

| Component | Technical Specification | Subsystem Function |
| :--- | :--- | :--- |
| **sEMG Sensor (Anterior Digastric)** | Dry sintered Ag/AgCl contacts | Captures submental microvolt potentials during tongue depression and vocal shaping. |
| **sEMG Sensor (Thyrohyoid)** | High-CMRR (>100 dB) differential contacts | Tracks laryngeal elevation and thyroid cartilage displacement for vowel modulation. |
| **Kinematic Strain Gauges** | Dual piezoresistive flexible strips ($GF > 25$) | Measures throat circumference expansion to isolate articulation from jaw flex. |
| **Compute & Sensor Fusion Pod** | ESP32 SoC (Dual-Core 240 MHz) + MPU-6050 6-DOF IMU | Executes quantized on-device neural inference and cancels dynamic neck motion artifacts. |
| **Acoustic Transducer** | 1.5W Class-D micro-speaker (85 dB @ 10cm) | Instantaneous local synthesized voice playback of decoded silent speech tokens. |
| **Power Toggle & Recalibration** | Soft-latch tactile micro-switch | Controls system power states and initiates 60-second baseline drift recalibration. |
| **Power Management & Charging** | 500 mAh 3.7V LiPo Cell + Flush USB-C Port | Provides 14+ hours continuous battery life with 5V/1.5A fast charging (<40 min). |

---

## Edge AI & Signal Pipeline

```text
  [ sEMG Electrodes ]       [ Strain Gauges ]       [ 6-DOF IMU ]
           │                        │                     │
           ▼                        ▼                     ▼
┌──────────────────────┐  ┌────────────────────┐  ┌──────────────┐
│ Analog Pre-Amp & BPF │  │ Kinematic Baseline │  │ Gross Motion │
│   (20 Hz - 450 Hz)   │  │    Perimeter DSP   │  │ Cancellation │
└──────────┬───────────┘  └─────────┬──────────┘  └──────┬───────┘
           │                        │                    │
           └────────────────► Sensor Fusion ◄────────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │ TFLite Micro INT8  │
                         │ Inference (<15 ms) │
                         └──────────┬─────────┘
                                    │
                         ┌──────────┴─────────┐
                         ▼                    ▼
                [ Micro-Speaker ]     [ BLE 5.0 Output ]
