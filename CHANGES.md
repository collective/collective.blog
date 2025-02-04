# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.1 (2025-02-04)


### Bug fixes:

- Override addCreator for not setting the default author if not set. @sneridagh #80
- change tag translation in queryfield. @jnptk #81

## 1.0.0 (2025-01-16)


### Bug fixes:

- Remove unnecessary .gitkeep files which broke the profile in Plone 5. @davisagli #79

## 1.0.0a13 (2024-06-17)


### Bug fixes:

- Remove custom serializers for blog content types. They were serializing preview_image_link in the wrong format. @davisagli #75

## 1.0.0a12 (2024-04-24)


### Bug fixes:

- Fix tags widget to not have an open vocabulary, and adjust Volto widget @sneridagh #71

## 1.0.0a11 (2024-04-10)


### Bug fixes:

- Fix 'Wrong contained type' error for new blog posts with no tags created using plone.restapi. @davisagli #69

## 1.0.0a10 (2024-03-28)


### New features:

- - Update German translations [@jonaspiterek] #63
- Update Brazilian Portuguese translations [@ericof] #67


### Internal:

- Add a GitHub Actions workflow to automatically check for Changelog entries on pull requests [@ericof] #65

## 1.0.0a9 (2024-03-27)


### New features:

- Added Blog Tag content type. A tags folder is created for new blogs, but not existing ones. @davisagli #61

## 1.0.0a8 (2024-02-28)


### Bug fixes:

- Limit authors vocabulary to authors from the current blog context. @davisagli #59

## 1.0.0a7 (2024-02-02)


### New features:

- Allow a Blog Post to be created inside a subfolder of a Blog #54


### Bug fixes:

- Refactor post_authors indexer to avoid repeated calls to the catalog #56

## 1.0.0a6 (2024-01-29)


### New features:

- - Add indexer for indexing authors from a blog post [@jonaspiterek] #53


## 1.0.0a5 (2023-12-04)


### New features:

- Translate id and title for Authors folder on creation [@jonaspiterek] #50


## 1.0.0a4 (2023-11-28)


### Bug fixes:

- Rename Blog fti to BlogFolder, allowing contents with id blog to be added [@ericof] #42
- Add initial blocks to auto_add_authors_container handler [@jonaspiterek] #43
- Rename blog index and metadata to blog_uid [@ericof] #48


## 1.0.0a3 (2023-11-24)


### New features:

- Control creation of "Authors" folder via registry configuration [@ericof] #34
- Add control panel to configure Blog Settings [@ericof] #36
- Additional information returned on /@authors endpoint [@ericof] #40


### Internal:

- Increase test coverage of the package [@ericof] #38


## 1.0.0a2 (2023-11-23)


### New features:

- Initial Package Structure for Plone 6 [@jonaspiterek] #11
- Blog and Author should be listed on Plone Navigation [@jonaspiterek] #13
- Implement i18n support [@ericof] #17
- Implement `collective.blog.blog_info` behavior [@ericof] #20
- Disable allowing to add Author globally. Fix GS titles [@jonaspiterek] #21
- Add index and metadata for blog post and blog author, Add test for blog author [@jonaspiterek] #28
- Implement collective.blog: Add Author, collective.blog: Add Blog, collective.blog: Add Post permissions [@ericof] #30
- Create folder authors inside a blog [@jonaspiterek] #32


### Documentation:

- Improve README.md [@ericof] #15


## 1.0a1 (2016-02-14)

- Initial release. [@pcdummy]
