
import 'react-responsive-carousel/lib/styles/carousel.min.css'; // Import the carousel styles

import image from '../img/batman4.png';

import Layout from "../hocs/Layout";

export default function Home() {

  return (

      <div style={{ backgroundImage: `url(${image})`, backgroundSize:`cover`}} className="px-20">
        <div className={"mx-20 text-white"}>
          <h1 className={'mr-5'}>home</h1> <br/>
          home <br/>
          home <br/>
        </div>

      </div>

  );
}
