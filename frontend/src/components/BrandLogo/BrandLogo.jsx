import { useNavigate } from "react-router-dom";
import { pages } from "../../constants/index";
import Logo from "../../../public/brand-logo.svg?react";

const BrandLogo = () => {
    const navigate = useNavigate();

    return ( 
        <div className="logo-container flex items-center gap-4.75 lg:gap-8.75" onClick={() => pages.home && navigate(pages.home) } >
          <Logo className="size-10 lg:size-13 xl:size-16" />
          <h1 className="text-[22px] md:text-[25px] xl:text-[28px] font-medium">EcoPulse</h1>
        </div>
     );
}
 
export default BrandLogo;