import React from 'react';
import Carousel from "../components/Carousel/Carousel";
import Layout from "../hocs/Layout";

export default function Home() {
  // Define your carousel items and options
  const carouselItems = [
    {
      position: 0,
      el: (
          <div className="carousel-item-content">
            <h1 className="text-2xl font-bold">Slide 1</h1>
            <p>This is the first slide content.</p>
          </div>
      ),
    },
    {
      position: 1,
      el: (
          <div className="carousel-item-content">
            <h1 className="text-2xl font-bold">Slide 2</h1>
            <p>This is the second slide content.</p>
          </div>
      ),
    },
    {
      position: 2,
      el: (
          <div className="carousel-item-content">
            <h1 className="text-2xl font-bold">Slide 3</h1>
            <p>This is the third slide content.</p>
          </div>
      ),
    },
  ];

  const carouselOptions = {
    defaultPosition: 0,
    interval: 3000,
    indicators: {
      activeClasses: 'bg-blue-500',
      inactiveClasses: 'bg-gray-300 hover:bg-gray-400',
      items: carouselItems,
    },
    onNext: (position) => {
      console.log(`Next slide is shown (Position: ${position})`);
    },
    onPrev: (position) => {
      console.log(`Previous slide is shown (Position: ${position})`);
    },
    onChange: (position) => {
      console.log(`New slide is shown (Position: ${position})`);
    },
  };

  return (
      <Layout>
        {/* Add the Carousel component */}
        <div className="min-h-screen flex items-center justify-center">
          <Carousel items={carouselItems} options={carouselOptions} />
        </div>
      </Layout>
  );
}
