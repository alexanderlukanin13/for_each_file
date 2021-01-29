=============
for-each-file
=============


.. image:: https://img.shields.io/pypi/v/for_each_file.svg
        :target: https://pypi.python.org/pypi/for_each_file

.. image:: https://img.shields.io/travis/alexanderlukanin13/for_each_file.svg
        :target: https://travis-ci.com/alexanderlukanin13/for_each_file

Process each file in subdirectories in a Pythonic way, without boilerplate code.

Let's say we have following directory structure:

.. code-block:: text

    example/
        shapes.txt
        aa/
            colors.dat    # not a txt!
            numbers.txt
            pets.txt
        bb/
            names.txt
            cc/
                cars.txt

Print all ``*.txt`` files in all first-level subdirectories:

    >>> from for_each_file import for_each_file
    >>> for_each_file('example', print, pattern='*/*.txt')
    example/aa/numbers.txt
    example/aa/pets.txt
    example/bb/names.txt

But wait, there's more!

Filter directories and files via glob()
---------------------------------------

All syntax of :py:func:`pathlib.Path.glob` is supported.

Print all ``*.txt`` files in *all* subdirectories:

.. code-block:: python

    >>> for_each_file('example', print, pattern='**/*.txt')
    example/shapes.txt
    example/aa/numbers.txt
    example/aa/pets.txt
    example/bb/names.txt
    example/bb/cc/cars.txt

Print all ``*.txt`` files only in a top-level directory:

.. code-block:: python

    >>> for_each_file('tests/data/example', print, pattern='*.txt')
    example/shapes.txt

Print all ``*.txt`` files in first-level subdirectories:

    >>> for_each_file('example', print, pattern='*/*.txt')
    example/aa/numbers.txt
    example/aa/pets.txt
    example/bb/names.txt

Files as an iterable
--------------------

Iterate over :py:class:`pathlib.Path` objects:

.. code-block:: python

    >>> [x.name for x in iter_files('example', '**/*.txt')]
    ['shapes.txt', 'numbers.txt', 'pets.txt', 'names.txt', 'cars.txt']

...or over text file contents directly, for example combine the first words from each file:

.. code-block:: python

    >>> ', '.join(x.split(' ')[0] for x in iter_texts('example', pattern='**/*.txt'))
    'Square, One, Cat, Alice, Toyota'

Pasting all files together into corpus
--------------------------------------

.. code-block:: python

    >>> with open('corpus.txt', 'w') as corpus:
    ...   for_each_text('tests/data/example1', corpus.write, pattern='**/*.txt')

Convert files from one directory to another directory
-----------------------------------------------------

Let's say you want to extract OCR text from a large collection of ``*.pdf`` into ``*.txt`` files.

You have a wonderful function ``pdf_to_text(pdf_filename, txt_filename)`` from another package,
it does the job well, but how to apply it to a nested directory tree?

.. code-block:: python

    >>> from for_each_file import convert_files
    >>> convert_files('input/directory/with/pdfs', 'output/directory/for/txt', pdf_to_text, pattern='**/*.pdf', rename=lambda p: p.with_suffix('.txt'))

That's all. You'll have the same directory structure in output, and same file names, but with ``*.txt`` suffix instead of ``*.pdf``.

Of course, ``convert_files`` can be used for any kind of conversion.

Convert text files
------------------

If both input and output is plain text, use ``convert_texts`` and forget about reading and writing files.
For example, here's a snippet which MAKES EVERYTHING IN EVERY FILE UPPERCASE:

.. code-block:: python

    >>> convert_texts('example', 'output', str.upper, pattern='**/*.txt')

We open ``output/aa/numbers.txt`` and we see:

.. code-block:: text

    ONE TWO
    THREE


