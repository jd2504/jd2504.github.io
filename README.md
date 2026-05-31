## build

The reading log under `lego/` is generated from markdown sources by `lego/src/build.py`.

Requires Python 3.9+ and PyYAML:

```
pip install -r lego/requirements.txt
python3 lego/src/build.py
```

Sources live in `lego/src/` (`books/*.md`, `writings/*.md`, `templates/`). The
build writes generated HTML to `lego/` (`read.html`, per-entry pages, `aaNNN.html`
redirects) and `lego/writings/`. Generated HTML is committed, so GitHub Pages
serves it directly — after editing a source `.md`, rebuild and commit the output.


## reading

[eBook of Books](https://jd2504.github.io/lego/read.html)

[2024](https://jd2504.github.io/lego/writings/reading-2024.html)

[2025](http://substack.com/@deerwester/p-183404073)


## writing

[Thoughts on Not In Our Genes, Lewontin, Kamin, and Rose, 1984](https://jd2504.github.io/lego/not-in-our-genes-lewontin-1984.html) [2024-02-20] *Genetics, evolutionary biology, and sociobiology*

[GPTs and other gollems](https://jd2504.github.io/lego/writings/harris-gollems.html) [2023-12-04] *Tristan Harris talk on GPTs and AI*

[LLMs, the brain, and whatever general intelligence is](https://jd2504.github.io/exaro/llms_and_intelligence.html) [2024-12-02]


### papers

## refs and random useful resources

[use gnu emacs](https://www2.lib.uchicago.edu/keith/emacs/) - u chicago, waclena book

[tufte-latex classes](https://www.ctan.org/pkg/tufte-latex)

[learn medical neuroscience site](https://www.learnmedicalneuroscience.nl/)

[MNE tools](https://mne.tools/stable/index.html)
