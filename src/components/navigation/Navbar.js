import { Link } from "react-router-dom";
import { Button, Navbar } from 'flowbite-react';
import { Dropdown } from 'flowbite-react';
import { HiLogout, HiViewGrid, HiShoppingCart } from 'react-icons/hi';
// import {DarkThemeToggle, Flowbite } from 'flowbite-react';

import Alert from "../alert";
import { connect } from "react-redux";
import { logout } from "../../redux/actions/auth";

import { useState } from "react";

import { Navigate } from "react-router-dom";

function NavbarWithCTAButton({isAuthenticated, user, logout}) {

    const [redirect, setRedirect] = useState(false);

    const logoutHandler = () => {
        logout()
        setRedirect(true);
    }

    if (redirect) {
        window.location.reload(false);
        return <Navigate to='/'/>;
    }


  return (
    <>
      <Navbar
        fluid
      >
        <Navbar.Brand href="/">
          <img
            alt="Flowbite"
            className="ml-3 h-6 sm:h-9"
            src="https://flowbite.com/docs/images/logo.svg"
          />
          <span className="self-center whitespace-nowrap sm:text-l md:text-xl font-semibold dark:text-white">
            نوین صنعت تسلا
          </span>
        </Navbar.Brand>

        {isAuthenticated ?
          <div className="flex md:order-2 dark:text-gray-400 flex justify-center items-center">
            <Link to={"/cart"} >
              {/*<Button className={" m-0 ml-2 p-0 "}>*/}
                <div className={'flex justify-center items-center ml-3'}>
                  <span className="inline-flex items-center justify-center w-4 h-4 text-xs font-semibold text-blue-800 bg-blue-200 rounded-full">
                    2
                  </span>
                  <svg className="w-8 mt-1 h-8 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 20">
                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 15a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm0 0h8m-8 0-1-4m9 4a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm-9-4h10l2-7H3m2 7L3 4m0 0-.792-3H1"/>
                  </svg>
                </div>
              {/*</Button>*/}
            </Link>
            <div className={'mr-2 ml-4'}>
              <Dropdown
                inline
                label={<svg className="w-10 h-10 text-gray-800 dark:text-white" aria-hidden="true"
                                  xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 19">
                          <path
                            d="M7.324 9.917A2.479 2.479 0 0 1 7.99 7.7l.71-.71a2.484 2.484 0 0 1 2.222-.688 4.538 4.538 0 1 0-3.6 3.615h.002ZM7.99 18.3a2.5 2.5 0 0 1-.6-2.564A2.5 2.5 0 0 1 6 13.5v-1c.005-.544.19-1.072.526-1.5H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h7.687l-.697-.7ZM19.5 12h-1.12a4.441 4.441 0 0 0-.579-1.387l.8-.795a.5.5 0 0 0 0-.707l-.707-.707a.5.5 0 0 0-.707 0l-.795.8A4.443 4.443 0 0 0 15 8.62V7.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.12c-.492.113-.96.309-1.387.579l-.795-.795a.5.5 0 0 0-.707 0l-.707.707a.5.5 0 0 0 0 .707l.8.8c-.272.424-.47.891-.584 1.382H8.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1.12c.113.492.309.96.579 1.387l-.795.795a.5.5 0 0 0 0 .707l.707.707a.5.5 0 0 0 .707 0l.8-.8c.424.272.892.47 1.382.584v1.12a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1.12c.492-.113.96-.309 1.387-.579l.795.8a.5.5 0 0 0 .707 0l.707-.707a.5.5 0 0 0 0-.707l-.8-.795c.273-.427.47-.898.584-1.392h1.12a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5ZM14 15.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Z" />
                        </svg>}
                arrowIcon=""
              >
                <Dropdown.Header>
                  {user &&
                  <span className="block truncate text-sm font-medium text-center">
                    نام کاربری : {user.username}<br/>
                    شماره تلفن: {user.phone_number}
                  </span>
                  }
                </Dropdown.Header>
                <Dropdown.Item icon={HiViewGrid}>
                  <p className={'mr-1'}>پروفایل</p>
                </Dropdown.Item >
                {/*<Dropdown.Item icon={HiCog}>*/}
                {/*  <p className={'mr-1'}>تنظیمات</p>*/}
                {/*</Dropdown.Item>*/}
                <Dropdown.Divider />
                <button onClick={logoutHandler} className={'w-full'}>
                  <Dropdown.Item icon={HiLogout} >
                    خروج
                  </Dropdown.Item>
                </button>
              </Dropdown>
            </div>




            <Navbar.Toggle />



          </div>

          :


          <div className="flex md:order-2">

          {/*<Flowbite>*/}
          {/*  <DarkThemeToggle className={"mr-2"}/>*/}
          {/*</Flowbite>*/}
          <Link to={"/login"}>
            <Button className={"mr-2"} >
              ورود
            </Button>
          </Link>
          <Link to={"/signup"}>
            <Button className={"mx-2"}>
                ثبت نام
            </Button>
          </Link>
          <Navbar.Toggle />
        </div>
        }

        <Navbar.Collapse>
          <Navbar.Link
            className={'ml-6'}
            active
            href="/"
          >
            <p>
              خانه
            </p>
          </Navbar.Link>
          <Navbar.Link href="#">
            محصولات
          </Navbar.Link>
          <Navbar.Link href="/about">
            بلاگ
          </Navbar.Link>
          <Navbar.Link href="#">
            درباره ما
          </Navbar.Link>
          <Navbar.Link href="#">
            تماس با ما
          </Navbar.Link>
        </Navbar.Collapse>
      </Navbar>

      <Alert/>
    </>
  )
}

const mapStateToProps = state => ({
  loading: state.Auth.loading,
  type: state.Auth.type,
  message: state.Auth.message,
  isAuthenticated: state.Auth.isAuthenticated,
  user: state.Auth.user
})

export default connect(mapStateToProps, {
  logout
}) (NavbarWithCTAButton);