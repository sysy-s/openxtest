import json
import requests

# gets seller list form a given domain, returns array of dicts
def get_sellers(domain: str):

    try:
        if domain[:8] == 'https://' or domain[:7] == 'http://':
            res = requests.get(f'{domain}sellers.json') 
            print(f'{domain}sellers.json')
            if 'application/json' in res.headers.get('Content-Type'):
                return res.json()['sellers']
        else:
            res = requests.get(f'https://{domain}/sellers.json') 
            if 'application/json' in res.headers.get('Content-Type'):
                return res.json()['sellers']
    except:  # exceptions like a 404 for example, or an SSL exception
        pass
    return [{
            "seller_id": -1,
            "name": f"Exception: {domain} could not provide sellers.json",
            "domain": domain,
            "seller_type": "Not disclosed"
            }]


domains_checked = []    # used for not checking any domain twice for sellers.json
schain_object = {       # from openRTB github
    "schain": {
        "ver": "1.0",
        "complete": 0,
        "nodes": []
    }
}

# recursive function that takes the starting domain and preferred starting depth
# for each seller if checks if it's intermediary and if it is
def supply_chain(domain: str, depth: int) -> None:
    sellers = get_sellers(domain)
    for seller in sellers[:500]:
        global domains_checked
        global schain_object
        # some sites 
        if 'name' not in seller.keys():
            seller['name'] = "Not disclosed"
        if 'domain' not in seller.keys():
            seller['domain'] = "Not disclosed"
        if 'seller_type' not in seller.keys():
            seller['seller_type'] = "PUBLISHER"

        seller_node = {
            "sid": seller['seller_id'],
            "name": seller['name'],
            "domain": seller["domain"],
            "depth": depth
        }
        if seller_node not in schain_object['schain']['nodes']: # append current seller node if not present in nodes
            schain_object['schain']['nodes'].append(seller_node)
        if seller['seller_type'] == 'INTERMEDIARY' or seller['seller_type'] == 'BOTH': # recurse if intermediary or both
            if seller['domain'] in domains_checked: # if domain already checked, no need to recurse
                continue
            else:
                seller['sellers'] = get_sellers(seller['domain'])
                domains_checked.append(seller['domain'])
                print(seller['domain'])
                supply_chain(seller['domain'], depth + 1)


supply_chain('openx.com', 0)
with open('supply_chain.json', 'w+') as f:
    f.flush()
    json.dump(schain_object, f, indent=4)


# simple search for maximum depth
max_depth = 0
for node in schain_object['schain']['nodes']:
    if node['depth'] > max_depth:
        max_depth = node['depth']

print(f'Maximum supply chain depth: {max_depth}')