import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import FooterWithLogo from "../components/navigation/Footer";
import NavbarWithCTAButton from "../components/navigation/Navbar";


export default function Layout(props) {
  return(
    <div className="">
      <NavbarWithCTAButton/>
      <ToastContainer autoClose={8000}/>
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900 p-10 text-gray-900 dark:text-white">{props.children}</main>
      <FooterWithLogo/>
    </div>
  );
}