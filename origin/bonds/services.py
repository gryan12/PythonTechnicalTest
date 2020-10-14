import requests
import json


_TIMEOUT = 5
_GLEI_URL = "https://leilookup.gleif.org/api/v2/leirecords?lei="


def get_legal_name(lei):
    """
        lei: :string:, length 12
        returns None if cannot parse Legal Name from @lei
    """
    try: 
        resp =  requests.get(
            _GLEI_URL + lei, timeout=_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return None

    try: 
        data = json.loads(resp.content)
    except json.JSONDecodeError as e:
        return None

    if resp.status_code == 200:
        if data:
            return data[0].get('Entity').get('LegalName').get("$")

    return None







    



