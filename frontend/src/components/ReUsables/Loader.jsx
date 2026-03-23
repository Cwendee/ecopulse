import BrandLogo from "../BrandLogo/BrandLogo";

const Loader = ({
  isLoading = true,
  message = "Eco Pulse is a platform to help communities in Africa receive timely flood alerts and remain prepared for flooding emergencies.",
}) => {
  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-950/80 backdrop-blur-md transition-opacity duration-500">
      <div className="relative flex flex-col items-center gap-6">
        <div className="relative">
          <div className="h-32 w-32 rounded-full border-4 border-t-transparent border-[#296083] animate-spin"></div>
          <div className="absolute inset-0 h-32 w-32 rounded-full border-4 border-t-transparent border-[#3B89BA] animate-[spin_3s_linear_infinite]"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <BrandLogo />
          </div>
        </div>
        <p className="text-xs md:text-xl font-semibold text-white/90 tracking-wide animate-pulse">
          {message}
        </p>
        <div className="h-1.5 w-64 overflow-hidden rounded-full bg-gray-700/50">
          <div className="h-full w-1/3 bg-gradient-to-r from-[#296083] via-[#3B89BA] to-[#296083] animate-[progress_2.5s_linear_infinite]"></div>
        </div>
      </div>
    </div>
  );
};

export default Loader;
