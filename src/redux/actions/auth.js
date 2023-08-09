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

} from "./types";

import { setAlert } from "./alert";

import axios from "axios";

export const resetAuthState = () => ({
  type: RESET_AUTH_STATE,
});

export const signup = (username, phone_number, password, re_password) => async dispatch => {
    dispatch({
        type: SET_AUTH_LOADING
    });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const body = JSON.stringify({
        username,
        phone_number,
        password,
        re_password
    });

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/register/`, body, config);

        if (res.status === 202) {
            dispatch({
                type: SIGNUP_SUCCESS,
                payload: res.data
            });
            dispatch(setAlert(res.data.message , res.data.type));
        } else {
            dispatch({
                type: SIGNUP_FAIL,
                payload: res.data
            });
            dispatch(setAlert(res.data.message , res.data.type));
        }
        dispatch({
            type: REMOVE_AUTH_LOADING,
        });
    } catch (err) {
        let errorMessage = "Server error"; // Default error message
        let errorType = "failure"; // Default error type

        if (err.response && err.response.data) {
            errorMessage = err.response.data.message || errorMessage;
            errorType = err.response.data.type || errorType;
        }
        dispatch({
            type: SIGNUP_FAIL,
            payload: { "type": errorType, "message": errorMessage }
        });
        dispatch({
            type: REMOVE_AUTH_LOADING,
        });
        dispatch(setAlert(errorMessage, errorType));
    }
}


export const activate = (code, username, phone_number, password) => async dispatch => {
    dispatch({
        type: SET_AUTH_LOADING
    });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const body = JSON.stringify({
        code, username, phone_number, password
    });

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/verify/`, body, config);

        if (res.status === 201) {
            dispatch({
                type: ACTIVATION_SUCCESS,
                payload: res.data
            });
            dispatch(setAlert(res.data.message , res.data.type));
        } else {
            dispatch({
                type: ACTIVATION_FAIL,
                payload: res.data
            });
            dispatch(setAlert(res.data.message , res.data.type));
        }
        dispatch({
            type: REMOVE_AUTH_LOADING,
        });
    } catch (err) {
        let errorMessage = "Server error"; // Default error message
        let errorType = "failure"; // Default error type

        if (err.response && err.response.data) {
            errorMessage = err.response.data.message || errorMessage;
            errorType = err.response.data.type || errorType;
        }
        dispatch({
            type: ACTIVATION_FAIL,
            payload: { "type": errorType, "message": errorMessage }
        });
        dispatch({
            type: REMOVE_AUTH_LOADING
        });
        dispatch(setAlert(errorMessage, errorType));
    }
};


export const load_user = () => async dispatch => {
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Authorization': `JWT ${localStorage.getItem('access')}`,
                'Accept': 'application/json'
            }
        };

        try {
            const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/me/`, config);

            if (res.status === 200) {
                dispatch({
                    type: USER_LOADED_SUCCESS,
                    payload: res.data
                });
            } else {
                dispatch({
                    type: USER_LOADED_FAIL,
                    payload: res.data
                });
            }
        } catch (err) {
            let errorMessage = "Server error"; // Default error message
            let errorType = "failure"; // Default error type

            if (err.response && err.response.data) {
                errorMessage = err.response.data.message || errorMessage;
                errorType = err.response.data.type || errorType;
            }
            dispatch({
            type: USER_LOADED_FAIL,
            payload: { "type": errorType, "message": errorMessage }
            });
        }
    } else {
        dispatch({
            type: USER_LOADED_FAIL,
            payload: { "type": 'failure', "message": "user is not logged in" }
        });
    }
}

export const login = (phone_number, password) => async dispatch => {
    dispatch({
        type: SET_AUTH_LOADING
    });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const body = JSON.stringify({
        phone_number,
        password
    });

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/login/`, body, config);
        if (res.status === 200) {
            dispatch({
                type: LOGIN_SUCCESS,
                payload: res.data
            });
            dispatch(load_user());
            dispatch({
                type: REMOVE_AUTH_LOADING,
            });
            dispatch(setAlert(res.data.message , res.data.type));
        } else {
            dispatch({
                type: LOGIN_FAIL,
                payload: res.data
            });
            dispatch({
                type: REMOVE_AUTH_LOADING
            });
            dispatch(setAlert(res.data.message , res.data.type));
        }
    } catch (err) {
        let errorMessage = "Server error"; // Default error message
        let errorType = "failure"; // Default error type

        if (err.response && err.response.data) {
                errorMessage = err.response.data.message || errorMessage;
                errorType = err.response.data.type || errorType;
            }
        dispatch({
            type: SIGNUP_FAIL,
            payload: { "type": errorType, "message": errorMessage }
        });
        dispatch({
            type: REMOVE_AUTH_LOADING
        });
        dispatch(setAlert(errorMessage, errorType));
    }
}