Introduction
============

A blog for Plone 5. Ideas have been take from `ftw.blog <https://github.com/4teamwork/ftw.blog>`_ and `plone.app.event <https://github.com/plone/plone.app.event>`_.

I've written it to learn Plone.


Install
=======

- Add ``collective.blog`` to your buildout configuration

::

    [instance]
    eggs =
        collective.blog

- Run buildout

- Install ``collective.blog`` in portal_setup

You can of course install it also by adding to to your `site` package.

- Add it to your packages **setup.py**

::

    install_requires=[
        ...
        `collective.blog`
    ]

- Add its profile as dependency to your **profiles/default/metadata.xml**

::

    <dependency>profile-collective.blog:default</dependency>


Registry settings
=================

- `collective.blog.interfaces.IBlogSettings.show_lead_image`
   Show lead image in blog entries.

   **default**: False

   **WARNING**: Don't disable once you added a lead image to a blog entry,
            you won't be able to save that entry else.

- `collective.blog.interfaces.IBlogSettings.batch_size`
   Number of blog entries to show on batch (prev/next) navigations.

   **default**: 10

- `collective.blog.interfaces.IBlogSettings.show_folder_title`
   Show the folders title on blog listings.

   **default**: False

- `collective.blog.interfaces.IBlogSettings.allow_anonymous_view_about`
   Allow anonymous users to see the about line.

   **default**: False


Views
=====

blog_listing
------------

A fast listing view for the content type `Blog Entry` it doesn't call getObject if
if you don't enable `show_lead_image`.

It show's all entries from all subfolders of the Folder where ist activated,
this is usefull for archived content. We will soon publish a addon which allows
you to archive your content (based on `sc.contentrules.groupbydate <https://github.com/collective/sc.contentrules.groupbydate>`_).


Blog Listing supports some request parameters:

   - **SearchableText**: Any Text

   Date range:

   - **start**: The start date to search for, as example: 2015-09-01
   - **end**: The end date to search for, as example: 2015-09-30, if omitted it searches until today.

   Or by `year`, `year and month` or `year, month and day`

   - **year**: The Year
   - **month**: The month, can be omitted then it will search for the whole year
   - **day**: The day, if bove the year and month have been given show only this day, can be omitted then it searches for the whole month.


Portlets
========

Subject cloud
-------------


Uninstall
=========

This package provides an uninstall Generic Setup profile, however, it will
not uninstall the package dependencies.
Make sure to uninstall the dependencies if you no longer use them.


Copyright
=========

This package is copyrighted by the `Webmeisterei <http://webmeisterei.com>`_.

``collective.blog`` is licensed under GNU General Public License, version 2.