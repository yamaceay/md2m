import sys

from commands import latex, latex_by_mpl

default_options = {
    'output': {'required': True},
    'dpi': {'type': int, 'default': 300},
    'background': {'default': '#FFFFFF'},
    'foreground': {'default': '#000000'}
}

def cli(options):
    output, dpi, bg, fg = options['output'], options['dpi'], options['background'], options['foreground']
    tex = ''.join(sys.stdin).replace('\n', ' ')
    try:
        latex(tex, output, dpi, bg, fg)
    except:
        try:
            latex_by_mpl(tex, output, dpi, bg, fg)
        except: 
            pass