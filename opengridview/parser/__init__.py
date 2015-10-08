
class Parser:

  @staticmethod
  def find_parser(config):
    parser = config['format']
    if parser == 'line_json':
        import opengridview.parser.linejson
        return opengridview.parser.linejson.ParserLineJson(config)
    elif parser == 'csv':
        import opengridview.parser.csvp
        return opengridview.parser.csvp.ParserCsv(config)
    elif parser == 'autosplit':
        import opengridview.parser.autosplit
        return opengridview.parser.autosplit.ParserAutoSplit(config)
    else:
        raise Exception('cant figure out format')

  def __init__(self, config):
    self.config = config

  # Make l the length n, inflate using default or truncate
  def inflate_truncate(self,l,n,default=None):
    return l[:n] + [default]*(n-len(l))

  def g_type(self,value):
      if not value:
          return value
      elif type(value) in [int,str,float,bool]:
          return value
      else:
          return str(value)

  def read_stream(self, stream, item_func, header_func):
    raise Exception('Should be implemented in subclasses') # TODO throw proper exception
