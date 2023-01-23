
import sys
import os
from docutils.parsers.rst import Directive, directives 
from docutils import nodes, statemachine
import subprocess


class ExecDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = True

    option_spec = {
        'filename': directives.path,
        # 'args': directives.args,
    }

    def run(self):
        fname = self.options.get('filename')
        is_temp = not fname
        try:
            if is_temp:
                fname = os.path.abspath('_tmp.py')
                with open(fname, 'w') as f:
                    f.write('\n'.join(self.content))

            r = subprocess.run([sys.executable, fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = [nodes.literal_block(text=open(fname).read())]
            out = r.stdout.decode()
            if out:
                output.extend([nodes.paragraph(text='Output:'), nodes.literal_block(text=out)])
            if r.returncode:
                output.extend([
                    nodes.paragraph(text='Error:'),
                    nodes.error(None, nodes.literal_block(text=r.stderr.decode()))
                ])
            return output
        finally:
            if is_temp and os.path.isfile(fname):
                os.remove(fname)

def setup(app):
    app.add_directive('exec-code', ExecDirective)
