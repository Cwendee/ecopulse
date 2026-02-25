import { ResourcesData } from "../constants";
import { useNavigate } from "react-router-dom";
import { pages } from "../constants/index";
import polygon from "../assets/svgIcons/polygon.svg";
import Button from "../components/ReUsables/Button";
import HeroS from "../assets/images/Hero-s.png";
import HeroM from "../assets/images/Hero-m.png";
import HeroL from "../assets/images/Hero-l.png";
import RightArrow from "../assets/svgIcons/right-arrow.svg?react";
import LocationPointer from "../assets/svgIcons/location-pointer.svg?react";

const Landing = () => {
  const navigate = useNavigate();

  return (
    <section className="site-container">
      
      <section className="hero my-4">
        <div className="bg-[#008B8B] border border-[#008B8B] rounded-lg flex flex-col justify-center items-center md:px-3 md:pt-4 pb-4"> 
          <div className="relative h-55 pb-6 flex flex-col justify-center items-center md:h-auto" >
            <picture className="w-full rounded-lg">
                <source media="(min-width: 1024px)" srcSet={HeroL} />
                <source media="(min-width: 768px)" srcSet={HeroM} />
                <img src={HeroS} alt="flooded area with a water over road sign"  />
            </picture>
            <h1 className="text-[#F8F8FF] typo-4xl text-center font-medium py-6 absolute top-0 bg-[#008B8B]/20 h-full md:relative md:h-auto" > FLOOD ALERTS AND PREPAREDNESS  YOU CAN TRUST ACROSS AFRICA </h1>
          </div>

          <input type="email" placeholder="Enter your email to receive early flood warnings" className="w-full bg-white rounded-[20px] py-1.75 px-5 " /> <br />
          <Button children={"Receive emergency flood alerts"} rightSection={<RightArrow />} className="btn btn-primary btn-md" onClick={() => pages.signup && navigate(pages.signup)} />
        </div>
      </section>

      <section className="flood-risk-section bg-[#C6E2E8] rounded-xl mt-20 mb-12">
        <div className=" flex flex-col justify-center items-center gap-6 section ">
          <h2 className="typo-3xl mb-2 text-center " >Check for flood risk in your area</h2>
          <input type="text" placeholder="Enter your region" className="w-[80%] bg-white rounded-[20px] py-1.75 px-5" />
          <Button children={"Use My Current Location"} rightSection={<LocationPointer />} className="btn btn-md btn-accent " />

          <div className="flex gap-5 " >
            <Button children={"Check Flood Risk"} className="btn btn-primary btn-lg " />
            <Button children={"View Full Map"} rightSection={<RightArrow />} className="btn btn-md btn-accent " onClick={() => pages.map && navigate(pages.map)} />
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
            <img src={polygon} alt="polygon shape" className="w-18 h-16 md:w-29.75 md:h-26" />
          </div>
        </div>
        <div className="flex justify-center mx-auto py-8">
          <Button className="btn btn-primary btn-md" onClick={() => pages.chat && navigate(pages.chat)}>Start chat</Button>
        </div>
      </section>
    </section>
  );
};

export default Landing;
