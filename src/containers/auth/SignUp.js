import { Link } from "react-router-dom";
import Layout from "../../hocs/Layout";

import { useState, useEffect } from 'react'

import {connect} from 'react-redux'
import { signup, activate, resetAuthState } from "../../redux/actions/auth";
import {Navigate} from "react-router-dom";
import { Oval } from "react-loader-spinner";



const SignupPage = ({signup, activate, loading, type, message, resetAuthState}) => {

  const [timer, setTimer] = useState(0);



  // useEffect(() => {
  //   window.scrollTo(0,0)
  // }, [])

  const [accountCreated, setAccountCreated] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const [isChecked, setIsChecked] = useState(false);
  const [shouldNavigate, setShouldNavigate] = useState(false);
  const [isOkayToSend, setIsOkayToSend] = useState(false);


  const isUsernameValid = (value) => value.length >= 4;
  const isCodeValid = (value) => value.length >= 6;
  const isPhoneNumberValid = (value) => /^(09\d{9}|(\+98|0)\d{10})$/.test(value);
  const isPasswordValid = (value) => /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{4,}$/.test(value);
  const isRePasswordValid = (value, value2) => value === value2;

  const startTimer = () => {
    setTimer(125); // Set the timer to 120 seconds
  };

  useEffect(() => {
    let interval;

    if (timer > 0) {
      interval = setInterval(() => {
        setTimer(prevTimer => prevTimer - 1);
      }, 1000); // Decrease the timer every second
    } else {
      clearInterval(interval);
    }

    // Clean up the interval when the component unmounts
    return () => clearInterval(interval);
  }, [timer]);

  useEffect(() => {
    if (codeSent) {
      startTimer()
    }
  }, [codeSent])


  const [formData, setFormData] = useState({
    username: '',
    phone_number: '',
    password: '',
    re_password: '',
    code:''
  })

  const {
    username,
    phone_number,
    password,
    re_password,
    code,
  } = formData;

  const handleCheckboxChange = (event) => {
    setIsChecked(event.target.checked);
  };

  const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = e => {
    e.preventDefault();
    if (isUsernameValid(username) && isPhoneNumberValid(phone_number) && isPasswordValid(password)) {
      signup(username, phone_number, password, re_password);
    }

    // window.scrollTo(0,0)
  }

  const onSubmitVerify = e =>{
    e.preventDefault();
    if (isUsernameValid(username) && isPhoneNumberValid(phone_number) && isPasswordValid(password) && isCodeValid(code)) {
      activate(code, username, phone_number, password, re_password);
    }
  }

    useEffect(() => {
      if (type === "success" && message==="we sent you a code"){
          setCodeSent(true);
      }
    }, [type, message]);


    useEffect(() => {
        if (type==="success" && message==="your account has been created") {
          setAccountCreated(true);
        }
    }, [type, message]);

    useEffect(() => {
      if (accountCreated && !loading) {
        setTimeout(()=> {
          setShouldNavigate(true);
        }, 5000)
      }
    }, [accountCreated, loading]);

    useEffect(() => {
      if (isChecked && isPasswordValid(password) && isUsernameValid(username) && isRePasswordValid(password, re_password) && isPhoneNumberValid(phone_number)){
        setIsOkayToSend(true);
      } else {
        setIsOkayToSend(false);
      }
    }, [password, username, re_password, phone_number, isChecked, isOkayToSend])

    if (shouldNavigate) {
      resetAuthState();
      return <Navigate to="/" />
    }

  return (
    <Layout>
      {(codeSent===true) ? (<section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
          <Link to="#" className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
            رمز موقت
          </Link>
          <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                یک رمز ۶ رقمی برای شما ارسال شد
              </h1>
              <form onSubmit={e=>onSubmitVerify(e)} className="space-y-4 md:space-y-6">
                <div>
                  {!isCodeValid(code) && <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">رمز باید ۶ رقم باشد</p>}
                  <label htmlFor="code" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    رمز شما:</label>
                  <input name="code" id="code"
                         value={code}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="******" required/>
                </div>
                <button type="submit"
                        className="flex items-center justify-center w-full text-white font-medium rounded-lg text-sm px-5 py-2.5 text-center focus:outline-none bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:ring-primary-300">
                  {loading ? (
                    <Oval height={20} width={20} color={"#fff"} wrapperClass="" />
                  ) : (
                    <></> // or any other content you want to render when loading is false
                  )
                  }
                  <span style={{ marginLeft: '10px' }}>ایجاد حساب کاربری</span>
                </button>
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  رمز را دریافت نکردید ؟&nbsp;
                  {timer === 0 ? (
                  <button  onClick={() => {startTimer(); signup(username, phone_number, password, re_password);}} className="font-medium text-primary-600 hover:underline dark:text-primary-500">
                    ارسال دوباره
                  </button>
                    ) : (
                  <button disabled className="font-medium hover:underline text-gray-400 cursor-not-allowed">
                    ارسال دوباره
                  </button>
                    )}
                  <p>ارسال دوباره در {timer} ثانیه </p>
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>)
        :
        (<section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
          <Link to="#" className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
            ثبت نام
          </Link>
          <div
            className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                ایجاد حساب کاربری
              </h1>
              <form onSubmit={e=>onSubmit(e)} className="space-y-4 md:space-y-6">
                <div>
                  {!isUsernameValid(username) && <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">نام کاربری شما باید بیش از ۴ کاراکتر باشد</p>}
                  <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    نام کاربری شما:
                  </label>
                  <input name="username" id="username"
                         value={username}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="نام کاربری..." required/>
                </div>
                <div>
                  {!isPhoneNumberValid(phone_number) && <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">شماره تلفن همراه شما باید به این اشکال باشد: '۹۸۹xxxxxxxxx' یا '۰۹xxxxxxxxx'.</p>}<br/>
                  <label htmlFor="phone_number" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    شماره تلفن همراه شما:</label>
                  <input name="phone_number" id="phone_number"
                         value={phone_number}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="*********۰۹" required/>
                </div>
                <div>
                  {!isPasswordValid(password) && <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">رمز شما باید بیشتر از ۴ کاراکتر حاوی عدد و حروف باشد</p>}
                  <label htmlFor="password"
                         className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"> رمز شما: </label>
                  <input type="password" name="password" id="password" placeholder="رمز..."
                         value={password}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         required/>
                </div>
                <div>
                  {!isRePasswordValid(re_password, password) && <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">رمز و تکرار رمز باید برابر باشند</p>}
                  <label htmlFor="re-password"
                         className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    تکرار رمز شما: </label>
                  <input type="password" name="re_password" id="re_password" placeholder="تکرار رمز..."
                         value={re_password}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         required/>
                </div>
                <div className="flex items-start">
                  <div className="flex items-center h-5">
                    <input id="terms" aria-describedby="terms" type="checkbox"
                           className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
                           onChange={handleCheckboxChange}
                           required/>
                  </div>
                  <div className="mr-3 text-sm">
                    <label htmlFor="terms" className="font-light text-gray-500 dark:text-gray-300">با <Link
                      className="font-medium text-primary-600 hover:underline dark:text-primary-500" to="#">شرایط و مقررات&nbsp;</Link>
                    موافق هستم
                    </label>
                  </div>
                </div>
                {loading ? <button
                    type="submit"
                    className={`flex items-center justify-center w-full text-white font-medium rounded-lg text-sm px-5 py-2.5 text-center focus:outline-none ${
                      isOkayToSend
                        ? 'bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:ring-primary-300'
                        : 'bg-gray-400 cursor-not-allowed'
                    } ${isOkayToSend && 'dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800'}`}
                    disabled={!isOkayToSend}
                  >
                    <Oval height={20} width={20} color={"#fff"} wrapperClass="" />
                    <span style={{ marginLeft: '10px' }}>Create an account</span>
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
                  >ایجاد حساب کاربری
                </button>
                }
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  حساب کاربری دارید؟&nbsp;
                  <Link to="/login" className="font-medium text-primary-600 hover:underline dark:text-primary-500">
                    ورود به حساب کاربری
                  </Link>
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>)
      }
    </Layout>
  );
};

const mapStateToProps = state => ({
  loading: state.Auth.loading,
  type: state.Auth.type,
  message: state.Auth.message,
})

export default connect(mapStateToProps, {
  signup,
  activate,
  resetAuthState,
}) (SignupPage);
