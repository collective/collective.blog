import PostView from './components/PostView';
import reducers from './reducers';

const applyConfig = (config) => {
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['en'];
  config.settings.defaultLanguage = 'en';

  config.addonReducers = { ...config.addonReducers, ...reducers };

  config.views.contentTypesViews.Post = PostView;

  return config;
};

export default applyConfig;
