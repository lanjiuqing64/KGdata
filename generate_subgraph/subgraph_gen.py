import itertools
import xmlrpc.client
import typing as tp
import json
from dataclasses import dataclass
import time
import typing as tp
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from client_utils import Entity, Relation, a_factory
import requests
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import time
import typing as tp
from concurrent.futures import ThreadPoolExecutor


SUBKG = defaultdict()
HOP2ENTITY = []

class WikidataQueryClient:
    def __init__(self, url: str):
        self.url = url
        self.server = xmlrpc.client.ServerProxy(url)

    def label2qid(self, label: str) -> str:
        return self.server.label2qid(label)

    def label2pid(self, label: str) -> str:
        return self.server.label2pid(label)

    def pid2label(self, pid: str) -> str:
        return self.server.pid2label(pid)

    def qid2label(self, qid: str) -> str:
        return self.server.qid2label(qid)

    def get_all_relations_of_an_entity(
        self, entity_qid: str
    ) -> tp.Dict[str, tp.List]:
        return self.server.get_all_relations_of_an_entity(entity_qid)
    def get_all_relations_of_an_entity_with_opposite(
            self, entity_qid: str, th_num_for_head: int, th_num_for_tail: int
    ) -> tp.Dict[str, tp.List[tp.Tuple]]:
        if True:
            return self.server.get_all_relations_of_an_entity_with_opposite(
                    entity_qid, th_num_for_head, th_num_for_tail)
        else:
            return self.server.get_all_relations_of_an_entity_with_opposite(self.server,
                    entity_qid, th_num_for_head, th_num_for_tail)

    def get_tail_entities_given_head_and_relation(
        self, head_qid: str, relation_pid: str
    ) -> tp.Dict[str, tp.List]:
        return self.server.get_tail_entities_given_head_and_relation(
            head_qid, relation_pid
        )

    def get_tail_values_given_head_and_relation(
        self, head_qid: str, relation_pid: str
    ) -> tp.List[str]:
        return self.server.get_tail_values_given_head_and_relation(
            head_qid, relation_pid
        )

    def get_external_id_given_head_and_relation(
        self, head_qid: str, relation_pid: str
    ) -> tp.List[str]:
        return self.server.get_external_id_given_head_and_relation(
            head_qid, relation_pid
        )

    def mid2qid(self, mid: str) -> str:
        return self.server.mid2qid(mid)

    def entities2label(self, entities: tp.List[tp.Tuple[str,str,str]]) \
        -> tp.Dict[str, str]:
        res = self.server.entities2label(entities)
        # print('test, ', res)
        return res



class MultiServerWikidataQueryClient:
    def __init__(self, urls: tp.List[str]):
        self.clients = [WikidataQueryClient(url) for url in urls]
        self.executor = ThreadPoolExecutor(max_workers=len(urls))
        # test connections
        start_time = time.perf_counter()
        self.test_connections()
        end_time = time.perf_counter()
        print(f"Connection testing took {end_time - start_time} seconds")

    def convert_entitiy_to_label(self, entities: tp.List[tp.Tuple[str,str,str]]) \
        -> tp.List[tp.Tuple[str,str,str]]:
        dic = self.query_all("entities2label", entities)['tail']
        res = []
        for head,rel,tail in entities:
            h = dic.get(head, None)
            r = dic.get(rel,  None)
            t = dic.get(tail, None)
            res.append((h,r,t))
         return res

def test_connections(self):
        def test_url(client):
            try:
                # Check if server provides the system.listMethods function.
                client.server.system.listMethods()
                return True
            except Exception as e:
                print(f"Failed to connect to {client.url}. Error: {str(e)}")
                return False

        start_time = time.perf_counter()
        futures = [
            self.executor.submit(test_url, client) for client in self.clients
        ]
        results = [f.result() for f in futures]
        end_time = time.perf_counter()
        # print(f"Testing connections took {end_time - start_time} seconds")
        # Remove clients that failed to connect
        self.clients = [
            client for client, result in zip(self.clients, results) if result
        ]
        if not self.clients:
            raise Exception("Failed to connect to all URLs") 
