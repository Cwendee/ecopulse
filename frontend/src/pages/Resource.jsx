import { useNavigate } from "react-router-dom";
import { ResourcessPage } from "../constants";

const Resource = () => {
  const navigate = useNavigate();
  return (
    <section className="site-container">
      <h1 className="typo-4xl">Find Resources Here</h1>
      <section className="flex flex-col gap-y-6 md:gap-y-12 p-0 m-0 cursor-pointer">
        {ResourcessPage.map((item, index) => (
          <div
            key={index}
            className="md:flex space-y-2 md:space-y-0 items-center justify-between border-[2.2px] border-[#296083] bg-[#C6E2E8] p-3 rounded-xl"
            onClick={() => item.link && navigate(item.link)}
          >
            <div>
              <h1 className="typo-xl">{item.title}</h1>
              <p className="typo-base">{item.description}</p>
            </div>
            <img src={item.image} alt={`${item.title} image`} />
          </div>
        ))}
      </section>
    </section>
  );
};

export default Resource;
