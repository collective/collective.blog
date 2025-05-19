import type { ConfigType } from '@plone/registry';

import PostView from './components/PostView';

import installBlocks from './config/blocks';

const applyConfig = (config: ConfigType) => {
  installBlocks(config);

  config.views.contentTypesViews.Post = PostView;

  return config;
};

export default applyConfig;
