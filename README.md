GSPN Lib - Library for Generalized Stochastic Petri Nets (GSPNs)
================================================================

### Installation

Build as a Python module:

    $ python setup.py develop

### Usage

The script `generate_tikz.py` takes GSPNs as input. GSPNs are provided in the PNPRO format which can be created with the [GreatSPN](https://github.com/greatspn/SOURCES) tool.

The script outputs a tex file containing a [tikz](http://www.texample.net/tikz/) picture representing the corresponding GSPN.

An example call would be:

    $ python bin/generate_tikz.py --gspn path/to/gspn_file.pnpro --out path/tikz.tex

### Latex files

To compile the tikz pictures within LaTeX the GSPN style provided in [tikz/gspn-tikz.tex](tikz/gspn-tikz.tex) needs to be provided.
An example include would look as follows:

    % Load required tikz packages
    \usepackage{tikz}
    \usetikzlibrary{positioning,arrows,petri}

    % Include GSPN styles
    \input{gspn-tikz}