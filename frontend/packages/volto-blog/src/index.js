import PostView from './components/PostView';
import reducers from './reducers';

const applyConfig = (config) => {
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['en'];
  config.settings.defaultLanguage = 'en';

  config.addonReducers = { ...config.addonReducers, ...reducers };

  config.views.contentTypesViews.Post = PostView;

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

  return config;
};

export default applyConfig;
