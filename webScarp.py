# WebScarp Using only libs on StandardLib of Python
# I used findall instead of search to make the script reusable if we search for multiple results.
from urllib.request import Request, urlopen
from re import findall, DOTALL

# GitHub webpage where the word list is published
url = "https://gist.github.com/meis/83472749034277a19844f5c7b1f77a2e#file-the-random-wordle-md"

# Making the request with urllib
req = Request(url)
# Fetching the response from the web
resp = urlopen(req)
# Taking the data from the response
respData = resp.read()

# Preparing the regex for extract the selected data from the data response
search = r'<p dir="auto">Please, use the following list of valid words<\/p>\\n<pre><code>(.*?)\\n<\/code><\/pre>'
# Extracting the selected data
words = findall(search, str(respData), DOTALL)
# Formatting the data
words = words[0].replace('\\n', '\n')

# Storing the list in a file
f = open("secrets", "w")
f.write(words)
f.close()
