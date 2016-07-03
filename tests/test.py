from __future__ import print_function
from zendeskhc.HelpCenter import HelpCenter
import sys

try:
    domain = sys.argv[1]
except:
    print("You must pass the zendesk website as argument 1")
    sys.exit(1)

hc = HelpCenter(domain)
#print(hc.list_all_articles())
sections = hc.list_all_sections()
categories = hc.list_all_categories()
print(hc.list_articles_by_locale('en-us'))
print(hc.list_articles_by_category(categories['categories'][0]['id']))
print(hc.list_articles_by_section(sections['sections'][0]['id']))
