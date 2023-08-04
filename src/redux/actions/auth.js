import {
  SIGNUP_SUCCESS,
  SIGNUP_FAIL
} from "./types";

import axios from "axios";

export const signup = (phone_number, password, re_password) => async dispatch => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const body = JSON.stringify({
        phone_number,
        password,
        re_password
    });

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/register/`, body, config);

        if (res.status === 201) {
            dispatch({
                type: SIGNUP_SUCCESS,
                payload: res.data
            });
            // dispatch(setAlert('Send email', 'green'))
        } else {
            dispatch({
                type: SIGNUP_FAIL
            });
            // dispatch(setAlert('Error', 'red'));
        }
        // dispatch({
        //     type: REMOVE_AUTH_LOADING
        // });
    } catch (err) {
        dispatch({
            type: SIGNUP_FAIL
        });
        // dispatch({
        //     type: REMOVE_AUTH_LOADING
        // });
        // dispatch(setAlert('Error', 'red'));
    }
}
