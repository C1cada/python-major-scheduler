from urllib.request import urlopen

url = "https://www.rit.edu/programs-api/?type=p&q=PSYC-BS&college=&degree=&text="
page = urlopen(url)
print(page)