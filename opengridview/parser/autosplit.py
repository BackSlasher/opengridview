from opengridview.parser import Parser
import re

class ParserAutoSplit(Parser):

  def __init__(self,config):
    Parser.__init__(self,config) # Base
    if config.has_key('separator'):
      self.separator = config['separator']
    else:
      self.separator = '\s+'

  def read_stream(self, stream, item_func, header_func):
    while True:
      line = stream.readline()
      if line:
        line = line.rstrip()
        row = re.split(self.separator,line)
        if not self.header_names:
          # This is the first row. Use it to set header names
          self.set_headers(row)
          continue
        else:
          self.add_item(row,header_func,item_func)
      else:
        break
