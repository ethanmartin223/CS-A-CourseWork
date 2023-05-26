import re
#RegEx function to remove HTML links (ie. <a href="https://...)

def extract_html_links(string_with_html_links):
  match_expression = r"""<.*?a.*?href=[\"\']http[s]?:/*?w{3}?\.?[a-zA-Z0-9/\.@#:%\-\$&!_]*\.[a-zA-Z0-9]*[a-zA-Z0-9/\.@#:%\-\$&!_]*[\"\'].*?>.*<.*?/a.*?>"""
  inner_match_patteren = r""">.*<"""
  link_match_pattern = r"""href=[\'\"].*?[\'\"]"""
  matches = re.findall(match_expression,string_with_html_links)
  links = []
  for i,v in enumerate(matches):
    inner_text = ''.join(re.findall(inner_match_patteren,v)).strip('<>')
    string_with_html_links = string_with_html_links.replace(v,inner_text)
    links+=[v.replace('href="','').rstrip('">') for i,v in enumerate(re.findall(link_match_pattern,v))]
  return string_with_html_links, links

