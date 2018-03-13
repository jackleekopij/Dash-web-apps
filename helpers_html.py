

def set_tab_labels(tab_names=None):
    '''
    set_tab_labels is used to set the labels on the left of the page.
    :param tab_names: an optional Python list to convert a list of names to tabs
    :return: an array of dictionary objects to be used in tabs of page.
    '''
    if tab_names == None:
        return [
                {'label': 'Market Value', 'value': 1},
                {'label': 'Usage Over Time', 'value': 2},
                {'label': 'Predictions', 'value': 3},
                {'label': 'Target Pricing', 'value': 4},
            ]
    else:
        return [{'label':x, 'value':i} for i,x in enumerate(tab_names)]