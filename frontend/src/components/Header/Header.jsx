import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import Button from "../ReUsables/Button";
import BrandLogo from "../BrandLogo/BrandLogo.jsx";
import RightArrow from "../../assets/svgIcons/right-arrow.svg?react";
import Menu from "../../assets/svgIcons/menu.svg?react";
import Cancel from "../../assets/svgIcons/cancel.svg?react";
import { headerNavigation } from "../../constants/index.js";
import SignUp from "../../pages/SignUp.jsx";
import Modal from "../ReUsables/Modal.jsx";
import clsx from "clsx";


const Header = () => {
  const navigate = useNavigate();
  const [openMenu, setOpenMenu] = useState(false);
  const [modal, setModal] = useState(false);

  function handleMenu() {
    setOpenMenu((o) => !o);
  }

  return (
    <header className=" fixed top-0 left-0 right-0 z-50 bg-white">
      <div className="site-container flex items-center justify-between gap-4 lg:gap-8.75">
        <div className="header__logo">
          <BrandLogo />
        </div>
        <nav className="header__navigation-links hidden lg:block ">
          <ul className="flex items-center gap-2 lg:gap-5.25">
            {headerNavigation.map((nav, index) => (
              <NavLink
                key={index}
                end={nav.link === "/"}
                to={nav.link}
                className={({ isActive }) =>
                  clsx(
                    "text-[16px] md:text-[18px] xl:text-[24px] font-medium cursor-pointer hover:text-[#296083]",
                    isActive &&
                      "border-b-2 border-[#03A199] transition-all duration-300",
                  )
                }
              >
                {nav.title}
              </NavLink>
            ))}
          </ul>
        </nav>

        {/* Mobile Navigation Link */}
        <Menu
          className="size-10 text-[#03A199] lg:hidden"
          onClick={handleMenu}
        />

        <div
          className={`fixed inset-0 bg-black/40 transition-opacity z-5  lg:hidden ${openMenu ? "opacity-100" : "opacity-0 pointer-events-none"}`}
          onClick={() => setOpenMenu(false)}
        >
          <aside
            className={`fixed top-o right-0 h-screen w-64 bg-[#03A199] shadow-lg transform transition-transform text-white lg:hidden ${openMenu ? "translate-x-0" : "tanslate-x-full"} `}
          >
            <div className="p-4 flex justify-between items-center border-b border-b-white ">
              <span className="font-semibold text-white">Menu</span>
              <Cancel className="size-5" onClick={() => setOpenMenu(false)} />
            </div>

            <div>
              <ul className="px-4 pb-4 flex flex-col gap-3">
                {headerNavigation.map((nav, index) => (
                  <li
                    key={index}
                    onClick={() => nav.link && navigate(nav.link)}
                    className="text-[22px] font-medium"
                  >
                    {nav.title}
                  </li>
                ))}
              </ul>
              <Button
                children={"Receive Flood Alerts"}
                rightSection={<RightArrow />}
                className="btn btn-primary btn-md mx-4"
                onClick={() => setModal(true)}
              />
            </div>
          </aside>
        </div>

        <div className="header__button hidden lg:block">
          <Button
            children={"Receive Flood Alerts"}
            rightSection={<RightArrow />}
            className="btn btn-primary btn-md"
            onClick={() => setModal(true)}
          />
        </div>
      </div>
      <Modal opened={modal} onClose={() => setModal(false)}>
        <SignUp onClose={() => setModal(false)} />
      </Modal>
    </header>
  );
};

export default Header;
