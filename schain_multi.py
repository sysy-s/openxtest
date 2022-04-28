import json
import requests
from threading import Thread
from queue import Queue
from threading import Thread

chekced_domains = set() # used for not checking any domain twice for sellers.json
schain_object = {       # from openRTB github
    "schain": {
        "ver": "1.0",
        "complete": 0,
        "nodes": []
    }
}

class SupplyChainWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            domain = self.queue.get()
            try:
                supply_chain(domain, 1)
            finally:
                self.queue.task_done()

# gets seller list form a given domain, returns array of dicts
def get_sellers(domain: str):

    try:
        if domain[:8] == 'https://' or domain[:7] == 'http://':
            res = requests.get(f'{domain}sellers.json') 
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

# recursive function that takes the starting domain and preferred starting depth
# for each seller if checks if it's intermediary and if it is already in the checked domains
def supply_chain(domain: str, depth: int) -> None:
    sellers = get_sellers(domain)
    print(domain, '-', len(sellers))
    for seller in sellers[:100]:
        global schain_object
        # some sites have lacking data so this is a quick fix
        if 'name' not in seller.keys():
            seller['name'] = "None"
        if 'domain' not in seller.keys():
            seller['domain'] = "None"
        if 'seller_type' not in seller.keys():
            seller['seller_type'] = "PUBLISHER"
        if 'seller_id' not in seller.keys():
            seller['seller_id'] = "None"

        # seller node to be appended to the schain object
        seller_node = {
            "sid": seller['seller_id'],
            "name": seller['name'],
            "domain": seller["domain"],
            "depth": depth
        }

        if seller_node not in schain_object['schain']['nodes']: # append current seller node if not present in nodes
            schain_object['schain']['nodes'].append(seller_node)

        if seller['domain'] in chekced_domains: # skip recursion if domain has already beed searched (not the most reliable while multithreading)
            continue

        if seller['seller_type'] == 'INTERMEDIARY' or seller['seller_type'] == 'BOTH': # recurse if intermediary or both
            seller['sellers'] = get_sellers(seller['domain'])
            chekced_domains.add(seller['domain'])
            supply_chain(seller['domain'], depth + 1)

def main():
    
    # we create a queue and workers (arbitrary amount)
    queue = Queue()
    # perform bacically the supply_chain function on the top level 
    # to filter out most of the duplicate domains, meaning less computing (still a lot)
    # adds all intermediary objects to queue where they are taken care of by workers
    # aside from that it's basically the same function as supply_chain with some minor tweaks
    for seller in get_sellers('openx.com'):
        if seller['domain'] in chekced_domains:
            continue
        if seller['seller_type'] == 'INTERMEDIARY' or seller['seller_type'] == 'BOTH':
            queue.put(seller['domain'])
        else:
            seller_node = {
                "sid": seller['seller_id'],
                "name": seller['name'],
                "domain": seller["domain"],
                "depth": 0
            }

            if seller_node not in schain_object['schain']['nodes']: # append current seller node if not present in nodes
                schain_object['schain']['nodes'].append(seller_node)

        chekced_domains.add(seller['domain'])
    
    # initialize workers
    for x in range(20):
        worker = SupplyChainWorker(queue)
        worker.daemon = True
        worker.start()

    queue.join()

    # after a very long wait dumps contents to file
    with open('supply_chain.json', 'w+') as f:
        f.flush()
        json.dump(schain_object, f, indent=4)

    # simple search for maximum depth
    max_depth = 0
    for node in schain_object['schain']['nodes']:
        if node['depth'] > max_depth:
            max_depth = node['depth']

    print(f'Maximum supply chain depth: {max_depth}')

if __name__ == '__main__':
    main()
