import { Link } from "react-router-dom";
import { Button, Navbar } from 'flowbite-react';
// import {DarkThemeToggle, Flowbite } from 'flowbite-react';

export default function NavbarWithCTAButton() {

  return (

      <Navbar
        fluid
      >
        <Navbar.Brand href="/">
          <img
            alt="Flowbite"
            className="mr-3 h-6 sm:h-9"
            src="https://flowbite.com/docs/images/logo.svg"
          />
          <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
            Flowbite React
          </span>
        </Navbar.Brand>
        <div className="flex md:order-2">
          {/*<Flowbite>*/}
          {/*  <DarkThemeToggle className={"mr-2"}/>*/}
          {/*</Flowbite>*/}
          <Link to={"/signup"}>
            <Button className={"mr-2"} >
              Login
            </Button>
          </Link>
          <Link to={"/signup"}>
            <Button className={"mr-2"}>
                SignUp
            </Button>
          </Link>
          <Navbar.Toggle />
        </div>
        <Navbar.Collapse>
          <Navbar.Link
            active
            href="/"
          >
            <p>
              Home
            </p>
          </Navbar.Link>
          <Navbar.Link href="/about">
            About
          </Navbar.Link>
          <Navbar.Link href="#">
            Services
          </Navbar.Link>
          <Navbar.Link href="#">
            Pricing
          </Navbar.Link>
          <Navbar.Link href="#">
            Contact
          </Navbar.Link>
        </Navbar.Collapse>

      </Navbar>
  )
}


