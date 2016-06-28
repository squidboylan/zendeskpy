from __future__ import print_function
from zendeskhc.HelpCenter import HelpCenter
import sys

try:
    domain = sys.argv[1]
except:
    print("You must pass the zendesk website as argument 1")
    sys.exit(1)

hc = HelpCenter(domain)
print(hc.list_all_articles())
print(hc.list_all_sections())
print(hc.list_all_categories())
