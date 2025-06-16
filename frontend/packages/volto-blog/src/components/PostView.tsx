import FormattedDate from '@plone/volto/components/theme/FormattedDate/FormattedDate';
import PreviewImage from '@plone/volto/components/theme/PreviewImage/PreviewImage';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';
import { FormattedMessage } from 'react-intl';
import { Link } from '@plone/components';

import type { Content, Image } from '@plone/types';

export interface BlogContent extends Content {
  post_tags: Array<{ '@id': string; title: string }>;
  post_authors: Array<{
    '@id': string;
    title: string;
    description: string;
    image_scales: Record<string, Array<Image>> | null;
    image_field: string;
  }>;
}

const PostView = ({ content }: { content: BlogContent }) => {
  return (
    <div id="page-document" className="ui container view-wrapper blogpost-view">
      {content?.effective && (
        <header className="post head-title">
          <span className="day">
            {/* @ts-expect-error */}
            <FormattedDate
              className="day"
              date={content.effective}
              format={{
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              }}
            />
          </span>
        </header>
      )}
      <RenderBlocks content={content} />
      {content?.post_tags?.length > 0 && (
        <span className="tags-container">
          <strong>
            <FormattedMessage id="post_tags" defaultMessage="Tags:" />
          </strong>
          <div className="tags-wrapper">
            {content.post_tags.map((tag) => (
              <Link key={tag['@id']} className="tag-item" href={tag['@id']}>
                {tag.title}
              </Link>
            ))}
          </div>
        </span>
      )}
      {content?.post_authors?.map((author) => (
        <div key={author['@id']}>
          <div className="about-the-author">
            <h2 className="heading">
              <FormattedMessage
                id="About"
                defaultMessage="About {name}"
                values={{ name: author.title }}
              />
            </h2>
            <figure className="author-profile">
              <PreviewImage
                item={author}
                image_field={author.image_field}
                loading="lazy"
                className="headshot"
                alt={author.title}
                width="150"
                height="150"
              />
              <div>
                <figcaption>
                  {author.description && (
                    <p className="description">{author.description}</p>
                  )}
                  <Link href={author['@id']}>
                    <FormattedMessage id="More" defaultMessage="More" />
                  </Link>
                </figcaption>
              </div>
            </figure>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PostView;
