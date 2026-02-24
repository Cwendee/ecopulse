import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../ReUsables/Button";
import BrandLogo from "../BrandLogo/BrandLogo.jsx";
import RightArrow from "../../assets/svgIcons/right-arrow.svg?react";
import Menu from "../../assets/svgIcons/menu.svg?react";
import Cancel from "../../assets/svgIcons/cancel.svg?react";
import { headerNavigation } from "../../constants/index.js";

const Header = () => {
  const navigate = useNavigate();

  const [openMenu, setOpenMenu] = useState(false);

  function handleMenu () {
    setOpenMenu(o => (!o));
  }

  return (
    <header className="header site-container">
      <div className="flex items-center justify-between gap-4 lg:gap-8.75">
        <div className="header__logo">
          <BrandLogo />
        </div>
        <nav className="header__navigation-links hidden md:block ">
          <ul className="flex items-center gap-2 lg:gap-5.25">
            {
              headerNavigation.map((nav, index) => <li 
              key={index} 
              onClick={() => nav.link && navigate(nav.link)}
              className="text-[22px] md:text-[25px] xl:text-[28px] font-medium">
                {nav.title}
              </li>)
            }
          </ul>
        </nav>

        {/* Mobile Navigation Link */}
        <Menu className="size-10 text-[#03A199] md:hidden" onClick={handleMenu} />

        <div className={`fixed inset-0 bg-black/40 transition-opacity z-5  md:hidden ${ openMenu ? "opacity-100" : "opacity-0 pointer-events-none"} `} >

        <aside  className={`fixed top-o right-0 h-screen w-64 bg-[#03A199] shadow-lg transform transition-transform text-white md:hidden ${openMenu ? "translate-x-0" : "tanslate-x-full" } `} >
            <div className="p-4 flex justify-between items-center border-b border-b-white ">
              <span className="font-semibold text-white">Menu</span>
              <Cancel className="size-5" onClick={() => setOpenMenu(false)} />
            </div>

            <div>
              <ul className="px-4 pb-4 flex flex-col gap-3">
                {
                  headerNavigation.map((nav, index) => <li 
                  key={index} 
                  onClick={() => nav.link && navigate(nav.link)}
                  className="text-[22px] font-medium">
                    {nav.title}
                  </li>)
                }
              </ul>
              <Button children={"Receive Flood Alerts"} rightSection={<RightArrow/>} className="btn btn-primary btn-md mx-4" />
            </div>
        </aside>

        </div>

        {/* {
          openMenu && (
            
            
          )
        } */}

        <div className="header__button hidden md:block">
          <Button children={"Receive Flood Alerts"} rightSection={<RightArrow/>} className="btn btn-primary btn-md" />
        </div>
      </div>
    </header>
  );
};

export default Header;
