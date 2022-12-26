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

## Installation
1. git clone
2. make a virtualenv
3. python setup.py install
4. setup a bing api key
5. set bing api key as local env
6. run tests

## Run
get run.py and how it works


## Package artifacts
Image from pynsource

1. Address manager
2. Address row
3. CsvReader
4. AddressGeocoder 
5. DictStacker
6. DistanceStacker
7. AddressGroupsWriter
