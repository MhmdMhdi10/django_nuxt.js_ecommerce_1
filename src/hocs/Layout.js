import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import FooterWithLogo from "../components/navigation/Footer";
import NavbarWithCTAButton from "../components/navigation/Navbar";
import { connect } from "react-redux";

import { check_authentication, load_user, refresh } from "../redux/actions/auth";
import { useEffect } from "react";


function Layout(props) {

  useEffect(() => {

    props.refresh();
    props.check_authentication();
    props.load_user();
  },[])

  return(
    <div dir="rtl">
      <NavbarWithCTAButton/>
      <ToastContainer autoClose={8000}/>
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900  text-gray-900 dark:text-white">{props.children}</main>
      <FooterWithLogo/>
    </div>
  );
}

const mapStateToProps = state => ({
  loading: state.Auth.loading,
  type: state.Auth.type,
  message: state.Auth.message,
  isAuthenticated: state.Auth.isAuthenticated,
  // user: state.Auth.user
})

export default connect(mapStateToProps, {
  check_authentication, load_user, refresh
}) (Layout);