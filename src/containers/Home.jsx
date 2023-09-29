import React from 'react';
import 'react-responsive-carousel/lib/styles/carousel.min.css'; // Import the carousel styles

import image from '../img/batman4.png';

import Layout from "../hocs/Layout";

export default function Home() {

  return (
    <Layout>
      <div style={{ backgroundImage: `url(${image})`, backgroundSize:`cover`}} className="px-20  ">
        <div className={"mr-[100px]"}>
          <h1>home</h1> <br/>
          home <br/>
          home <br/>
        </div>

      </div>
    </Layout>
  );
}
