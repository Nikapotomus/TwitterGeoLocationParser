# TwitterGeoLocationParser
Nikola Katchkin Cucakovic, October 2016

## Overview
Pulls twitter feed data and parses forensically valuable data to create a csv file.

## Usage
Go to https://apps.twitter.com/ to register for api keys as this is required

Simply run the python script and specify the twitter account to pull data from.

```python
python <script directory>/run.py
```
Once run you will be notified on the number of found items along with the output file in the kml_files directory.

## Dependencies

* [Twython](https://twython.readthedocs.io/en/latest/)
* [csv](https://docs.python.org/2/library/csv.html)
* [simplekml](http://simplekml.readthedocs.io/en/latest/)
