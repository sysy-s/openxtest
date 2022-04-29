# OpenX test

## Install packages
```
pip install -r requirements.txt
```

## Task 1
Outputs the supply chain object in `supply_chain.json` file.
File structure should look something along these lines:
```json
{
  "schain": {
    "ver": "1.0",
    "complete": 0,
    "nodes": [
        {
          "sid": "123456",
          "name": "Company name or exception",
          "domain": "domain",
          "depth": 0
        },
        {
          "sid": "123457",
          "name": "Company name or exception",
          "domain": "domain",
          "depth": 1
        }
    ]
}
```
Additionally it prints out the max depth of the chain when run.
### Run script (takes a while to run)
* Option 1
```
python3 schain.py
```
* Option 2 (multithreaded)
```
python3 schain_multi.py
```
## Task 2
Outputs soonest possible meeting, starting with today's date
### Run script
```
python3 find_available_slots.py --calendars dir --duration-in-minutes minutes --minimum-people ammount
```
### Run tests
Only available for `Task 2`, because quite frankly i didn't know how to test such a specific and large case.
```
pytest
```