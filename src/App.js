import { Provider } from "react-redux";
import store from "./store";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Error404 from "./containers/error/Error404";
import Home from "./containers/Home";
import SignupPage from "./containers/auth/SignUp";
import LoginPage from "./containers/auth/Login";


function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path={'*'} element={<Error404/>} />
          <Route exact path={'/'} element={<Home/>} />
          <Route exact path={'/signup'} element={<SignupPage/>}/>
          <Route exact path={'/login'} element={<LoginPage/>}/>
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;
