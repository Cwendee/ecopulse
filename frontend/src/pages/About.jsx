import AboutUs from "../assets/images/About-us.png";
import { aboutUs } from "../constants/index.js"

const About = () => {
  return (
    <section className="about-us site-container" >
      <div>
        <h1 className="typo-4xl " >About Us</h1>
        <img src={AboutUs} alt="A group of people sitting together" className="my-8 rounded-xl" />
        <div className="flex flex-col gap-8 " >
          {aboutUs.map(
            (container, index) => 
              <div 
              key={index}
              className={`container ${container.background} rounded-xl px-6 pt-5 md:pt-7.5 pb-6`}
              >
                <h2 className="text-[28px] md:text-[32px] lg:text-[56px] " >{container.title}</h2>
                <p className="typo-2xl text-left pr-6" >{container.content}</p>
              </div>
          )}
        </div>
      </div>
    </section>
);
};

export default About;
