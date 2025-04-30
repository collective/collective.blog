const GET_AUTHORS = 'GET_AUTHORS';

/**
 * Get service to get authors data.
 * @function getAuthors
 * @param {string} url/@authors Service path.
 * @returns {Object} Action.
 */
export function getAuthors(url) {
  return {
    type: GET_AUTHORS,
    request: {
      op: 'get',
      path: `${url}/@authors`,
    },
  };
}

export default GET_AUTHORS;
