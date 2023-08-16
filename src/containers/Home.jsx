import React from 'react';
import 'react-responsive-carousel/lib/styles/carousel.min.css'; // Import the carousel styles
import { Carousel } from 'react-responsive-carousel';
import toolsImage from '../img/tools.jpg';
import image1 from '../img/tools.jpg';
import image2 from '../img/tools2.jpg';
import Layout from "../hocs/Layout";

export default function Home() {
  return (
    <Layout>
    <div className="">
      <div className="max-w-5xl mx-auto py-12">
        <h1 className="text-3xl font-semibold mb-8 text-center">Image Carousel Example</h1>
        <Carousel
          showThumbs={false}
          infiniteLoop={true}
          autoPlay={true}
          interval={3000}
          transitionTime={500}
        >
          <div>
            <img src={toolsImage} alt="Tools" />
            <p className="legend">Tools</p>
          </div>
          <div>
            <img src={image1} alt="Image 1" />
            <p className="legend">Image 1</p>
          </div>
          <div>
            <img src={image2} alt="Image 2" />
            <p className="legend">Image 2</p>
          </div>
        </Carousel>
      </div>
    </div>
      </Layout>
  );
}
