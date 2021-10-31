from opengridview.parser import Parser
import csv

class ParserCsv(Parser):

  def __init__(self,config):
    Parser.__init__(self,config) # Base
    self.headers = None

  def read_stream(self, stream, item_func, header_func):
    while True:
      line = stream.readline()
      if line:
        if 'separator' in self.config:
          reader = csv.reader([line],delimiter=self.config['separator'])
        else:
          reader = csv.reader([line])
        row = next(reader)
        if not self.header_names:
          # This is the first row. Use it to set header names
          self.set_headers(row)
          continue # Don't process as input
        else:
          self.add_item(row,header_func,item_func)
      else:
        break
