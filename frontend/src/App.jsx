import { BrowserRouter, Route, Routes } from "react-router-dom";
import "leaflet/dist/leaflet.css";
import MainLayout from "./layouts/MainLayout";
import Landing from "./pages/Landing";
import NotFound from "./pages/NotFound";
import Resource from "./pages/Resource";
import routes from "./constants/routes";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Faq from "./pages/Faq";
import CommunityPage from "./pages/CommunityPage";
import EmergencyPrep from "./pages/EmergencyPrep";
import LocalPage from "./pages/LocalPage";
import Map from "./pages/Map";
import SignUp from "./pages/SignUp";
import ChatBot from "./pages/ChatBot";
import Result from "./pages/Result";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route index element={<Landing />} />
          <Route path={routes.main.resources()} element={<Resource />} />
          <Route path={routes.main.about()} element={<About />} />
          <Route path={routes.main.contact()} element={<Contact />} />
          <Route path={routes.main.faq()} element={<Faq />} />
          <Route path={routes.main.support()} element={<CommunityPage />} />
          <Route path={routes.main.emergency()} element={<EmergencyPrep />} />
          <Route path={routes.main.localResources()} element={<LocalPage />} />
          <Route path={routes.main.map()} element={<Map />} />
          <Route path={routes.main.signup()} element={<SignUp />} />
          <Route path={routes.main.chatbot()} element={<ChatBot />} />
          <Route path={routes.main.result()} element={<Result />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
