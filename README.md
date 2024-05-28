# Frequency_processing

This Python program scrapes news articles from various finance websites and analyzes the frequency of specified keywords within those articles. The results are saved to a CSV file for further analysis.

## Installation

To run this program, you need to install the following Python packages:

- `requests`
- `beautifulsoup4`
- `pandas`

You can install these packages using `pip` with the following command:

```bash
py -m pip install requests beautifulsoup4 pandas
```

## Usage

To run the program, navigate to the directory containing the script and execute it with Python:

```bash
python Frequency_processing.py
```

The script will scrape the specified finance websites, analyze the content for the given keywords, and output the results to a CSV file named `frequency.csv`.

## Output

After running the script, you will find the `frequency.csv` file in the same directory. This file contains the frequency counts of each keyword across the different websites.

