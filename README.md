# Palabras Locas

### What is it?
Palabras Locas is a simple python program which can be fed a file with english plane text, and for every sentence in that file, it will select a random word from each sentence, and ask you for a replacement of the same type (noun, verb, etc). Upon completion, it will ask you to hit enter for the resulting Palabras Locas.

### Why?
I was visiting Mexico with my family, and decided to take a break one afternoon, because I was cooking my carcus in the sun. I hid in the room and wrote this, for family entertainment.

### Installation
1. Clone this repo down, or download and extract the archive.
1. `cd` into the directory
1. Create a virtual environment for dependencies (python 3.6 recommended)<br>
`virtualenv -p python3 venv`
1. Source that virtual environment<br>
`source venv/bin/activate`
1. Install dependencies into the virtual environment<br>
`pip install -r requirements.txt`

### Running Palabras Locas
`python palabras_locas.py ${path/to/your/text/file.txt}`<br>
eg: `python palabras_locas.py test_texts/teapot.txt`

### Recommendations
1. Don't tell your audience what the source text is, it ruins the fun man...
1. If your source text has a lot of run-on sentences, replace some of those commas and semicolons with periods, so word replacements are not few, and far between.
1. Running on a Mac is recommended, because it will use the `say` tts utility to prompt your audience and when done, its default tinny voice will read the output while you can drink a cervesa.

### Lame Issues
1. The name, sorry.
1. It should be more descriptive in input specification, for example: probably tell you if it needs a plural noun, thing ending with "ing", a name should ask for a name, etc... The Vocabulary community python module would cover a bit of that.. however, I decided to use PyDictionary library, because it does not run into frequent rate limiting.
1. Probably should not be fed shell commands, since the say command is a simple os execution of stuff that was typed.
1. (Probably many other bugs...)

### Example Execution