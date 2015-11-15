def escape_html(string):
    '''
    Returns the given string with ampersands and angle brackets
    encoded for use in HTML.
    '''
    return (string
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))
