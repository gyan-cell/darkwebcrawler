import requests

url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

body = {
    "input": """Input: hello
Output: hello

Input: Guide me  about the dark web 
Output: 
The dark web refers to a part of the internet that is intentionally hidden and requires specific software, configurations, or authorization to access. Unlike the surface web, which is indexed by search engines like Google and accessible via standard browsers, the dark web operates within encrypted networks and is not indexed by traditional search engines. Here’s a breakdown:

Key Characteristics:
Anonymity:

The dark web relies on technologies like Tor (The Onion Router) or I2P (Invisible Internet Project) to anonymize users'\'' identities and locations.
Websites on the dark web often have URLs ending in .onion (for Tor) or .i2p (for I2P).
Access Requirements:

You need specific software like the Tor browser to access dark web content.
Some sites require invitations or special credentials to access.
Content:

The dark web hosts a variety of content, including:
Legitimate activities: Privacy-focused communication, whistleblower platforms, and forums for freedom of speech in oppressive regimes.
Illicit activities: Black markets, hacking forums, illegal trade, and other unethical practices.
Not to Be Confused with the Deep Web:

The deep web refers to parts of the internet that are not indexed by search engines (e.g., private databases, academic journals, or personal email accounts). It’s much larger than the surface web.
The dark web is a small subset of the deep web, distinguished by its anonymity and encryption.
Uses of the Dark Web:
Positive Uses:
Protecting free speech under oppressive governments.
Sharing sensitive information securely (e.g., whistleblowing).
Negative Uses:
Illegal marketplaces for drugs, weapons, and stolen data.
Services for hacking, identity theft, and other cybercrimes.
Risks:
Legal Issues: Accessing or participating in illegal activities can lead to severe legal consequences.
Cybersecurity Risks: Malware, scams, and phishing attempts are common.
Surveillance: Despite anonymity tools, law enforcement agencies actively monitor the dark web.

Input: hi
Output:""",
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 200,
        "min_new_tokens": 0,
        "repetition_penalty": 1,
    },
    "model_id": "ibm/granite-3-8b-instruct",
    "project_id": "1be211f3-c770-4d0a-a2f6-9d368af4b4c0",
    "moderations": {
        "hap": {
            "input": {
                "enabled": True,
                "threshold": 0.5,
                "mask": {"remove_entity_value": True},
            },
            "output": {
                "enabled": True,
                "threshold": 0.5,
                "mask": {"remove_entity_value": True},
            },
        },
        "pii": {
            "input": {
                "enabled": True,
                "threshold": 0.5,
                "mask": {"remove_entity_value": True},
            },
            "output": {
                "enabled": True,
                "threshold": 0.5,
                "mask": {"remove_entity_value": True},
            },
        },
    },
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
}

response = requests.post(url, headers=headers, json=body)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()
