# permit-grabber
A script that grabs building permits from https://www.burnaby.ca.

## Getting started

### Prerequisites
* Python 3
* beautifulsoup4 https://pypi.org/project/beautifulsoup4/
* requests https://pypi.org/project/requests/
* pdfrw https://pypi.org/project/pdfrw/

### How to run

```
python3 main.py <start date> <end date>
```
**Note:** To grab building permits from the same month, use the same date for both the start date and the end date.

Since the website only limits the PDFs to be displayed for one year, the range will vary depending on when the user utilizes the program. The range will be from "{Current Month} {Current Year}" to "{Current Month} {Current Year - 1}".
  
The following table was created on September 17, 2018:

| Valid Date Entries |
| ------------- |
| "September 2017" |
| "October 2017" |
| "November 2017" |
| "December 2017" |
| "January 2018" |
| "February 2018" |
| "March 2018" |
| "April 2018" |
| "May 2018" |
| "June 2018" |
| "July 2018" |
| "August 2018" |
| "September 2018" |

## Sample output:
Please see output.pdf.
