import pandas as pd
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
fefu_id = '60103811'
con_file = open("config.json")
config = json.load(con_file)
con_file.close()
# view = 'COMPLETE' -- to access more fields
client = ElsClient(config['apikey'], num_res = 25)

search = ElsSearch('AF-ID( ' + fefu_id + ' )', 'scopus')
search.execute(client)
sr = search.results

result = []
res = {}

authorname = ''
authid = ''

special_fields = ['authname', 'authid', 'prism:coverDisplayDate',
                  'prism:pageRange', 'openaccessFlag', 'link', 'prism:coverDate']
fields = {
        'authname'                  : 'Authors',
        'authid'                    : 'Author(s) ID',
        'dc:title'                  : 'Title', 
        'prism:coverDate'           : 'Year', 
        'prism:publicationName'     : 'Source title',
        'prism:volume'              : 'Volume',
        'prism:doi'                 : 'DOI',
        'citedby-count'             : 'Cited by', 
        'subtypeDescription'        : 'Document Type',
        'eid'                       : 'EID'
        }

for item in sr:
    '''
    for elem in item['author']:
        authorname += elem['authname'] + ', '
        authid += elem['authid'] + ', '
    
    res[fields['authname']] = authorname[:-2]
    res[fields['authid']] = authid[:-2]
    '''
    res[fields['authname']] = authorname
    res[fields['authid']] = authid
    
    res['Link'] = item['link'][2]['@href']

    res[fields['prism:coverDate']] = item['prism:coverDate'][0 : 4]
    
    try:
        page_range = item['prism:pageRange'].split('-')
    except:
        page_range = ['nan', 'nan']
    res['Page start'] = page_range[0]
    res['Page end'] = page_range[1]
    
    if item['openaccessFlag']:
        res['Access Type'] = 'Open Access'
    
    for key in item:
        for fieldname in fields:
            if fieldname in special_fields:
                continue
            try:
                res[fields[fieldname]] = item[fieldname]
            except KeyError:
                pass
    result.append(res)
    res = {}

orig_file = 'scopus.csv'
orig_df = pd.read_csv(orig_file)
res_file = 'res.csv'
res_df = pd.concat([pd.DataFrame(result), orig_df], ignore_index = True)
res_df.to_csv(res_file)

