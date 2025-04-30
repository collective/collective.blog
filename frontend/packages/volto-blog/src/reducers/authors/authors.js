import GET_AUTHORS from 'volto-blog/actions/authors';

const initialState = {
  loaded: false,
  loading: false,
  error: null,
};

export default function authors(state = initialState, action = {}) {
  switch (action.type) {
    case `${GET_AUTHORS}_PENDING`:
      return {
        ...state,
        error: null,
        loaded: false,
        loading: true,
      };
    case `${GET_AUTHORS}_SUCCESS`:
      return {
        ...state,
        ...action.result,
        error: null,
        loaded: true,
        loading: false,
      };
    case `${GET_AUTHORS}_FAIL`:
      return {
        ...state,
        error: action.error,
        loaded: false,
        loading: false,
      };
    default:
      return state;
  }
}
