from parsers.regions_parser import regions_parse
from parsers.events_parser import events_parse

def main():
  regions_parse()
  events_parse(1, 2024, 12, 2024)
  

main()