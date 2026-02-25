
import BrandLogo from "../BrandLogo/BrandLogo";

const ButtonLoader = ({ message = "Analyzing local flood data..." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 w-full border-2 border-dashed border-[#C6E2E8] rounded-xl bg-white/50">
      <div className="relative flex items-center justify-center">
        <div className="absolute w-20 h-20 bg-[#008B8B] rounded-full opacity-10 animate-ping"></div>
        <div className="absolute w-16 h-16 bg-[#008B8B] rounded-full opacity-20 animate-pulse"></div>
        <div className="relative">
        <BrandLogo/>
        </div>
      </div>

      <h3 className="mt-8 text-[#008B8B] font-semibold tracking-wide animate-pulse">
        {message}
      </h3>
      <p className="text-gray-400 text-sm mt-2">
        Connecting to risk Analysis engine...
      </p>
    </div>
  );
};

export default ButtonLoader;
