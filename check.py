import os
import json
from collections import Counter, defaultdict
from decimal import Decimal
import argparse
import sys


def parse_dir(directory: str, nft: str = None, stat: bool = None):
    rarity_list = []
    for filename in os.listdir(directory):
        path_file = os.path.join(directory, filename)
        if not os.path.isfile(path_file):
            continue
        with open(path_file, 'r', encoding='utf-8') as file:
            try:
                rarity_list.append(json.load(file))
            except Exception as exp:
                print(f'Format file not correct - {path_file}')
                print(exp)
    print(f'Metadata successfully uploaded from "{directory}"')
    nfts, statistics = counting_nft(rarity_list)
    # for nft in nfts:
    #     print(nft['rarity'], nft['rank'], nft['stat'])
    if nft:
        print(f'Data and rarity for NFT #{nft}')
        json_formatted_str = json.dumps(nfts[int(nft)], indent=2)
        print(json_formatted_str)
    if stat:
        print('Counting statistics for collection:')
        json_formatted_str = json.dumps(statistics, indent=2)
        print(json_formatted_str)

    return nfts


def counting_nft(nfts: json):
    all_attributes = {}
    statistics = defaultdict(int)
    for n in nfts:
        for j in n['attributes']:
            if j['trait_type'] not in all_attributes:
                all_attributes[j['trait_type']] = []

            all_attributes[j['trait_type']].append(j['value'])
    for n in nfts:
        list_attr = [list(attr.values())[0] for attr in n['attributes']]
        for item in all_attributes.keys():
            if item not in list_attr:
                n['attributes'].append({item: {'value': 'None'}})
                all_attributes[item].append('None')
    attributes = {}

    for a in all_attributes:
        attributes[a] = dict(Counter(all_attributes[a]))
    smm = 0
    for a in attributes:
        smm += sum(attributes[a][val] for val in attributes[a])
    for a in attributes:
        for n in attributes[a]:
            attributes[a][n] = float(attributes[a][n] / smm)

    results = []
    for n in nfts:
        n['rarity'] = 1
        for attr in n['attributes']:
            n['rarity'] = n['rarity'] * Decimal(attributes[attr['trait_type']][attr['value']])

        results.append(n)
    close_results = sorted(results, key=lambda d: d['rarity'])
    for r in results:
        for index, item in enumerate(close_results):
            if item['name'] == r['name']:
                r['rank'] = 1 if not r['attributes'] else index
                r['rarity'] = str(r['rarity'])
    for r in results:
        lk = r['rank'] / len(nfts)
        if r['rank'] == 1 or r['rarity'] == 1:
            r['stat'] = 'Unique'
        elif lk <= 0.01:
            r['stat'] = 'Myth'
        elif 0.05 >= lk > 0.01:
            r['stat'] = 'Legendary'
        elif 0.15 >= lk > 0.05:
            r['stat'] = 'Epic'
        elif 0.35 >= lk > 0.15:
            r['stat'] = 'Rare'
        elif 0.6 >= lk > 0.35:
            r['stat'] = 'Uncommon'
        else:
            r['stat'] = 'Common'
        statistics[r['stat'].lower()] += 1
    return nfts, statistics


def parse_args(args):
    match_info = argparse.ArgumentParser(
        description='TON-NFT-Rarity-Check is a Python script for check rarity in TON NFT collection. Use script to get stats for entire collection or for selected NFT.'
    )
    match_info.add_argument(
        'dir',
        action='store',
        type=str,
        help='Path for directory'
    )
    match_info.add_argument(
        '--nft',
        action='store',
        type=str,
        help='Specific nft'
    )
    match_info.add_argument(
        '--stat',
        action="store_true",
        help='Showing statistics'
    )

    match_args = match_info.parse_args()
    nft = None
    stat = True
    if match_args.nft:
        nft = match_args.nft
        stat = False
    if match_args.stat:
        stat = match_args.stat
        
    return match_args.dir, nft, stat


if __name__ == '__main__':
    # print(sys.argv[1:])
    directory, nft, stat = parse_args(sys.argv[1:])
    parse_dir(directory, nft, stat)
