import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Landing from "./pages/Landing";
import NotFound from "./pages/NotFound";
import Resource from "./pages/Resource";
import routes from "./constants/routes";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Faq from "./pages/Faq";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route index element={<Landing />} />
          <Route path={routes.main.resources()} element={<Resource />} />\
          <Route path={routes.main.about()} element={<About />} />
          <Route path={routes.main.contact()} element={<Contact />} />
          <Route path={routes.main.faq()} element={<Faq/>} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
