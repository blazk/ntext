#!/usr/bin/env python

from textwrap import dedent
import re


class Templates(dict):

    def expand(self, text, **local_templates):
        ctx = _Context()
        return self._expand(text, ctx, local_templates)

    _lbr = '<'
    _rbr = '>'

    class UndefinedTemplateError(Exception):
        pass
    class SyntaxError(Exception):
        pass


    @staticmethod
    def _to_tuples(argv):
        args = []
        for arg in argv:
            key, value = arg.split('=')
            args.append((key.strip(), value.strip()))
        return args


    def _to_command(self, keyword, args):
        cmd = [keyword]
        for arg, val in args:
            cmd.append('{}={}'.format(arg, val))
        return ', '.join(cmd)


    def _parse_command(self, it):
        # The "command" is a template invocation of the form
        # "<keyword, arg1=val1, arg2=val2,...>"
        # This method ingests text up to and including the closing
        # bracket. Returns keyword and a dict of arguments.
        command = ''
        nested = 0
        c = None
        prev_c = self._lbr
        while 1:
            try:
                c = it.next()
            except StopIteration:
                msg = 'missing "{rbr}" in "{lbr}{cmd}"'.format(
                        rbr=self._rbr, lbr=self._lbr, cmd=command)
                raise Templates.SyntaxError(msg)
            if c == self._lbr:
                if prev_c == '\\':
                    command = command[:-1] + c
                    continue
                nested += 1
            if c == self._rbr:
                if prev_c == '\\':
                    command = command[:-1] + c
                    continue
                if nested == 0:
                    break
                nested -= 1
            prev_c = c
            command += c
        argv = command.split(',')
        keyword = argv.pop(0)
        args = self._to_tuples(argv)
        return keyword, args


    def _get_template(self, keyword, ctx, local_templates):
        """
        Return expanded template associated with the keyword
        """
        try:
            template = local_templates[keyword]
        except KeyError:
            try:
                template = self[keyword]
            except KeyError:
                msg = 'Undefined template "{}"'.format(keyword)
                if ctx.trace:
                    #msg += ' (in {})'.format(ctx.trace[-1])
                    msg = ctx.traceback(msg)
                raise Templates.UndefinedTemplateError(msg)
        return template


    def _expand(self, text, ctx, local_templates):
        it = iter(text)
        expanded = ''
        prev_c = None
        indent = 0
        try:
            while 1:
                c = it.next()
                if c == self._lbr:
                    if prev_c == '\\':
                        expanded = expanded[:-1] + c
                        continue
                    keyword, args = self._parse_command(it)
                    templates = dict(local_templates)
                    templates.update(args)
                    keyword = self._expand(keyword, ctx, templates)
                    template = self._get_template(keyword, ctx, templates)
                    ctx.trace.append(self._to_command(keyword, args))
                    ctx.indent += indent
                    expanded += self._expand(template, ctx, templates)
                    ctx.trace.pop()
                    ctx.indent -= indent
                    indent = 0
                    continue
                if c == self._rbr and prev_c == '\\':
                    expanded = expanded[:-1] + c
                    continue
                if c == ' ':
                    indent += 1
                else:
                    indent = 0
                expanded += c
                if c == '\n':
                    expanded = expanded + ' ' * ctx.indent
                prev_c = c
        except StopIteration:
            return expanded





class _Context(object):

    def __init__(self):
        self.trace = []
        self.indent = 0

    def traceback(self, msg):
        lines = ['\n  {}'.format(t) for t in (self.trace)]
        lines.append('\n    ' + msg)
        return '\nTraceback (most recent template last):' + ''.join(lines)



def trim(text):
    '''
    Dedents text, then removes leading spaces up to and incuding first newline,
    and trailing spaces starting from the last newline.
    '''
    try:
        m = re.search(r'\s*?\n(.*)\n\s*?$', dedent(text), flags=re.DOTALL)
        return m.group(1)
    except AttributeError:
        return dedent(text)
