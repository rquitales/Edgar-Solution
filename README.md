# Ramon's Edgar Analytics Coding Challenge Solution
#### README

## Requirements
This solution requires Python to run.

## Language and Modules
The solution presented here was coded in Python, and is targetted for Python 3. However, it is backwards compatible with Python 2 as well. No external modules/packages/libraries are required to run this as only the following default Python modules are used:

 * **_csv_**: To open and read the `log.csv` file sequntially.
 * **_datetime_**: To manipulate/parse dates and times.
 * **_collections_**: To use the specialized container data structure subclass, `OrderedDict`.
 * **_sys_**: To access variables passed from `run.sh`, the input files and output file location.
 
The `run.sh` script attempts to determine if the command `python3` exists on the machine running the script. If `python3` exists, the python script is run using the `python3` command. If the command is not found however, a fallback onto `python` is used. This is because Python 3 is the preferred version for running this script as it alows for greater efficiency.
## Approach
### Current Implementation
Currently, an ordered dictionary is used to log all sessions. An ordered data structure was used to preserve the order in which the IP addresses are logged in the original server log file. It was observed that the example log.csv records were first ordered by time then IP address. However, the specifications of this challenge **ONLY** explicitly mentioned that the log file was ordered by date/time and nothing was mentioned about the order of the IP address. Thus, to follow the specifications of this challenge, the assumption that IP address is ordered as well was **not** taken into account when solving this challenge. As such, this ruled out the use of faster non-ordered data structures such as hash tables.

This solution iterates over the CSV log file line by line. This sequential approach was determined to be the best method for two reasons:

    1. Processing of the sessions happens chronologically with time, with one IP address being able to have multiple sessions.
    2. Data is intended to be streaming for a frontend/dashboard to display.
    
As the log.csv file is to be processed row-by-row, it doesn't make sense to import it into memory before processing it row-by-row. The `csv` module in Python allows the reading of CSVs row-by-row and was used. A SQL query did not seem possible as well, thus copying the log.csv file into a database and then being queried was ruled out. Furthermore, in the **Implementation details** section of the challenge's ReadMe, it states "as you process the EDGAR weblogs line by line...." thus further indicating that this challenge is intended for us to sequentially process the log file.

As each line is read by the csv reader, it logs the IP address, date/time and number of files opened (always 1 in each iteration as each line in the log.csv is 1 file) as a list into an ordered dictionary. The **key** for the ordered dictionary is the IP address, while the **value** is a list of the other output fields of `sessionization.txt`. If the IP address is already present in the ordered dictionary, the script just updates the IP's time and file counter by 1. This script does not take into account the `cik`, `accession` and `extention` fields in the log.csv file as every document opened is always considered as one webpage request as per the FAQ section in the challenge's ReadMe. Each interaction also checks to see if any sessions have ended by comparing the latest time with every last log time for each IP address. If any session has ended, it is written to `sessionization.txt` and the record is then deleted from the ordered dictionary. At the end of interating over the csv rows, all remaining entries in the ordered dictionary are written out as all sessions are considered to have ended at the end of the log.csv file.

### Future Possible Implementation
If we can assume that the EDGAR log file is ordered by date/time then IP address (which was not explicitly specified), we can forgo an ordered dictionary and implement a similar approach but using a non-ordered dictionary - ie. hash tables. This would improve efficiency as `OrderedDict` maintains a doubly linked list that orders the keys according to insertion order. This means that `OrderedDict` can be more than twice as large as a normal dictionary thereby having a larger memory overhead. The final `sessionalization.txt` in this scenario would then have to be ordered by time and IP address to produce the same output, given that we can assume that IP address is also sorted.

