import os
import unittest
import sys
import json
import shutil

from .check import parse_dir, counting_nft, parse_args


TEST_JSON_1 = {'name': '90stx #6', 'symbol': 'YC', 'description': 'Remember to replace this description', 'seller_fee_basis_points': 1000, 'image': '6.png', 'external_url': 'https://www.youtube.com/c/hashlipsnft', 'edition': 6, 'attributes': [{'trait_type': 'Background', 'value': 'Black'}, {'trait_type': 'Eyeball', 'value': 'Red'}, {'trait_type': 'Eye color', 'value': 'Green'}, {'trait_type': 'Iris', 'value': 'Small'}, {'trait_type': 'Shine', 'value': 'Shapes'}, {'trait_type': 'Bottom lid', 'value': 'Low'}, {'trait_type': 'Top lid', 'value': 'High'}], 'properties': {'files': [{'uri': '6.png', 'type': 'image/png'}], 'category': 'image', 'creators': [{'address': 'Cq315bYim8bhXukPv1eWYgDP5LRegvRzfHgasU5pW7Y4', 'share': 100}]}}
TEST_JSON_2 = {'name': '90stx #9', 'symbol': 'YC', 'description': 'Remember to replace this description', 'seller_fee_basis_points': 1000, 'image': '9.png', 'external_url': 'https://www.youtube.com/c/hashlipsnft', 'edition': 9, 'attributes': [{'trait_type': 'Background', 'value': 'Black'}, {'trait_type': 'Eyeball', 'value': 'Red'}, {'trait_type': 'Eye color', 'value': 'Yellow'}, {'trait_type': 'Iris', 'value': 'Large'}, {'trait_type': 'Shine', 'value': 'Shapes'}, {'trait_type': 'Bottom lid', 'value': 'Middle'}, {'trait_type': 'Top lid', 'value': 'Middle'}], 'properties': {'files': [{'uri': '9.png', 'type': 'image/png'}], 'category': 'image', 'creators': [{'address': 'Cq315bYim8bhXukPv1eWYgDP5LRegvRzfHgasU5pW7Y4', 'share': 100}]}}


class TestCountingRarity(unittest.TestCase):

    def test_counting_nft(self):
        nfts, statistics = counting_nft([TEST_JSON_1, TEST_JSON_2])
        self.assertTrue('rarity' in nfts[0])
        self.assertTrue('myth' in statistics)

    def test_parse_dir(self):
        directory = 'test_json'
        os.makedirs(directory)
        file_name_1 = os.path.join(directory, 'test_1.json')
        file_name_2 = os.path.join(directory, 'test_2.json')
        file_1 = open(file_name_1, 'w')
        file_2 = open(file_name_2, 'w')
        json.dump(TEST_JSON_1, file_1)
        json.dump(TEST_JSON_2, file_2)
        file_1.close()
        file_2.close()
        nfts = parse_dir(directory, 'myth', 'yes')
        shutil.rmtree(directory)
        self.assertTrue('rarity' in nfts[0])

    def test_parser_args(self):
        args = ['assets', '--nft', 'myth', '--stat', 'yes']
        for arg in args:
            sys.argv.append(arg)
        directory, attribute, stat = parse_args(sys.argv[1:])
        self.assertTrue('assets' in directory)
        self.assertTrue('myth' in attribute)
        self.assertTrue(stat)

if __name__ == '__main__':
   tcr = TestCountingRarity()