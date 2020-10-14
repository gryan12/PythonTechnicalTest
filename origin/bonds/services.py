import requests
import json


_TIMEOUT = 5
_GLEI_URL = "https://leilookup.gleif.org/api/v2/leirecords?lei="


def get_legal_name(lei):
    """
        lei: :string:, length 12
    """
    try: 
        resp =  requests.get(
            _GLEI_URL + lei, timeout=_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        raise(e)

    try: 
        data = json.loads(resp.content)
    except json.JSONDecodeError as e:
        return None

    
    name = data[0].get("Entity").get("legal_name").get("$")

    print("name is: ", name)






    



