# text_clustering
Text Clustering on crisis dataset

## Requirements
You will need
* [Python](https://www.python.org/) version 3

## Usage
Execute the following command to run the code:
```
python3 clustering.py [input-path] [output-path]
```

```
usage: clustering.py [-h] [-v] input output

Clustering text to needs, resources, issues categories.

positional arguments:
  input       Input folder name
  output      Output folder name

optional arguments:
  -h, --help  show this help message and exit
  -v          Verbose output
```

## Input Format


```
{
    "originalText": "Text", 
    "createdAt": "1970-01-01T00:00:00Z", 
    "ORG": [
        "RT"
    ], 
    "language": "en", 
    "id": 123456789012345678, 
    "sentimentString": "Negative, Activation", 
    "GPE": [
        "GPEVALUE"
    ], 
    "geoLocations": [
        {
            "lat": 00.0000, 
            "lon": 00.0000, 
            "geohash": "abcdefghi"
        }
    ]
}
```