def query_all(self, method, *args):
        start_time = time.perf_counter()
        futures = [
            self.executor.submit(getattr(client, method), *args)
            for client in self.clients
        ]
        # Retrieve results and filter out 'Not Found!'
        is_dict_return = method in [
            "get_all_relations_of_an_entity",
            "get_tail_entities_given_head_and_relation",
            "get_tail_values_given_head_and_relation",
            "get_all_relations_of_an_entity_with_opposite",
            "entities2label"
        ]
        results = [f.result() for f in futures]
        end_time = time.perf_counter()
        # print(f"HTTP Queries took {end_time - start_time} seconds")

        start_time = time.perf_counter()
        real_results = set() if not is_dict_return else {"head": [], "tail": []}
        for res in results:
            if isinstance(res, str) and res == "Not Found!":
                continue
            elif isinstance(res, tp.List):
                if len(res) == 0:
                    continue
                if isinstance(res[0], tp.List):
                    res_flattened = itertools.chain(*res)
                    real_results.update(res_flattened)
                     continue
                else:
                    real_results.update({"head": [], "tail": res})
                #     continue
                # real_results.update(res)
            elif is_dict_return:
                if 'head' in res:
                    real_results["head"].extend(res["head"])
                    real_results["tail"].extend(res["tail"])
                else:
                    real_results.update({"head": [], "tail": res})

            else:
                real_results.add(res)
        end_time = time.perf_counter()
        # print(f"Querying all took {end_time - start_time} seconds")

        return real_results if len(real_results) > 0 else "Not Found!"
    
def get_all_triples(client, ent,th_num_for_head=300,th_num_for_tail=0):
    global SUBKG
    if ent in SUBKG:
        return SUBKG[ent]
    res = []
    results =client.query_all("get_all_relations_of_an_entity_with_opposite",ent,th_num_for_head,th_num_for_tail)
    res +=list(set([(ent,x[0],x[1])for x in results['head'] if 'N/A' not in x[1]]))
    tails = list(set([(ent,x[0],x[1])for x in results['head'] if 'N/A' in x[1]]))
    # get tail values
    for head,rel,_ in tails:
        tail_values = client.query_all("get_tail_values_given_head_and_relation",head, rel)# not so slow
        if len(tail_values['tail']):
            for tail in set(tail_values['tail']):
                if 'http' in tail.lower():
                    continue
                res.append((head,rel,tail))
    SUBKG[ent] = res
    return res
def get_nhop(client,start_entity, n_hop):
    global HOP2ENTITY
    current = [start_entity]
    res = []
    while n_hop > 0:
        next_hop = []
        for i in range(len(current)):
            next_hop += get_all_triples(client,current[i])
        res += next_hop
        current = [x[2] for x in next_hop if 'Q' in x[2]]
        n_hop -= 1
    res = list(set(res))
    print(len(res))
    HOP2ENTITY += current
    return res
def get_labels(client,ents):
    labels = client.convert_entitiy_to_label(ents)
    return labels

if __name__ == "__main__":
    addr_list = "/home/ec2-user/ToG/Wikidata/server_urls.txt"

    with open(addr_list, "r") as f:
        server_addrs = f.readlines()
        server_addrs = [addr.strip() for addr in server_addrs]
    print(f"Server addresses: {server_addrs}")
    client = MultiServerWikidataQueryClient(server_addrs)
    res = defaultdict()
    filename = 'T-REX'
    with open(f'/home/ec2-user/processed_{filename}.json', 'r') as f:
        creak = json.load(f)
    cnt = 0
    nhop = 2
    labeldict = defaultdict()
    # df = df.sample(1)
    for entityid,_ in creak.items():
        print(f'now is {cnt}th entity of {len(creak)}')
        triples = get_nhop(client,entityid,nhop)
        res[entityid] = triples
        current_labels =get_labels(client,triples)
        for id,label in zip(triples,current_labels):
            for x,y in zip(id,label):
                if y:
                    labeldict[x] = y

        cnt += 1
        # break

    # save the res as json file
    with open(f'/home/ec2-user/ToG/Wikidata/{filename}_2hop.json', 'w') as f:
        json.dump(res, f, indent=4)

    # save the labels as json file
    with open(f'/home/ec2-user/ToG/Wikidata/{filename}_2hop_labels.json', 'w') as f:
        json.dump(labeldict, f, indent=4)

    hop3_entities = list(set(HOP2ENTITY))
    hop3res = defaultdict()
    hop3labeldict = defaultdict()
    for ent in tqdm(hop3_entities):
        triples = get_all_triples(client,ent)
        hop3res[ent] = triples
        current_labels =get_labels(client,triples)
        for id,label in zip(triples,current_labels):
            for x,y in zip(id,label):
                if y:
                    hop3labeldict[x] = y

    # save the hop3res as json file
    with open(f'/home/ec2-user/ToG/Wikidata/{filename}_3rd_hop.json', 'w') as f:
        json.dump(hop3res, f, indent=4)
    # save the hop3labels as json file
    with open(f'/home/ec2-user/ToG/Wikidata/{filename}_3rd_hop_labels.json', 'w') as f:
        json.dump(hop3labeldict, f, indent=4)