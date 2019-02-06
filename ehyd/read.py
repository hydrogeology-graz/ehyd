"""Module to read data from ehyd files.

Author: R.A. Collenteur, University of Graz.

"""


import pandas as pd
from numpy import nan
from io import StringIO


def read_ehyd(fname, name=None):
    """Method to read files from Ehyd.

    Parameters
    ----------
    fname: str
        String with the path and filename.
    name: str, optional

    Returns
    -------
    series: pandas.Series
        Pandas Series instance with the timeseries. The metadata is
        available as the metadata of the pandas Series.
        E.g. series.metadata.

    Notes
    -----
    Data from Ehyd is available at http://ehyd.gv.at


    """
    with open(fname, "r", encoding="iso8859", newline=None) as file:
        # Store the metadata in a dict
        metadata = {}

        line = file.readline()

        # Use "Werte:" as the identifier for the start of the data block
        while "Werte:" not in line:
            line = line.strip("\n")
            line = line.split(";")

            # Read in all usual metadata consisting of a key and value
            if len(line) is 2:
                line[0] = line[0].strip(" ").strip(":")
                metadata[line[0]] = line[1]
                line = file.readline()

            # Read in the metadata with multiple rows and put in a DataFrame
            elif len(line) is 1:
                key = line[0].strip(":").strip(" ")

                # Read in the line temporarily to find the length of the header
                temp_line = file.readline()
                header = temp_line.split(";")

                # Start a string to later provide to read_csv
                csv_str = temp_line

                # Keep scanning lines as long as they belong to the data
                belongs_to_data = True

                while belongs_to_data:
                    temp_line = file.readline()
                    new_line = temp_line.split(";")

                    if len(new_line) == len(header):
                        csv_str = csv_str + temp_line
                        belongs_to_data = True
                    else:
                        line = temp_line
                        belongs_to_data = False

                metadata[key] = pd.read_csv(StringIO(csv_str), dayfirst=True,
                                            index_col=0, parse_dates=True,
                                            skipinitialspace=True, sep=";")

            # If none of the above, simply store the data as a list
            else:
                key = line[0].strip(" ")
                line.remove(line[0])
                metadata[key] = line
                line = file.readline()

        # Read the time series in the remainder of the file using pandas
        f = file.read().replace(" ", "").replace(",", ".")

    if not name and "HZB-Nummer" in metadata.keys():
        name = metadata["HZB-Nummer"]
    else:
        name = fname

    date_parser = lambda s: pd.to_datetime(s, format="%d.%m.%Y%H:%M:%S")
    series = pd.read_csv(StringIO(f), sep=";", date_parser=date_parser,
                         parse_dates=True, names=["Date", name],
                         usecols=[0, 1], squeeze=True, index_col="Date",
                         na_values=[u"Lücke"])
    series.metadata = metadata
    return series
