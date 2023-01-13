# geocoding

Given a list of people and their addresses, this package groups 
people who live at the same address.

### Input of the package's main method:
* A path to a utf-8 encoded .csv file with two columns Name,Address.
* A path to a directory where output file should be saved.

### Output of the package's main method
A text document saved at the specified location. Each line is a comma-
separated list of names of the people living at the same address. The
names in a line should be sorted alphabetically. The lines of the file should
also be sorted alphabetically.

### Example input file data
> Name,Address \
Ivan Draganov,”ul. Shipka 34, 1000 Sofia, Bulgaria” \
Leon Wu,”1 Guanghua Road, Beijing, China 100020” \
Ilona Ilieva,”ул. Шипка 34, София, България” \
Dragan Doichinov,”Shipka Street 34, Sofia, Bulgaria” \
Li Deng,”1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020” \
Frieda Müller,”Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, 
Germany”

### Expected output
> Dragan Doichinov, Ilona Ilieva, Ivan Draganov \
Frieda Müller \
Leon Wu, Li Deng 

## Architecture

  ![architecture](https://github.com/batetopro/geocoding/blob/main/img/architecture.png?raw=true)

1. Input Connector - retrieve data - this is on the physical layer. It can
take as parameter from the file system, URL, cloud storage, stream, etc. The current implementation 
of the parameter is file path.
2. Reader - parses different formats to python structures. The input format can be
csv, json, XML, etc. and the current format is csv.
3. Transformer - it takes the input address and applies different transformations on it.
They can be organized as pipeline of different steps. The normalizations can be:
* Lexicographical NLP parsing
* Machine learning
* Geocoding (3rd party adapter)

The output of this stage is location.
4. Aggregator - combines the locations in different groups by using:
* location dictionary
* location distance
5. Writer - convert to target format.
6. Output connector - takes care of the physical storage.

## Installation
Git clone the repository
```commandline
git clone git@github.com:batetopro/geocoding.git
```
Optionally, create a new virtualenv:
```commandline
python -m venv venv
source venv/bin/activate
```
After that, go to the folder, in which the repository was cloned.
Install the package:
```commandline
cd geocoding
python setup.py install
```
---
Next, go to [bing maps site](https://www.bingmapsportal.com/Application) and create a new API key for this application.
Then, click on ``Copy key`` to get the value of the key.

  ![bing maps api key](https://github.com/batetopro/geocoding/blob/main/img/map_keys.png?raw=true)

set the api key as local environment variable:
```commandline
export BING_API_KEY=<Secret API Key>
```
---
Run the main script of the package:
```commandline
python -m geocoding
```
---
To use the additional LocationIQ geo encoder, create an account in LocationIQ.
After that, get an API Access Token from [here](https://my.locationiq.com/dashboard). 
Click on ``Show token`` and then on the icon to select the whole API Access Token.
Set the environment variable to use this value:
```commandline
export LOCATIONIQ_API_KEY=<Secret API Key>
```
Bear in mind, that the default Free Pricing plan has a limit of 2 requests per second.

## Package artifacts

  ![Class diagram](https://github.com/batetopro/geocoding/blob/main/img/class_diagram.png?raw=true)

* AddressManager - its constructor takes *input_path* and *output_path*. 
   It's *run* method orchestrates the whole process of reading the input file,
   doing the geocoding, group matching and output file writing.
* AddressRow - this is the model class. It has owner and address. 
   It also can have lat and lng.
* CsvReader - reads the input file and provides a list of AddressRow with owner and address.
* AddressGeocoder - takes a list of AddressRow and extends the rows by doing 
   lookups to geocode the address and set the lat and lng of the row.
  * DummyAddressEncoder - for test purposes. Uses a dict mapping
  * LocationIQAddressEncoder - calls to LocationIQ
  * BingAddressEncoder - calls to Bing
* AddressGroupMatcher - groups addresses by their lat and lng
  * DictGroupMatcher - uses the keys of a dictionary. 
  * DistanceGroupMatcher - uses the distance between the points.
* AddressGroupsWriter - sorts the groups data and saves it to the output file.

