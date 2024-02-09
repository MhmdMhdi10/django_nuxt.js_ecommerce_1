import { Link, Navigate } from "react-router-dom";
import Layout from "../../hocs/Layout";

import { useState, useEffect } from 'react'

import {connect} from 'react-redux'

import { login } from "../../redux/actions/auth";
import { Oval } from "react-loader-spinner";



const LoginPage = ({login, loading, type, message, isAuthenticated}) => {

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isOkayToSend, setIsOkayToSend] = useState(false);
  const [shouldNavigate, setShouldNavigate] = useState(false);

  const [formData, setFormData] = useState({
    phone_number: '',
    password: '',
  })

  const {
    phone_number,
    password,
  } = formData;

  const isPhoneNumberValid = (value) => /^(09\d{9}|(\+98|0)\d{10})$/.test(value);

  const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = e =>{
    e.preventDefault();
    if (isPhoneNumberValid(phone_number)){
      login(phone_number, password)
    }
  }

  useEffect(() => {
    if (isPhoneNumberValid(phone_number)) {
      setIsOkayToSend(true);
    } else {
      setIsOkayToSend(false);
    }
  }, [password, phone_number])




  useEffect(() => {
    if (type==='success' && message==='login successful' && isAuthenticated) {
      setIsLoggedIn(true);
    }
    else {
      setIsLoggedIn(false);
    }
  }, [type, message, isAuthenticated])

  useEffect(() => {
    if (isLoggedIn && !loading) {
      setShouldNavigate(true);
    }
    else {
      setShouldNavigate(false);
    }
  }, [isLoggedIn, loading]);

  if (shouldNavigate) {
    return <Navigate to="/" />
  }


  return (
    <Layout>
      <section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
          <Link to="#" className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
            ورود
          </Link>
          <div
            className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                ورود به حساب کاربری
              </h1>
              <form onSubmit={e => onSubmit(e)} className="space-y-4 md:space-y-6">
                <div>
                  {!isPhoneNumberValid(phone_number) && <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">شماره تلفن همراه شما باید به این اشکال باشد: '۹۸۹xxxxxxxxx' یا '۰۹xxxxxxxxx'.</p>}
                  <label htmlFor="phone_number"
                         className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">شماره تلفن همراه شما:</label>
                  <input name="phone_number" id="phone_number"
                         value={phone_number}
                         onChange={e => onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="*********۰۹" required />
                </div>
                <div>
                  <label htmlFor="password"
                         className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">رمز شما:</label>
                  <input type="password" name="password" id="password" placeholder="رمز..."
                         value={password}
                         onChange={e => onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         required />
                </div>
                {loading ?
                  <button
                    type="submit"
                    className={`flex items-center justify-center w-full text-white font-medium rounded-lg text-sm px-5 py-2.5 text-center focus:outline-none ${
                      isOkayToSend
                        ? 'bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:ring-primary-300'
                        : 'bg-gray-400 cursor-not-allowed'
                    } ${isOkayToSend && 'dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800'}`}
                    disabled={!isOkayToSend}
                  >
                    <Oval height={20} width={20} color={"#fff"} wrapperClass="" />
                    <span style={{ marginLeft: '10px' }}>ورود به حساب کاربری</span>
                  </button>
                  :
                  <button
                    type="submit"
                    className={`flex items-center justify-center w-full text-white font-medium rounded-lg text-sm px-5 py-2.5 text-center focus:outline-none ${
                      isOkayToSend
                        ? 'bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:ring-primary-300'
                        : 'bg-gray-400 cursor-not-allowed'
                    } ${isOkayToSend && 'dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800'}`}
                    disabled={!isOkayToSend}
                  >
                    ورود به حساب کاربری
                  </button>
                }
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  حساب کاربری ندارید؟ <Link to="/login"
                                                 className="font-medium text-primary-600 hover:underline dark:text-primary-500">ایجاد جساب کاربری</Link>
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}

const mapStateToProps = state => ({
  loading: state.Auth.loading,
  type: state.Auth.type,
  message: state.Auth.message,
  isAuthenticated: state.Auth.isAuthenticated,
})

export default connect(mapStateToProps, {
  login
}) (LoginPage);