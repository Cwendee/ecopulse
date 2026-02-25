import BrandLogo from "../BrandLogo/BrandLogo";

const Loader = ({ message = "Analyzing flood data..." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 w-full animate-in fade-in duration-500">
      <div className="relative">
        <div className="absolute inset-0 rounded-full bg-[#008B8B] opacity-20 animate-ping"></div>

        <div className="relative bg-white p-4 rounded-full shadow-lg border border-[#C6E2E8]">
          <BrandLogo />
        </div>
      </div>

      <p className="mt-6 text-[#008B8B] font-medium typo-lg animate-pulse">
        {message}
      </p>
      <p className="text-gray-500 text-sm">This may take a few seconds.</p>
    </div>
  );
};

export default Loader;
