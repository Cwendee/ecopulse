import { Link } from "react-router-dom";
import Logo from "../../../public/brand-logo.svg?react";

const BrandLogo = () => {
  return (
    <Link
      to="/"
      className="logo-container flex items-center gap-4.75 lg:gap-8.75"
    >
      <Logo className="size-10 lg:size-13 xl:size-16" />
      <h1 className="text-[22px] md:text-[25px] xl:text-[28px] font-medium">
        EcoPulse
      </h1>
    </Link>
  );
};

export default BrandLogo;
