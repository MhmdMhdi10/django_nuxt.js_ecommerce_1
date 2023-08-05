import { Link } from "react-router-dom";
import Layout from "../../hocs/Layout";

import { useState, useEffect } from 'react'

import {connect} from 'react-redux'
import { signup, activate } from '../../redux/actions/auth'
import {Navigate} from "react-router-dom";


const SignupPage = ({signup, activate}) => {

  useEffect(() => {
    window.scrollTo(0,0)
  }, [])

  const [accountCreated, setAccountCreated] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const [isChecked, setIsChecked] = useState(false);




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

  const onSubmit = e =>{
    e.preventDefault();
    signup(username, phone_number, password, re_password);
    setCodeSent(true);
    // window.scrollTo(0,0)
  }

  const onSubmitVerify = e =>{
    activate(code, username, phone_number, password, re_password)
    setAccountCreated(true)
  }


  if (accountCreated) {
    return <Navigate to="/" />
  }

  return (
    <Layout>
      {codeSent===false ? (<section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
          <Link to="#" className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
            SignUp
          </Link>
          <div
            className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                Create and account
              </h1>
              <form onSubmit={e=>onSubmit(e)} className="space-y-4 md:space-y-6">
                <div>
                  <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your
                    username</label>
                  <input name="username" id="username"
                         value={username}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="username..." required/>
                </div>
                <div>
                  <label htmlFor="phone_number" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your
                    phone number</label>
                  <input name="phone_number" id="phone_number"
                         value={phone_number}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="09*********" required/>
                </div>
                <div>
                  <label htmlFor="password"
                         className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                  <input type="password" name="password" id="password" placeholder="password..."
                         value={password}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         required/>
                </div>
                <div>
                  <label htmlFor="re-password"
                         className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Confirm
                    password</label>
                  <input type="password" name="re_password" id="re_password" placeholder="re_password..."
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
                  <div className="ml-3 text-sm">
                    <label htmlFor="terms" className="font-light text-gray-500 dark:text-gray-300">I accept the <Link
                      className="font-medium text-primary-600 hover:underline dark:text-primary-500" to="#">Terms and
                      Conditions</Link></label>
                  </div>
                </div>
                <button
                  type="submit"
                  className={`w-full text-white font-medium rounded-lg text-sm px-5 py-2.5 text-center focus:outline-none ${
                    isChecked
                      ? 'bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:ring-primary-300'
                      : 'bg-gray-400 cursor-not-allowed'
                  } ${isChecked && 'dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800'}`}
                  disabled={!isChecked}
                >Create
                  an account
                </button>
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  Already have an account? <Link to="/login"
                                                 className="font-medium text-primary-600 hover:underline dark:text-primary-500">Login
                  here</Link>
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
            Otp Code
          </Link>
          <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                A 6 digit code has been sent to you
              </h1>
              <form onSubmit={e=>onSubmitVerify(e)} className="space-y-4 md:space-y-6">
                <div>
                  <label htmlFor="code" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your
                    Code</label>
                  <input name="code" id="code"
                         value={code}
                         onChange={e=>onChange(e)}
                         className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                         placeholder="******" required/>
                </div>
                <button type="submit"
                        className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Create
                  an account
                </button>
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  didn't receive the code?
                  <button className="font-medium text-primary-600 hover:underline dark:text-primary-500">
                    Send again
                  </button>
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

})

export default connect(mapStateToProps, {
  signup,
  activate
}) (SignupPage);
