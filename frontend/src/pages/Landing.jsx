import { ResourcesData } from "../constants";
import { useNavigate } from "react-router-dom";
import polygon from "../assets/svgIcons/polygon.svg";
import Button from "../components/ReUsables/Button";
import HeroS from "../assets/images/Hero-s.png";
import HeroM from "../assets/images/Hero-m.png";
import HeroL from "../assets/images/Hero-l.png";
import RightArrow from "../assets/svgIcons/right-arrow.svg?react";
import { useState } from "react";
import { useCountries, useFloodAnalysis, useRegions } from "../hooks/APIHooks";
import Modal from "../components/ReUsables/Modal";
import ButtonLoader from "../components/ReUsables/ButtonLoader";
import routes from "../constants/routes";
import { HiChevronDown } from "react-icons/hi";
import lowIcon from "../assets/svgIcons/status-low-icon.png"
import moderateIcon from "../assets/svgIcons/status-moderate-icon.svg";
import highIcon from "../assets/svgIcons/status-high-icon.svg";

const Landing = () => {
  const navigate = useNavigate();
  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedRegionId, setSelectedRegionId] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const { data: countryData } = useCountries();
  const { data: regionData } = useRegions(selectedCountry);
  const { riskQuery, aiQuery } = useFloodAnalysis(selectedRegionId, showModal);

  const getRiskStyles = (level) => {
    switch (level?.toLowerCase()) {
      case "low":
        return {
          border: "border-[#4CBB17]",
          bg: "bg-[#F8F8FF]",
          text: "text-[#4CBB17]",
          icon: lowIcon,
        };
      case "moderate":
        return {
          border: "border-[#FE5A1D]",
          bg: "bg-[#F8F8FF]",
          text: "text-[#FE5A1D]",
          icon: moderateIcon,
        };
      case "high":
        return {
          border: "border-[#CE2029]",
          bg: "bg-[#F8F8FF]",
          text: "text-red-600",
          icon: highIcon,
        };
      default:
        return {
          border: "border-gray-300",
          bg: "bg-gray-50",
          text: "text-gray-600",
          icon: "ℹ️",
        };
    }
  };

  const isProcessing = riskQuery.isFetching || aiQuery.isFetching;

  const handleSearch = () => {
    if (selectedRegionId) {
      setShowModal(true);
    }
  };

  return (
    <section className="site-container">
      <section className="hero my-4">
        <div className="bg-[#008B8B] border border-[#008B8B] rounded-lg flex flex-col justify-center items-center md:px-3 md:pt-4 pb-4">
          <div className="relative h-55 pb-6 flex flex-col justify-center items-center md:h-auto">
            <picture className="w-full rounded-lg">
              <source media="(min-width: 1024px)" srcSet={HeroL} />
              <source media="(min-width: 768px)" srcSet={HeroM} />
              <img src={HeroS} alt="flooded area with a water over road sign" />
            </picture>
            <h1 className="text-[#F8F8FF] typo-4xl text-center font-medium py-6 absolute top-0 bg-[#008B8B]/20 h-full md:relative md:h-auto">
              {" "}
              FLOOD ALERTS AND PREPAREDNESS YOU CAN TRUST ACROSS AFRICA{" "}
            </h1>
          </div>
          <input
            type="email"
            placeholder="Enter your email to receive early flood warnings"
            className="w-full bg-white rounded-[20px] py-1.75 px-5 "
          />{" "}
          <br />
          <Button
            children={"Receive emergency flood alerts"}
            rightSection={<RightArrow />}
            className="btn btn-primary btn-md"
          />
        </div>
      </section>

      <section className="flood-risk-section bg-[#C6E2E8] rounded-xl mt-20 mb-12">
        <div className=" flex flex-col justify-center items-center gap-6 section ">
          <h2 className="typo-3xl mb-2 text-center ">
            Check for flood risk in your area
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-6">
            <div className="relative w-full">
              <select
                value={selectedCountry}
                onChange={(e) => {
                  setSelectedCountry(e.target.value);
                  setIsSearching(false);
                }}
                className="form-input peer focus:outline-none transition-all appearance-none pr-10 cursor-pointer"
              >
                <option value="" disabled hidden>
                  Select Country
                </option>
                {countryData?.countries.map((country) => (
                  <option key={country.code} value={country.code}>
                    {country.name}
                  </option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                <HiChevronDown className="h-5 w-5 text-gray-500" />
              </div>
            </div>
            <div className="relative w-full">
              <select
                value={selectedRegionId}
                onChange={(e) => {
                  setSelectedRegionId(e.target.value);
                  setIsSearching(false);
                }}
                className="form-input w-full appearance-none pr-10 cursor-pointer"
              >
                <option value="">Select Region</option>
                {regionData?.regions.map((r) => (
                  <option key={r.region_id} value={r.region_id}>
                    {r.region_name}
                  </option>
                ))}
              </select>

              <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                <HiChevronDown className="h-5 w-5 text-gray-500" />
              </div>
            </div>
          </div>

          {/* <Button
            children={"Use My Current Location"}
            rightSection={<LocationPointer />}
            className="btn btn-md btn-accent "
          /> */}

          <div className="flex gap-3 md:gap-5 ">
            <Button
              onClick={handleSearch}
              disabled={!selectedRegionId}
              className="btn btn-primary btn-md"
            >
              Check Flood Risk
            </Button>

            <Button
              onClick={() => navigate(routes.main.map())}
              children={"View Full Map"}
              rightSection={<RightArrow />}
              className="btn btn-md btn-accent "
            />
          </div>
        </div>
      </section>

      <section className="space-y-9.5 section">
        <h2 className="typo-3xl text-center">Find Resources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 xl:gap-20">
          {ResourcesData.map((item, index) => (
            <div
              key={index}
              className="card hover-lift"
              onClick={() => item.link && navigate(item.link)}
            >
              <div className="bg-[#03A199] py-px px-0.75 rounded-xl h-8.25 w-9.25 flex justify-center items-center">
                <img src={item.icon} />
              </div>
              <h1 className="typo-xl">{item.title}</h1>
              <p className="typo-base">{item.description}</p>
            </div>
          ))}
        </div>{" "}
      </section>
      <section className="py-6">
        <div className="relative">
          <div className="bg-[#008B8B] rounded-[18px] py-8 px-5 text-white space-y-2 md:space-y-3">
            <h1 className="typo-2xl">Need more guidance?</h1>
            <p className="typo-lg">
              Chat with Eco, the friendly chatbot for instant help with
              preparation, safety, and recovery.
            </p>
          </div>

          <div className="absolute -bottom-6 right-6 ">
            <img
              src={polygon}
              alt="polygon shape"
              className="w-18 h-16 md:w-29.75 md:h-26"
            />
          </div>
        </div>
        <div className="flex justify-center mx-auto py-8">
          <Button className="btn btn-primary btn-md">Start chat</Button>
        </div>
      </section>
      <Modal
        opened={showModal}
        onClose={() => setShowModal(false)}
        title="EcoPulse Flood Analysis Report"
      >
        <div className="flex flex-col justify-center p-2">
          {isProcessing && (
            <div className="flex flex-col items-center justify-center py-16 animate-pulse">
              <ButtonLoader message="EcoPulse AI is calculating risk factors..." />
            </div>
          )}

          {(riskQuery.isError || aiQuery.isError) && !isProcessing && (
            <div className="flex flex-col justify-center space-y-4 text-center animate-in fade-in zoom-in duration-300">
              <div className="bg-[#F8F8FF] p-4 rounded-xl border-4px border-[#296083]">
                <h4 className="typo-2xl">Region Not Supported Yet</h4>
                <h3 className="typo-lg">
                  Flood risk data not available for this area right now. Explore
                  nearby regions for flood-risk updates.
                </h3>
                <Button
                  onClick={() => navigate(routes.main.map())}
                  className="btn btn-primary btn-md "
                  rightSection={<RightArrow />}
                >
                  Open map
                </Button>
                <p className="typo-lg">
                  Or view general preparedness guidance and emergency steps.
                </p>{" "}
                <Button
                  className="btn btn-accent btn-md"
                  rightSection={<RightArrow />}
                >
                  View guidance steps
                </Button>
              </div>{" "}
            </div>
          )}

          {!isProcessing &&
            riskQuery.data &&
            (() => {
              const risk = riskQuery.data.risk_level;
              const styles = getRiskStyles(risk);

              return (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <div
                    className={`p-3 md:p-6 rounded-xl border-[3px] ${styles.border} ${styles.bg} text-center mb-8 transition-all duration-300`}
                  >
                    <div className="flex justify-center mx-auto">
                      <img src={styles.icon} alt={`${styles.text} risk icon`} />
                    </div>

                    <h3 className="typo-xl">Flood Risk Level</h3>
                    <span className={`typo-3xl font-bold ${styles.text}`}>
                      {risk} Risk
                    </span>
                    <div className="">
                      <div className="typo-base">
                        {aiQuery.data?.explanation
                          ? aiQuery.data.explanation
                          : "No detailed AI analysis was provided for this specific region."}
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-center items-center space-x-5 mx-auto">
                    <Button
                      onClick={() => navigate(routes.main.emergency())}
                      className="btn btn-primary btn-md shadow-lg shadow-[#008B8B]/20"
                    >
                      Emergency Prep
                    </Button>
                    <Button
                      onClick={() => navigate(routes.main.resources())}
                      className="btn btn-accent btn-md shadow-lg shadow-[#008B8B]/20"
                    >
                      View Resources
                    </Button>
                  </div>
                </div>
              );
            })()}
        </div>
      </Modal>
    </section>
  );
};

export default Landing;
