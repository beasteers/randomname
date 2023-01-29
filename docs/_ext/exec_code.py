
import sys
import os
import contextlib
from docutils.parsers.rst import Directive, directives 
from docutils import nodes, statemachine
import subprocess


# class literal_block_compact(nodes.literal_block):
#     classes = nodes.literal_block.classes + []


class ExecDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = True

    option_spec = {
        'filename': directives.path,
        # 'args': directives.args,
        'hide_code': directives.flag,
    }

    @contextlib.contextmanager
    def _with_code_as_file(self, fname, content):
        if fname: 
            yield fname
            return
        import tempfile
        with tempfile.NamedTemporaryFile() as f:
            f.write('\n'.join(content).encode('utf-8'))
            f.seek(0)
            yield f.name

    def build_output(self, fname, r):
        output = []
        if not self.options.get('hide_code'):
            output.append(nodes.literal_block(text=open(fname).read(), classes=['highlight-source']))
        out = r.stdout.decode()
        output.append(nodes.literal_block(text=out, classes=[] if self.options.get('hide_code') else ['highlight-output']))
        if r.returncode:
            output.append(nodes.literal_block(text=r.stderr.decode(), classes=['highlight-error']))
        return [nodes.container("", *output, classes=["code-group"])]

    def run(self):
        with self._with_code_as_file(self.options.get('filename'), self.content) as fname:
            r = self.run_command(fname)
            return self.build_output(fname, r)


class ExecPython(ExecDirective):
    def run_command(self, fname):
        return subprocess.run([sys.executable, fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

class ExecShell(ExecDirective):
    def run_command(self, fname):
        return subprocess.run(['bash', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def setup(app):
    app.add_directive('exec-code', ExecPython)
    app.add_directive('exec-shell', ExecShell)

