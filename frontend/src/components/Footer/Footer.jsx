import { Link } from "react-router-dom";
import routes from "../../constants/routes";
import brandLogo from "../../assets/svgIcons/footer-logo.svg";

const Footer = () => {
  return (
    <div className="border border-y-[#296083] typo-base">
      <div className="site-container py-4 md:py-12 md:flex justify-between items-start">
        <div className="flex gap-8.75 items-center">
          <img src={brandLogo} alt="Bramd Logo" className="w-12 h-12" />
          <h1 className="typo-xl">Eco Pulse</h1>
        </div>
        <div className="grid grid-cols-2 gap-10.75 justify-between mt-4 md:mt-0">
          <div>
            {[
              {
                text: "Home",
                to: routes.main.home(),
              },
              {
                text: "Resources",
                to: routes.main.resources(),
              },
              {
                text: "Map",
              },
              {
                to: routes.main.about(),
                text: "About Us",
              },
            ].map((l, i) => (
              <Link
                key={i}
                to={l.to}
                className="typo-base cursor-pointer flex flex-col"
              >
                {l.text}
              </Link>
            ))}
          </div>
          <div>
            {[
              {
                text: "Contact Us",
                to: routes.main.contact(),
              },
              {
                text: "FAQs",
                to: routes.main.faq(),
              },
            ].map((l, i) => (
              <Link
                key={i}
                to={l.to}
                className="typo-base cursor-pointer flex flex-col"
              >
                {l.text}
              </Link>
            ))}
          </div>
        </div>
      </div>
      <div className="text-sm">
        <div className="flex items-center mx-auto justify-center">
          © {new Date().getFullYear()} Ecopulse | Tech4dev Women Techsters
          Capstone Project
        </div>
      </div>
    </div>
  );
};

export default Footer;
