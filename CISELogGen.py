from datetime import datetime
import random
import json
from netaddr import IPNetwork
import names
import uuid

subnets = {
    "3.88.45.0/24": {
        "location": "Ashburn, Virginia, USA",
        "region": "US East",
        "organization": "Amazon Web Services",
        "NetworkDeviceName": "US-VIR-ASW-01",
        "NAS-IP-Address": "3.88.45.1",
        "callingStationId": "02:00:09:19:d0:0f"
    },
    "87.141.86.0/24": {
        "location": "Berlin, Germany",
        "region": "Europe",
        "organization": "Deutsche Telekom",
        "NetworkDeviceName": "DE-BER-ASW-01",
        "NAS-IP-Address": "87.141.86.1",
        "callingStationId": "02:00:c9:60:d4:ea"
    },
    "203.0.113.0/24": {
        "location": "Tokyo, Japan",
        "region": "Asia Pacific",
        "organization": "IIJ",
        "NetworkDeviceName": "JP-TO-ASW-01",
        "NAS-IP-Address": "203.0.113.1",
        "callingStationId": "02:00:0e:4d:08:6e"
    },
    "101.160.142.0/24": {
        "location": "Sydney, Australia",
        "region": "Oceania",
        "organization": "Telstra",
        "NetworkDeviceName": "AU-SY-ASW-01",
        "NAS-IP-Address": "101.160.142.1",
        "callingStationId": "02:00:ae:93:48:50"
    },
    "187.75.199.0/24": {
        "location": "Sao Paulo, Brazil",
        "region": "South America",
        "organization": "Telefônica Brasil",
        "NetworkDeviceName": "BR-SP-ASW-01",
        "NAS-IP-Address": "187.75.199.1",
        "callingStationId": "02:00:0d:4a:bc:9f"
    }
}

device_types = [
    "Windows-Workstation", "Macbook", "iPhone", "Android", "Linux-Laptop"
]

def generate_mac():
    random_bytes = [random.randint(0, 255) for _ in range(4)]
    return f"02:00:{random_bytes[0]:02x}:{random_bytes[1]:02x}:{random_bytes[2]:02x}:{random_bytes[3]:02x}"

def generate_log_entry(seq_id):
    subnet, attr = random.choice(list(subnets.items()))
    framed_ip = str(random.choice(list(IPNetwork(subnet))[10:-1]))
    username = f"{names.get_first_name().lower()}.{names.get_last_name().lower()}"
    device_type = random.choice(device_types)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    auth_rule = random.choice(["Permit_802.1X", "Permit_MAB", "Quarantine"])
    timezone = "+02:00"
    message_id = random.randint(1000000, 9999999)
    step_id = 11003
    severity = "INFO"
    description = "Passed-Authentication: Authentication succeeded"

    calling_mac = generate_mac()

    kv_pairs = {
        "NetworkDeviceName": attr["NetworkDeviceName"],
        "User-Name": username,
        "Calling-Station-ID": calling_mac,
        "Called-Station-ID": attr["callingStationId"],
        "NAS-IP-Address": attr["NAS-IP-Address"],
        "NAS-Port": random.randint(1, 48),
        "Framed-IP-Address": framed_ip,
        "RequestLatency": random.randint(1, 100),
        "AuthenticationPolicyMatchedRule": auth_rule,
        "Device IP Address": str(random.choice(list(IPNetwork(subnet))[:-2])),
        "SelectedAccessService": "Default Network Access",
        "NetworkDeviceGroups": "Switches",
        "Location": attr["location"],
        "Device Type": device_type,
        "Acct-Delay-Time": 0,
        "Acct-Input-Octets": random.randint(10000, 99999),
        "Acct-Output-Octets": random.randint(10000, 99999),
        "Acct-Input-Packets": random.randint(50, 200),
        "Acct-Output-Packets": random.randint(50, 200),
        "Acct-Terminate-Cause": "User-Request",
        "undefined-52": str(uuid.uuid4())
    }

    kv_string = ", ".join(f"{key}={value}" for key, value in kv_pairs.items())
    message = f"{timestamp} {timezone} {message_id} {step_id} {severity} {description}, {kv_string}"

    return {
        "message": message,
        "cisco_ise": {
            "log": {
                "segment": {
                    "number": 0
                }
            }
        }
    }
def main():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ise_logs_{now}.jsonl"

    with open(filename, "w") as f:
        for i in range(10):  # generate 10 logs
            log_entry = generate_log_entry(i)
            f.write(json.dumps(log_entry) + "\n")

    print(f"✅ Generated: {filename}")

if __name__ == "__main__":
    main()