import { ResourcesData } from "../constants";
import { useNavigate } from "react-router-dom";
import polygon from "../assets/svgIcons/polygon.svg";
import Button from "../components/ReUsables/Button";

const Landing = () => {
  const navigate = useNavigate();

  return (
    <section className="site-container">
      <section className="space-y-9.5 section">
        <h1 className="typo-3xl text-center">Find Resources</h1>
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
          <Button className="btn btn-primary btn-md">Start chat</Button>
        </div>
      </section>
    </section>
  );
};

export default Landing;
