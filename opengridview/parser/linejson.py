import opengridview.parser
import json

class ParserLineJson(opengridview.parser.Parser):
  def __init__(self,config):
    opengridview.parser.Parser.__init__(self,config) # Base
    self.headers = None

  def read_stream(self, stream, item_func,header_func):
    while True:
      line = stream.readline()
      if line:
        item = json.loads(line)
        if not self.headers:
          self.headers = [(k,type(self.g_type(item[k]))) for k in item.keys() ]
          #TODO handle override headers
          if config.has_key('headers'):
            header_func(
                self.inflate_truncate(config['headers'],
                  len(self.headers),
                  default='???')
                )
          else:
            header_func(self.headers)
        vals = [self.g_type(t(item[key])) if item.has_key(key) else None for (key,t) in self.headers.iteritems()]
        item_func(vals)
      else:
        break
