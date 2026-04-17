# SDN Path Tracing Tool using Mininet and POX

## 📌 Problem Statement

The objective of this project is to design and implement an SDN-based path tracing tool that identifies and displays the path taken by packets in a network. The system tracks flow rules, determines forwarding paths, and validates network behavior under different scenarios.

---

## 🎯 Objectives

* Track flow rules installed by the controller
* Identify the forwarding path of packets
* Display the route taken from source to destination
* Validate behavior using test cases

---

## 🧠 Technologies Used

* Mininet (Network Emulator)
* POX Controller (SDN Controller)
* OpenFlow Protocol

---

## 🏗️ Network Topology

A linear topology with 3 switches and 3 hosts was used:

h1 — s1 — h2 - s2 — s3 — h3

This topology helps clearly observe packet traversal across multiple switches.

### Network Topology

<img width="504" height="196" alt="cnorange4" src="https://github.com/user-attachments/assets/7d3bd7f1-233d-4e5c-a91f-73d0805cacbc" />


This shows the Mininet network with hosts, switches, and controller connections.

---

## ⚙️ Setup and Execution

### Step 1: Start POX Controller

```bash
python3 pox.py pathtrace
```

### Step 2: Start Mininet

```bash
sudo mn --topo linear,3 --controller=remote,ip=127.0.0.1
```

### Step 3: Test Connectivity

```bash
pingall
```

---

## 🔍 Working Explanation

* The controller listens for PacketIn events
* It learns MAC-to-port mappings (learning switch logic)
* It installs flow rules (match-action)
* It tracks switches traversed by packets
* It displays the path in the controller terminal

---

## 📊 Sample Output

Example path output:

```
Path: h1 -> h2 via s1 -> s2 -> s3
```

---

## 🧪 Test Cases

### ✅ Test Case 1: Normal Operation

* Command: `pingall`
<img width="807" height="453" alt="cnorange1" src="https://github.com/user-attachments/assets/5d9a1dbf-f4b0-4e2c-8e1c-7fc29ac62de2" />
  
* Result: 0% packet loss
* Path successfully displayed

---

### ✅ Test Case 2: Link Failure

```bash
link s2 s3 down
pingall
```
<img width="399" height="232" alt="cnorange3" src="https://github.com/user-attachments/assets/e0570f04-5b91-4d23-9da0-0d02f91b63ff" />

* Result: Packet loss or altered behavior
* Demonstrates network response to failure

---

## 📸 Proof of Execution

### 1. Connectivity Test

<img width="807" height="453" alt="cnorange1" src="https://github.com/user-attachments/assets/5d9a1dbf-f4b0-4e2c-8e1c-7fc29ac62de2" />


### 2. Path Tracing Output

<img width="807" height="453" alt="cnorange1" src="https://github.com/user-attachments/assets/605c1303-bd5e-47c7-9bea-74d0d05fbe19" />


### 3. Flow Table Entries

```bash
sudo ovs-ofctl -O OpenFlow10 dump-flows s1
```

<img width="853" height="158" alt="cnorange2" src="https://github.com/user-attachments/assets/95a24ed2-1017-41ec-96a6-c69d79b08176" />


---

## 📈 Performance Analysis

* Latency measured using ping
* Flow table updates observed
* Packet forwarding behavior analyzed

---

## 🧠 Conclusion

This project demonstrates how SDN enables centralized control of network behavior. The controller dynamically installs flow rules and tracks packet paths, providing visibility into network operations.

---

## 📚 References

* https://mininet.org
* https://github.com/noxrepo/pox
* OpenFlow Documentation

---
