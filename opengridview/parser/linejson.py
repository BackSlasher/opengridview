from opengridview.parser import Parser
import json

class ParserLineJson(Parser):
  def __init__(self,config):
    Parser.__init__(self,config) # Base

  def read_stream(self, stream, item_func,header_func):
    while True:
      line = stream.readline()
      if line:
        item = json.loads(line)
        self.set_headers(item.keys()) # Always safe
        self.add_item([item.get(k) for k in self.header_names],header_func,item_func)
      else:
        break
