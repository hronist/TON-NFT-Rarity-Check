# TON-NFT-Rarity-Check

TON-NFT-Rarity-Check is a Python script for check rarity in TON NFT collection. Use script to get stats for entire collection or for selected NFT.


## Usage

Prepare metadata for NFT collection in separate directory in json files. Use current assets folder for example.

```bash
python3 check.py [-h] [--nft NFT] [--stat] dir
```

Positional arguments:

  dir         Path for directory

Optional arguments:

  -h, --help  show this help message and exit


  --nft NFT   Specific NFT


  --stat      Showing statistics

For example.
```bash
python3 check.py assets --stat 
python3 check.py assets --nft 3
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
