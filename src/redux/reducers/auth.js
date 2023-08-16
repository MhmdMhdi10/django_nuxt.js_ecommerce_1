import {
  SIGNUP_SUCCESS,
  SIGNUP_FAIL,
  ACTIVATION_SUCCESS,
  ACTIVATION_FAIL,
  SET_AUTH_LOADING,
  REMOVE_AUTH_LOADING,
  RESET_AUTH_STATE,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  USER_LOADED_SUCCESS,
  USER_LOADED_FAIL,
  AUTHENTICATED_SUCCESS,
  AUTHENTICATED_FAIL,
  REFRESH_SUCCESS,
  REFRESH_FAIL,
  LOGOUT_SUCCESS,
  LOGOUT_FAIL

} from "../actions/types";


const initialState = {
  access: localStorage.getItem('access'),
  refresh: localStorage.getItem('refresh'),
  isAuthenticated: null,
  user: null,
  loading: false,
  type:null,
  message:null,
}

export default function Auth(state = initialState, action) {
  const { type, payload } = action;
  switch(type) {
    case RESET_AUTH_STATE:
      return initialState;
    case SET_AUTH_LOADING:
      return {
        ...state,
        loading: true
      }
    case REMOVE_AUTH_LOADING:
      return {
        ...state,
        loading: false
      }
    case USER_LOADED_SUCCESS:
      return {
        ...state,
        user: payload.user,
        type: payload.type,
        message: payload.message
      }
    case USER_LOADED_FAIL:
      return {
        ...state,
        user: null,
        type: payload.type,
        message: payload.message
      }
    case AUTHENTICATED_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        type: payload.type,
        message: payload.message
      }
    case AUTHENTICATED_FAIL:
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      return {
        ...state,
        isAuthenticated: false,
        access: null,
        refresh: null,
        type: payload.type,
        message: payload.message
      }
    case LOGIN_SUCCESS:
      localStorage.setItem('access', payload.access);
      localStorage.setItem('refresh', payload.refresh);
      return {
        ...state,
        isAuthenticated: true,
        access: localStorage.getItem('access'),
        refresh: localStorage.getItem('refresh'),
        type: payload.type,
        message: payload.message
      }
    case ACTIVATION_SUCCESS:
    case ACTIVATION_FAIL:
      return{
        ...state,
        type: payload.type,
        message: payload.message
      }
    case REFRESH_SUCCESS:
      localStorage.setItem('access', payload.access);
      return {
        ...state,
        access: localStorage.getItem('access'),
        type: payload.type,
        message: payload.message
      }
    case SIGNUP_SUCCESS:
    case SIGNUP_FAIL:
    case LOGIN_FAIL:
    case REFRESH_FAIL:
    case LOGOUT_SUCCESS:
    case LOGOUT_FAIL:
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      return {
        ...state,
        access :null,
        refresh:null,
        isAuthenticated: false,
        user: null,
        type: payload.type,
        message: payload.message
      }
    default:
      return state
  }
}