import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import FooterWithLogo from "../components/navigation/Footer";
import NavbarWithCTAButton from "../components/navigation/Navbar";


export default function Layout(props) {
  return(
    <div className={''}>
      <NavbarWithCTAButton/>
      <ToastContainer autoClose={8000}/>
      {props.children}
      <FooterWithLogo/>
    </div>
  );
}