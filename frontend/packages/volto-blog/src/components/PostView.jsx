import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import FormattedDate from '@plone/volto/components/theme/FormattedDate/FormattedDate';
import PreviewImage from '@plone/volto/components/theme/PreviewImage/PreviewImage';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';
import PropTypes from 'prop-types';
import { useEffect } from 'react';
import { FormattedMessage } from 'react-intl';
import { useDispatch, useSelector } from 'react-redux';

import { getAuthors } from '@plone-collective/volto-blog/actions/authors';

/**
 * PostView view component class.
 * @function PostView
 * @params {object} content Content object.
 * @returns {string} Markup of the component.
 */
const PostView = ({ content, location }) => {
  const dispatch = useDispatch();

  const pathname = location.pathname;
  useEffect(() => {
    dispatch(getAuthors(pathname));
  }, [dispatch, pathname]);
  const authors = useSelector((state) => state.authors);

  return (
    <div id="page-document" className="ui container view-wrapper blogpost-view">
      <header className="post head-title">
        <span className="day">
          <FormattedDate
            className="day"
            date={content?.effective}
            format={{
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            }}
          />
        </span>
      </header>
      <RenderBlocks content={content} />
      <span className="tags-container">
        {content?.post_tags.length > 0 && (
          <>
            <strong>
              <FormattedMessage id="post_tags" defaultMessage="Tags:" />
            </strong>
            <div className="tags-wrapper">
              {content?.post_tags?.map((tag, index) => (
                <UniversalLink key={index} className="tag-item" href={tag.url}>
                  {tag.title}
                </UniversalLink>
              ))}
            </div>
          </>
        )}
      </span>
      {authors?.items?.map(
        (author) =>
          author['@type'] === 'Author' && (
            <div key={author['@id']}>
              <div className="about-the-author">
                <h2 className="heading">
                  <FormattedMessage id="About" defaultMessage="About" />
                  {` ${author?.fullname}`}
                </h2>
                <figure className="author-profile">
                  {author?.image_scales?.preview_image_link && (
                    <PreviewImage
                      item={author}
                      image_field="preview_image_link"
                      loading="lazy"
                      className="headshot"
                      alt={author.fullname}
                      width="150"
                      height="150"
                    />
                  )}
                  <div>
                    <figcaption>
                      <p className="description">{`${author?.description} `}</p>
                    </figcaption>
                    <UniversalLink href={author['@id']}>
                      <button className="ui button">
                        <FormattedMessage id="More" defaultMessage="More" />
                      </button>
                    </UniversalLink>
                  </div>
                </figure>
              </div>
            </div>
          ),
      )}
    </div>
  );
};

/**
 * Property types.
 * @property {Object} propTypes Property types.
 * @static
 */
PostView.propTypes = {
  content: PropTypes.shape({
    title: PropTypes.string,
    description: PropTypes.string,
    text: PropTypes.shape({
      data: PropTypes.string,
    }),
  }).isRequired,
};

export default PostView;
