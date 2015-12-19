
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
    self.approved_types = [int,str,float,bool,long,complex]
    self.config = config
    self.headers = None
    self.parse_headers(config.get('headers'))

  def parse_headers(self,headers):
    header_names = []
    header_types = []
    if not headers: headers=[]
    for header_item in headers:
      h_list = header_item.split(':')
      h_name = h_list[0]
      header_names.append(h_name)
      if len(h_list)>1: h_type = self.get_type(h_list[1])
      else: h_type = None
      header_types.append(h_type)
    self.header_names = header_names
    self.header_types = header_types

  def set_headers(self, titles):
    if not self.header_names:
      self.header_names = titles

  # Add a row of values as a new item
  def add_item(self,row,header_func,item_func):
    # Deduce header types if needed
    if not self.headers:
      val_types = [type(i) for i in row]
      # If we have pre-provided types, prefer it over the discovered values
      if self.header_types: val_types = self.merge_lists(self.header_types,val_types)
      # Set headers
      self.headers = zip(self.header_names,val_types)
      header_func(self.headers)
    # Convert row to acceptable types
    row = [ self.cast(z[0],z[1]) for z in zip(row,zip(*self.headers)[1]) ]
    row = self.inflate_truncate(row,len(self.headers))
    # Add item
    item_func(row)

  # Set the header types according to observed values from row. Call after setting header names
  def set_header_types(self, row_types):
    row_types = self.inflate_truncate(val_types,len(self.header_names))

  # Make l the length n, inflate using default or truncate
  def inflate_truncate(self,l,n,default=None):
    return l[:n] + [default]*(n-len(l))

  def g_type(self,value):
      if not value:
          return value
      elif type(value) in self.approved_types:
          return value
      else:
          return str(value)

  def get_type(self,type_name):
    global approved_types
    for t in self.approved_types:
      if t.__name__ == type_name:
        return t
    raise ValueError('No such type: %r' % type_name)

  def cast(self,inp,required_type):
    if inp == None:
      return None
    elif required_type == bool:
      return str(inp).lower() in ("yes", "true", "t", "1")
    else:
      return required_type(inp)

  # Merge lists like dictionary merge in ruby: Prefer the item in the first list, and if it's None defer to the same item in the second list
  def merge_lists(self,a,b):
    # Make B exactly long as A
    b = self.inflate_truncate(b,len(a))
    zipper = zip(a,b)
    return [ x[0] if x[0] else x[1] for x in zipper ]

  def read_stream(self, stream, item_func, header_func):
    raise Exception('Should be implemented in subclasses') # TODO throw proper exception
