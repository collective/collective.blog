import type { ConfigType } from '@plone/registry';

import PostView from './components/PostView';

import installBlocks from './config/blocks';

const applyConfig = (config: ConfigType) => {
  installBlocks(config);

  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['en'];
  config.settings.defaultLanguage = 'en';

  config.views.contentTypesViews.Post = PostView;

  return config;
};

export default applyConfig;
