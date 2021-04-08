# Install Java first
# then pip install tabula-py
# then pip install tabulate
from tabula import read_pdf
from tabulate import tabulate

# reads table from pdf file
path="" #Edit path to where file resides on your computer
tables = read_pdf(path, pages="all")
# if the pdf is one table on one page,
# tables becomes a Pandas dataframe;
# if the pdf has many pages,
# tables becomes a Python list of dataframes
print(tabulate(tables[0]))
