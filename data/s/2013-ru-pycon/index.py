import subprocess

subprocess.call(
    'rst2s5.py --current-slide --visible-controls index.rst index.html'
    '&& cat extend.css >> ui/default/slides.css',
    shell=True
)
