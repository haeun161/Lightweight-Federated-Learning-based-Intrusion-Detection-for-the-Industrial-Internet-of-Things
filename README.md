# Federated-Learning-based-Intrusion-Detection-for-the-Industrial-Internet-of-Things
Lightweight Federated Learning-based Intrusion Detection for the Industrial Internet of Things

# Abstract
With the exponential grow of IoT nodes, manufacturing and process industries are in- 
creasingly leveraging these nodes to gather data for model or building and automation. 
However, the lack of devices security measures in most IoT devices leaves them susceptible 
to attacks, leading to potential leaks in industrial secrets. Current solutions involve the use 
of intrusion detection systems (IDS) at industrial sites. However, these systems are typi- 
cally centralized, with individual nodes collecting and transmitting information directly to 
a central server. Thus, this process can lead to data falsification or leaks. In this study, 
we propose a novel approach to address this issue. We introduce a pruning-based learning 
method designed to minimize memory utilization by considering the limited resources of 
IoT nodes in a federated learning (FL)-based detection system. This system learns from 
data sensed by endpoints and shares only weight values, significantly reducing the risk of 
confidential information leakage. Experimental results show that our model enhances se- 
curity nine-fold compared to conventional models that learn from centrally received data. 
Additionally, our model reduces memory usage by 1.4 times while maintaining an accuracy 
rate of 97.7%. In conclusion, our proposed method offers a more secure and efficient solu- 
tion for industries using IoT nodes, ensuring the protection of valuable industrial secrets.

**Keywords:** Federated learning, MITRE ATT&CK, Internet of Things, Pruning

# Proposed Model
![image](https://github.com/haeun161/Lightweight-Federated-Learning-based-Intrusion-Detection-for-the-Industrial-Internet-of-Things/assets/80445078/960e8da7-8c06-44e0-8e09-d29945433aae)

### Dataset:
mapped logs and T-IDs performing an attack (collected by using the VAS Tool based on the 114 selected threat strategies)

**dataset contains 66 features:**
process ID and time type, connection information, event information (order, classification, summary, and time), file attributes (name, path, and 
type), login information, protocol and registry information, detection rules, transmission and reception information, SHA256, and window information (class and title)

**classification label:** MITRE ATT&CK Tactics ID & MITRE ATT&CK Techniques ID(used only Tactic ID in this experiment)

# Main Results
![image](https://github.com/haeun161/Lightweight-Federated-Learning-based-Intrusion-Detection-for-the-Industrial-Internet-of-Things/assets/80445078/84126e9a-35d0-4cc3-9ae1-7a4953880a01)


# Usage
### Dataset:
used preprocessed data as datset.csv : unopened for privacy easons

### Setup
Install dependencies using `pip install -r requirements.txt`

### Run
run `python main.py`
