import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // Initial blocks for blogtag content type
  config.blocks.initialBlocks.BlogTag = [
    { '@type': 'title' },
    {
      '@type': 'search',
      listingBodyTemplate: 'summary',
      query: {
        query: [
          {
            i: 'portal_type',
            o: 'plone.app.querystring.operation.selection.any',
            v: ['Post'],
          },
          {
            i: 'blog_tags',
            o: 'plone.app.querystring.operation.currentUID',
            v: '',
          },
        ],
        sort_on: 'effective',
        sort_order: 'descending',
      },
    },
  ];

  // Initial blocks for author content type
  config.blocks.initialBlocks.Author = [
    { '@type': 'title' },
    { '@type': 'slate' },
    {
      '@type': 'listing',
      healine: '',
      headlineTag: 'h2',
      querystring: {
        query: [
          {
            i: 'portal_type',
            o: 'plone.app.querystring.operation.selection.any',
            v: ['Post'],
          },
        ],
        sort_on: 'effective',
        sort_order: 'descending',
      },
      styles: {},
      theme: 'default',
      variation: 'default',
    },
  ];

  return config;
}
