# MINDS-i-Debugger - Scripts
Scripts to assist in decoding and visualizing log data.

## Usage

To be filled out.

## reader.py

Provides a method for decoding live or saved data from the APM logger output.

NOTE: saved data testing is not implimented or tested.  Do not attempt to decode saved data.

General usage:
```
python3 reader.py [-h] [-i INFILE] [-o OUTFILE] [-p PORT]
```

Example:

```
python3 reader.py -p COM9
```
