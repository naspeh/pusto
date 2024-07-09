import subprocess

subprocess.call(
    'python -m docutils --writer=s5 --current-slide --visible-controls --output=index.html index.rst'
    '&& cat extend.css >> ui/default/slides.css',
    shell=True
)
