class CSVfile:
  def __init__(self, filepath):
    self.filepath = filepath

  def read(self, type_checking=False, *args, **kwargs):
    data = []
    import csv
    with open(self.filepath) as file:
        reader = csv.reader(file, *args, **kwargs)
        for row in reader:
          for i,v in enumerate(row):
            row[i] = v = v.strip(""" ,"'""")
            if type_checking:
              if v.isdigit():
                row[i] = int(v)
              elif v.isdecimal():
                row[i] = float(v)
          if row:
            data.append(row)
    return data

  def toDict(self):
    master_dict = {}
    data = self.read()
    for i,v in enumerate(data):
      master_dict.update({v[0]:v[0:]})
    return master_dict

  def getHeaders(self, type_checking=True,  *args, **kwargs):
    import csv
    with open(self.filepath) as file:
      reader = csv.reader(file, *args, **kwargs)
      row = next(reader)
      column = []
      for i,v in enumerate(row):
        row[i] = v = v.strip(""" ,"'""")
        if type_checking:
          if v.isdigit():
            row[i] = int(v)
          elif v.isdecimal():
            row[i] = float(v)
      f = True
      while f:
        try:
          column.append(next(reader)[0])
        except (StopIteration,IndexError):
          f = False
      return {'row':tuple(row),'column':tuple(column)}

  def search(self, column_search_term=None, row_search_term=None):
    if column_search_term == None and row_search_term == None:
      return None
    search_res = []
    for i,v in enumerate(self.read(type_checking=False)):
      if row_search_term in v:
        search_res.append(v)
      elif column_search_term in v:
        search_res.append(v)
    return search_res if search_res else None
  
  def __list__(self):
    return self.read()
    
  def __dict__(self):
    return self.toDict()
    
  def __getitem__(self, index):
    return self.read()[index]