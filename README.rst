Introduction
============
``pyramid_recipe_modwgi`` is a `zc.buildout`_ recipe which create `mod_wsgi`_
entry point for your wsgi application.

Package was inspired by `collective.recipe.modwsgi`_.

.. contents::


Example
=======

    [buildout]
    parts = modwsgi

    [modwsgi]
    recipe = pyramid-recipe-modwsgi
    eggs = pyramid
    target = ${buildout:directory}/app.wsgi
    config-file = ${buildout:directory}/production.ini


Environment variables
=====================

mod_wsgi (and so Pyramid) applications doesn't inherit from Apache's environment variables.

If you need to use environment variables in your application, you can define another 'env' value
into your modwsgi section, like this:

    [modwsgi]
    ...
    env =
        CHAMELEON_CACHE=${buildout:directory}/myapp/var/tmp


Changelog
=========

0.2 - 28-04-2016
----------------

- Added environment variables
  [tflorac]


0.1 - 05-10-2012
----------------

- Initial release
  [garbas]


Contributors
============

- `Rok Garbas`_

- `Thierry Florac`_


.. _`zc.buildout`: http://buildout.org
.. _`mod_wsgi`: http://code.google.com/p/modwsgi
.. _`collective.recipe.modwsgi`: https://github.com/wichert/collective.recipe.modwsgi
.. _`Rok Garbas`: http://garbas.si
.. _`garbas`: http://garbas.si
.. _`Thierry Florac`: http://hg.ztfy.org
