Things To Do and Keep in Mind
=============================

Things To Keep in Mind
----------------------

Our overall coding goals (in roughly decreasing importance):

1. Write code that is easy to understand and extend: style, design, and documentation.

  * Please force yourself to adhere to `PEP 8 style guide. <http://legacy.python.org/dev/peps/pep-0008>`_

    Standardizing our coding style promotes readability. 

    20 useful adages: `Zen of Python <http://legacy.python.org/dev/peps/pep-0020/>`_

  * Program design and development is nontrivial, ideally we would follow the 
    new school philosophy of `"agile development" <http://en.wikipedia.org/wiki/Agile_software_development>`_
    where development process involves many small iterations. 

2. Write code that works: unit testing.

  * Code is broken until tested.

3. Eventually write code that is efficient with time and memory, but only after #2.


Things To Do
------------

Things to be improved, tested, or implemented for the first time.

General Objectives
^^^^^^^^^^^^^^^^^^

1. Generally, we want to minimize our dependence on outside packages.

2. Descriptive and concise docstrings in all modules. Decide on essentials
   for docstrings.

3. Figure out how to grab source code docstrings into Sphinx documentation.

4. Write a simple example Document example.

Models
^^^^^^

1. Have a module for different contact interaction functions. Assign an 
   extensible way to label contact types.

    1. Possible contact types:

        LJ1210

        LJ1210rep

        Bare Gaussian

        Gaussian + hard wall

        Double Gaussian + hard wall

        Others? (Desolvation barriers, etc.)

    2. Consider allowing for interactions made up of a small set of 
       basis functions.

    3. Determine a quick way to evaluate the energies of contacts.

2. Decide on design that allows for multiple chains in the topology.