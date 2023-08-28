import React from 'react';
import 'react-responsive-carousel/lib/styles/carousel.min.css'; // Import the carousel styles

import  Carousel  from "../components/carousel/Carousel";
import image from '../img/batman4.png';

import Layout from "../hocs/Layout";

export default function Home() {

  return (
    <Layout>
      <div style={{ backgroundImage: `url(${image})`, backgroundSize:`cover`}} className="px-20  ">
          home <br/>
        home <br/>
        home <br/>


      </div>
    </Layout>
  );
}
