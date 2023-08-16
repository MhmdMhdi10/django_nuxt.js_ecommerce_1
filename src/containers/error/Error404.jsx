import React from 'react';
import Layout from "../../hocs/Layout";
import { Link } from 'react-router-dom';
import { Button } from 'flowbite-react';

const Error404 = () => {
  return (
    <Layout>
      <div className=" w-full px-16 md:px-0 h-screen flex items-center justify-center">
          <div className="flex flex-col items-center justify-center px-4 md:px-8 lg:px-24 py-8 rounded-lg shadow-2xl">
              <p className="text-6xl md:text-7xl lg:text-9xl font-bold tracking-wider text-gray-300">404</p>
              <p className="text-2xl md:text-3xl lg:text-5xl font-bold tracking-wider text-gray-500 mt-4">صفحه پیدا نشد</p>
              <p className="text-gray-500 mt-4 pb-4 text-center"> پوزش. صفحه مورد نظر شما پیدا نشد</p>

              <Link to="/" className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-gray-100 rounded transition duration-150" title="Return Home">
                  <Button className={'mt-6'}>
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd"></path>
                      </svg>
                      <span>بازگشت به خانه</span>
                  </Button>
              </Link>

          </div>
      </div>
    </Layout>
  );
};

export default Error404;
